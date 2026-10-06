#!/usr/bin/env python3
"""
Export ALL player-facing text of the game into one translation table:

    Assets/Resources/Localization/game_text.csv

The same file is (1) the deliverable for translators and (2) the runtime table read by
Assets/Scripts/Core/Loc.cs. Translators fill the EN / JA / ZH-CN / ZH-TW columns; drop the file
back at the same path and the game uses it.

Sources
  * Dialogue lines / choices : Assets/Resources/Data/Dialogues/*.json   (test_* and _legacy skipped)
  * Speaker names            : unique "speaker" values of those dialogues  -> speaker.<KoreanName>
  * Evidence / case texts    : Assets/Resources/Data/Evidence/*.json, Data/Cases/*.json (test_* skipped)
  * UI text                  : every  Loc.Get("key", "한국어")  /  Loc.Format("key", "한국어", ...)  in Assets/Scripts

Re-running is safe: translations already in the CSV are kept (matched by Key). If the Korean text
of a row changed since the last export and it already has translations, the row is flagged in Notes.

Usage
  python Tools/Localization/export_game_text.py                 # regenerate / update the CSV
  python Tools/Localization/export_game_text.py --seed a.csv    # also import translations from seed CSVs
                                                                 # (header: Key,EN,JA,ZH-CN,ZH-TW[,Context])
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'Assets', 'Resources', 'Localization', 'game_text.csv')
REPORT = os.path.join(ROOT, 'Tools', 'Localization', 'export_report.txt')
DLG_DIR = os.path.join(ROOT, 'Assets', 'Resources', 'Data', 'Dialogues')
EVIDENCE_DIR = os.path.join(ROOT, 'Assets', 'Resources', 'Data', 'Evidence')
CASE_DIR = os.path.join(ROOT, 'Assets', 'Resources', 'Data', 'Cases')
SCRIPTS_DIR = os.path.join(ROOT, 'Assets', 'Scripts')

# Play order (files not listed are appended alphabetically after these)
PLAY_ORDER = [
    'ch0_origin', 'ch0_gathering', 'ch0_opening',
    'ch1_morning', 'ch1_night', 'ch1_investigation_talk',
    'ch1_result_perfect', 'ch1_resolution', 'ch1_epilogue', 'ch1_result_fail',
]

LANGS = ['EN', 'JA', 'ZH-CN', 'ZH-TW']
LEGACY_FIELD = {'EN': 'text_en', 'JA': 'text_ja', 'ZH-CN': 'text_cn', 'ZH-TW': 'text_tw'}
HEADER = ['Key', 'Category', 'Speaker', 'Context', 'Notes', 'KO'] + LANGS
KO_CHANGED_FLAG = '!! KO CHANGED since last export - re-check translation.'

LOC_CALL = re.compile(r'Loc\.(Get|Format)\(\s*"([^"\\]+)"\s*,\s*"((?:[^"\\]|\\.)*)"')
SPEAKER_CALL = re.compile(r'Loc\.Speaker\(')


def esc(s):
    """Real line breaks -> the two-character token \\n (Loc.cs converts back)."""
    return (s or '').replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n')


def decode_cs_literal(s):
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == '\\' and i + 1 < len(s):
            nx = s[i + 1]
            if nx == 'n': out.append('\n'); i += 2; continue
            if nx == 't': out.append('\t'); i += 2; continue
            if nx == 'r': i += 2; continue
            if nx in '"\\\'': out.append(nx); i += 2; continue
            if nx == 'u' and i + 5 < len(s):
                out.append(chr(int(s[i + 2:i + 6], 16))); i += 6; continue
        out.append(ch)
        i += 1
    return ''.join(out)


def auto_notes(text):
    notes = []
    if '\n' in text:
        notes.append('Contains manual line break(s) written as \\n - keep the \\n token (you may move it).')
    if re.search(r'<[^<>]+>', text):
        notes.append('Contains rich-text tags <...> - keep tags unchanged.')
    ph = sorted(set(re.findall(r'\{\d+[^}]*\}', text)))
    if ph:
        notes.append('Placeholders ' + ' '.join(ph) + ' must be kept.')
    return ' '.join(notes)


def char_of(path):
    """'Characters/미나/검은색 버전/기본' -> '미나'"""
    if not path:
        return None
    parts = path.replace('\\', '/').split('/')
    return parts[1] if len(parts) > 1 and parts[0] == 'Characters' else parts[0]


class Table:
    def __init__(self):
        self.rows = OrderedDict()
        self.warnings = []

    def add(self, key, category, ko, speaker='', context='', notes='', legacy=None):
        if key in self.rows:
            if self.rows[key]['KO'] != esc(ko):
                self.warnings.append(f'Duplicate key with different Korean text: {key!r}: '
                                     f'{self.rows[key]["KO"]!r} vs {esc(ko)!r} (first one kept)')
            return
        row = {'Key': key, 'Category': category, 'Speaker': speaker, 'Context': context,
               'Notes': ' '.join(x for x in [notes, auto_notes(ko)] if x), 'KO': esc(ko)}
        for l in LANGS:
            row[l] = esc((legacy or {}).get(l, '') or '')
        self.rows[key] = row


def load_json(path):
    with open(path, encoding='utf-8-sig') as f:
        return json.load(f)


def collect_dialogues(t, speakers):
    files = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(DLG_DIR, '*.json'))]
    files = [f for f in files if not f.startswith('test_')]
    ordered = [f for f in PLAY_ORDER if f in files] + sorted(f for f in files if f not in PLAY_ORDER)
    counts = OrderedDict()
    for name in ordered:
        data = load_json(os.path.join(DLG_DIR, name + '.json'))
        did = data.get('dialogueId') or name
        n_rows = 0
        for node in data.get('nodes', []):
            text = node.get('text') or ''
            spk = (node.get('speaker') or '').strip()
            on_screen = []
            for slot, field in (('L', 'characterSpriteLeft'), ('C', 'characterSpriteCenter'), ('R', 'characterSpriteRight')):
                c = char_of(node.get(field))
                if c:
                    on_screen.append(f'{c}({slot})')
            ctx = ('On screen: ' + ', '.join(on_screen)) if on_screen else 'No characters on screen'
            if text.strip():
                if spk:
                    speakers.setdefault(spk, did)
                legacy = {l: node.get(LEGACY_FIELD[l]) for l in LANGS}
                t.add(f'dlg.{did}.{node.get("id")}', f'Dialogue/{did}', text,
                      speaker=spk if spk else '(Narration)', context=ctx, legacy=legacy)
                n_rows += 1
            for i, ch in enumerate(node.get('choices') or []):
                ctext = ch.get('text') or ''
                if not ctext.strip():
                    continue
                legacy = {l: ch.get(LEGACY_FIELD[l]) for l in LANGS}
                t.add(f'dlg.{did}.{node.get("id")}.choice{i}', f'Choice/{did}', ctext,
                      speaker='(Player choice)', context=f'Choice button {i + 1} after line dlg.{did}.{node.get("id")}',
                      notes='Choice button - keep short (one line).', legacy=legacy)
                n_rows += 1
        counts[did] = n_rows
    return counts


def collect_speakers(t, speakers, ui_speaker_defaults):
    names = list(speakers.keys())
    for k in ui_speaker_defaults:
        if k not in names:
            names.append(k)
    for name in names:
        where = f'first speaks in {speakers[name]}' if name in speakers else 'character name in UI'
        t.add(f'speaker.{name}', 'Speaker', name, context=f'Name plate above the dialogue box ({where}).',
              notes='Character/speaker name - keep consistent everywhere.')


def collect_evidence_and_cases(t):
    for path in sorted(glob.glob(os.path.join(EVIDENCE_DIR, '*.json'))):
        if os.path.basename(path).startswith('test_'):
            continue
        for e in load_json(path).get('evidences', []):
            t.add(f'evidence.{e["id"]}.name', 'Evidence', e.get('evidenceName') or '',
                  context='Evidence item name (list / drag item / slot).', notes='Short title.')
            t.add(f'evidence.{e["id"]}.desc', 'Evidence', e.get('description') or '',
                  context=f'Evidence description shown in the detail popup ({e.get("evidenceName")}).')
    for path in sorted(glob.glob(os.path.join(CASE_DIR, '*.json'))):
        if os.path.basename(path).startswith('test_'):
            continue
        c = load_json(path)
        t.add(f'case.{c["caseId"]}.name', 'Case', c.get('caseName') or '', context='Case title on the deduction screen.')
        for i, q in enumerate(c.get('questions') or []):
            t.add(f'case.{c["caseId"]}.q{i}', 'Case', q.get('questionText') or '',
                  context=f'Deduction question {i + 1}; the answer is an evidence item.')


def collect_ui(t, seeds_ctx):
    found = OrderedDict()  # key -> (ko, [files])
    conflicts = []
    for path in sorted(glob.glob(os.path.join(SCRIPTS_DIR, '**', '*.cs'), recursive=True)):
        with open(path, encoding='utf-8-sig') as f:
            src = f.read()
        fname = os.path.splitext(os.path.basename(path))[0]
        for m in LOC_CALL.finditer(src):
            key, ko = m.group(2), decode_cs_literal(m.group(3))
            if key in found:
                if found[key][0] != ko:
                    conflicts.append(f'{key}: {found[key][0]!r} ({found[key][1][0]}) vs {ko!r} ({fname})')
                if fname not in found[key][1]:
                    found[key][1].append(fname)
            else:
                found[key] = (ko, [fname])
    speaker_defaults = OrderedDict()
    for key, (ko, files) in found.items():
        if key.startswith('speaker.'):
            speaker_defaults[key[len('speaker.'):]] = ko
            continue
        t.add(key, 'UI/' + '+'.join(files), ko, context=seeds_ctx.get(key, ''))
    t.warnings += ['UI key used with different Korean defaults: ' + c for c in conflicts]
    return speaker_defaults


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', action='append', default=[], help='seed CSV with existing translations')
    ap.add_argument('--out', default=OUT)
    args = ap.parse_args()

    seeds = {}
    seeds_ctx = {}
    for s in args.seed:
        for r in read_csv(s):
            k = (r.get('Key') or '').strip()
            if not k:
                continue
            seeds.setdefault(k, {})
            for l in LANGS:
                v = r.get(l) or ''
                if v and not seeds[k].get(l):
                    seeds[k][l] = esc(v)
            if r.get('Context') and k not in seeds_ctx:
                seeds_ctx[k] = r['Context']

    t = Table()
    speakers = OrderedDict()
    ui_speakers = collect_ui(t, seeds_ctx)          # collected first to get speaker defaults
    ui_rows = list(t.rows.values())
    t.rows.clear()
    dlg_counts = collect_dialogues(Table(), speakers)  # dry pass: gather speakers in play order
    collect_speakers(t, speakers, ui_speakers)
    for r in ui_rows:
        t.rows[r['Key']] = r
    collect_evidence_and_cases(t)
    dlg_counts = collect_dialogues(t, OrderedDict())

    # Merge: existing CSV translations > seed translations > legacy JSON fields
    existing = {}
    if os.path.exists(args.out):
        for r in read_csv(args.out):
            if r.get('Key'):
                existing[r['Key'].strip()] = r
    flagged, kept, seeded = [], 0, 0
    for key, row in t.rows.items():
        for l in LANGS:
            if seeds.get(key, {}).get(l) and not row[l]:
                row[l] = seeds[key][l]; seeded += 1
        old = existing.get(key)
        if old:
            has_tr = False
            for l in LANGS:
                if (old.get(l) or '').strip():
                    row[l] = old[l]; kept += 1; has_tr = True
            if has_tr and (old.get('KO') or '') != row['KO']:
                row['Notes'] = (KO_CHANGED_FLAG + ' Old KO: ' + (old.get('KO') or '') + ' ' + row['Notes']).strip()
                flagged.append(key)
            elif KO_CHANGED_FLAG in (old.get('Notes') or '') and has_tr:
                row['Notes'] = old['Notes']  # keep the flag until someone clears it
                flagged.append(key)
    removed = [k for k in existing if k not in t.rows]

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL, lineterminator='\r\n')
        w.writeheader()
        for row in t.rows.values():
            w.writerow(row)

    cats = OrderedDict()
    for row in t.rows.values():
        c = row['Category'].split('/')[0]
        cats[c] = cats.get(c, 0) + 1
    ko_chars = sum(len(r['KO'].replace('\\n', '')) for r in t.rows.values())
    lines = [f'Output: {args.out}', f'Total rows: {len(t.rows)}  (Korean characters: {ko_chars})']
    lines += [f'  {c}: {n}' for c, n in cats.items()]
    lines += ['Dialogue rows per file:'] + [f'  {k}: {v}' for k, v in dlg_counts.items()]
    lines.append(f'Translations kept from existing CSV: {kept} cells, imported from seeds: {seeded} cells')
    lines.append(f'Rows flagged KO-changed: {len(flagged)}')
    lines += ['  ' + k for k in flagged]
    lines.append(f'Keys in old CSV that no longer exist (dropped): {len(removed)}')
    lines += ['  ' + k for k in removed]
    lines.append(f'Warnings: {len(t.warnings)}')
    lines += ['  ' + w_ for w_ in t.warnings]
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'rows={len(t.rows)} flagged={len(flagged)} removed={len(removed)} warnings={len(t.warnings)} -> {REPORT}')
    return 1 if t.warnings else 0


if __name__ == '__main__':
    sys.exit(main())
