import sys

path = 'F:/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'speechStyle =' in line and '홍차 한 잔' in line:
        new_lines.append('            speechStyle = isEn ? "Polite.\\n\\\"Once you finish your tea, I\'ll bring you the next case file.\\\"" : "존댓말.\\n\\\"홍차 한 잔 다 드시면, 다음 사건 파일 가져다 드릴게요.\\\"",\n')
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(new_lines)

print("Fixed syntax error")
