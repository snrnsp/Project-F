import re

with open('Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = re.sub(
    r"else if \(used\.Count == 2\) xs = new\[\] \{ 0\.25f, 0\.75f \};",
    r"else if (used.Count == 2) xs = new[] { 0.33f, 0.67f };",
    content
)

with open('Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Patched DialogueUI.cs Layout Targets via regex")
