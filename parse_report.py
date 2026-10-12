import sys

filepath = 'C:/Users/cccc0/.gemini/antigravity/brain/fc10953b-5038-4aaf-8269-364bd034e7f8/scratch/character_sprite_audit_report.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Collect the most critical issues, ignoring the repetitive "noFade=true" issues for a moment
critical_issues = []
for i, line in enumerate(lines):
    if "문제 발견" in line:
        issue_desc = lines[i+2].strip()
        if "noFade=true 누락" not in issue_desc:
            critical_issues.append("".join(lines[i:i+4]))

print("Critical Issues found (excluding noFade):")
for issue in critical_issues:
    print(issue)
