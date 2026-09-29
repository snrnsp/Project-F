import sys

path = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace '35 + offset' with '24 + offset' for all buttons
old_str = "fontSize = 35 + offset;"
new_str = "fontSize = 26 + offset;"

if old_str in content:
    content = content.replace(old_str, new_str)
    
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✅ LobbyUI.cs 글꼴 크기 변경 성공 (35 -> 26)")
else:
    print("❌ 대상 텍스트를 찾을 수 없습니다.")
