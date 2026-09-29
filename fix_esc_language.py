import sys

path = 'F:/Project-F/Assets/Scripts/UI/GlobalUIManager.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

new_logic = """                // 0. If LanguageUI is open, close it.
                var langUi = UnityEngine.Object.FindFirstObjectByType<LanguageUI>(UnityEngine.FindObjectsInactive.Exclude);
                if (langUi != null && langUi.gameObject.activeInHierarchy)
                {
                    langUi.Hide();
                    return;
                }

                // 1. If Settings is open, close it."""

content = content.replace('// 1. If Settings is open, close it.', new_logic)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Added LanguageUI ESC check to GlobalUIManager.cs")
