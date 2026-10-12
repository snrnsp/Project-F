import sys

filepath = 'C:/Users/cccc0/.gemini/antigravity/brain/fc10953b-5038-4aaf-8269-364bd034e7f8/scratch/character_sprite_audit_report.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out_lines = []
current_file = ""
for i, line in enumerate(lines):
    if line.startswith("**파일:"):
        current_file = line.strip()
    if "문제 발견" in line:
        issue_desc = lines[i+2].strip()
        if "noFade=true" not in issue_desc:
            out_lines.append(f"{current_file}\n" + "".join(lines[i:i+4]) + "\n")

with open('critical_sprite_issues.txt', 'w', encoding='utf-8') as f:
    f.writelines(out_lines)
