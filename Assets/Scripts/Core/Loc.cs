using System.Collections.Generic;
using System.Text;
using UnityEngine;
using HalloweenVN.Data;

namespace HalloweenVN.Core
{
    /// <summary>
    /// Runtime string table for ALL player-facing text.
    ///
    /// Source file: Assets/Resources/Localization/game_text.csv (UTF-8, header row required).
    /// Columns are matched by header name: Key, KO, EN, JA, ZH-CN, ZH-TW (other columns such as
    /// Category / Context / Notes are for translators and ignored at runtime).
    ///
    /// Korean always comes from the source (dialogue JSON / code defaults). The CSV supplies the
    /// other languages; when a cell is empty we fall back to the given fallback (legacy per-node
    /// translations, then Korean). Regenerate the CSV with Tools/Localization/export_game_text.py.
    /// Line breaks inside a cell are written as the two-character token \n and converted on load.
    /// </summary>
    public static class Loc
    {
        public const string ResourcePath = "Localization/game_text";
        private static readonly string[] LangHeaders = { "KO", "EN", "JA", "ZH-CN", "ZH-TW" };
        private static Dictionary<string, string[]> _table;

        public static int Count { get { EnsureLoaded(); return _table.Count; } }

        /// <summary>Forces the CSV to be re-read on next access (e.g. after hot-swapping the file in the editor).</summary>
        public static void Reload() { _table = null; }

        /// <summary>
        /// Text for <paramref name="key"/> in the current language.
        /// <paramref name="fallback"/> is the Korean source text (or the best existing translation) and is
        /// returned in Korean mode and whenever the CSV has no translation for the current language.
        /// </summary>
        public static string Get(string key, string fallback)
        {
            int li = (int)SettingsData.Language;
            if (li <= 0) return fallback;
            EnsureLoaded();
            if (_table.TryGetValue(key, out var row) && li < row.Length && !string.IsNullOrEmpty(row[li]))
                return row[li];
            return fallback;
        }

        /// <summary>string.Format convenience: Loc.Format("ui.x", "남은 {0}개", n)</summary>
        public static string Format(string key, string fallback, params object[] args)
        {
            return string.Format(Get(key, fallback), args);
        }

        // ── Dialogue helpers ─────────────────────────────────────────────

        public static string DialogueKey(string dialogueId, int nodeId) => $"dlg.{dialogueId}.{nodeId}";

        /// <summary>Line text for a node in the current language.</summary>
        public static string NodeText(string dialogueId, DialogueNode node)
        {
            if (node == null) return "";
            string ko = node.text ?? "";
            string legacy = LegacyField(node.text_en, node.text_ja, node.text_cn, node.text_tw);
            if (string.IsNullOrEmpty(dialogueId)) return string.IsNullOrEmpty(legacy) ? ko : legacy;
            return Get(DialogueKey(dialogueId, node.id), string.IsNullOrEmpty(legacy) ? ko : legacy);
        }

        /// <summary>Choice text for a node's choice in the current language.</summary>
        public static string ChoiceText(string dialogueId, int nodeId, int choiceIndex, DialogueChoice choice)
        {
            if (choice == null) return "";
            string ko = choice.text ?? "";
            string legacy = LegacyField(choice.text_en, choice.text_ja, choice.text_cn, choice.text_tw);
            string fb = string.IsNullOrEmpty(legacy) ? ko : legacy;
            if (string.IsNullOrEmpty(dialogueId)) return fb;
            return Get($"{DialogueKey(dialogueId, nodeId)}.choice{choiceIndex}", fb);
        }

        /// <summary>Display name for a speaker (the Korean name stays the internal identifier, e.g. for name colors).</summary>
        public static string Speaker(string koreanName)
        {
            if (string.IsNullOrWhiteSpace(koreanName)) return koreanName;
            string trimmed = koreanName.Trim();
            return Get("speaker." + trimmed, trimmed);
        }

        public static string EvidenceName(EvidenceInfo e) => e == null ? "" : Get($"evidence.{e.id}.name", e.evidenceName);
        public static string EvidenceDescription(EvidenceInfo e) => e == null ? "" : Get($"evidence.{e.id}.desc", e.description);
        public static string CaseName(CaseContainer c) => c == null ? "" : Get($"case.{c.caseId}.name", c.caseName);
        public static string CaseQuestion(CaseContainer c, int i) =>
            (c == null || c.questions == null || i < 0 || i >= c.questions.Count) ? "" : Get($"case.{c.caseId}.q{i}", c.questions[i].questionText);

        private static string LegacyField(string en, string ja, string cn, string tw)
        {
            switch (SettingsData.Language)
            {
                case GameLanguage.English: return en;
                case GameLanguage.Japanese: return ja;
                case GameLanguage.ChineseSimplified: return cn;
                case GameLanguage.ChineseTraditional: return tw;
                default: return null;
            }
        }

        // ── CSV loading ──────────────────────────────────────────────────

        private static void EnsureLoaded()
        {
            if (_table != null) return;
            _table = new Dictionary<string, string[]>();
            var asset = Resources.Load<TextAsset>(ResourcePath);
            if (asset == null) return; // no table yet → everything falls back to source text

            var rows = ParseCsv(asset.text);
            if (rows.Count == 0) return;

            var header = rows[0];
            int keyCol = -1;
            int[] langCols = { -1, -1, -1, -1, -1 };
            for (int c = 0; c < header.Count; c++)
            {
                string h = header[c].Trim().TrimStart('\uFEFF');
                if (h == "Key") keyCol = c;
                for (int l = 0; l < LangHeaders.Length; l++) if (h == LangHeaders[l]) langCols[l] = c;
            }
            if (keyCol < 0)
            {
                Debug.LogWarning("[Loc] game_text.csv has no 'Key' column; localization table ignored.");
                return;
            }

            for (int r = 1; r < rows.Count; r++)
            {
                var row = rows[r];
                if (keyCol >= row.Count) continue;
                string key = row[keyCol].Trim();
                if (key.Length == 0) continue;
                var vals = new string[LangHeaders.Length];
                for (int l = 0; l < LangHeaders.Length; l++)
                {
                    int c = langCols[l];
                    vals[l] = (c >= 0 && c < row.Count) ? row[c].Replace("\\n", "\n") : null;
                }
                _table[key] = vals;
            }
        }

        /// <summary>RFC 4180 parser: quoted fields, escaped quotes (""), and newlines inside quotes.</summary>
        private static List<List<string>> ParseCsv(string text)
        {
            var rows = new List<List<string>>();
            if (string.IsNullOrEmpty(text)) return rows;
            if (text[0] == '\uFEFF') text = text.Substring(1);

            var row = new List<string>();
            var field = new StringBuilder();
            bool inQuotes = false;
            for (int i = 0; i < text.Length; i++)
            {
                char ch = text[i];
                if (inQuotes)
                {
                    if (ch == '"')
                    {
                        if (i + 1 < text.Length && text[i + 1] == '"') { field.Append('"'); i++; }
                        else inQuotes = false;
                    }
                    else field.Append(ch);
                }
                else if (ch == '"') inQuotes = true;
                else if (ch == ',') { row.Add(field.ToString()); field.Length = 0; }
                else if (ch == '\r') { /* handled with \n */ }
                else if (ch == '\n')
                {
                    row.Add(field.ToString()); field.Length = 0;
                    rows.Add(row); row = new List<string>();
                }
                else field.Append(ch);
            }
            if (field.Length > 0 || row.Count > 0) { row.Add(field.ToString()); rows.Add(row); }
            // Normalize CRLF that appeared inside quoted fields
            foreach (var r in rows) for (int c = 0; c < r.Count; c++) r[c] = r[c].Replace("\r\n", "\n");
            return rows;
        }
    }
}
