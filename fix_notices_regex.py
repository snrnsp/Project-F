import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 1. Modify Start()
if 'ShowPreAlphaWarning();' not in content:
    content = re.sub(r'private void Start\s*\(\)\s*\{', r'private void Start()\n        {\n            ShowPreAlphaWarning();\n', content)
    print("Injected ShowPreAlphaWarning into Start().")

# 2. Modify OnNewGameClicked
content = re.sub(r'private void OnNewGameClicked\s*\(\)\s*\{[\s\S]*?\}', 
r'''        private void OnNewGameClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            if (isStartingGame) return;
            isStartingGame = true;
            StartNewGame(null);
        }''', content)
print("Modified OnNewGameClicked().")

# 3. Modify Photosensitivity Warning OK button
content = re.sub(
r'''btn\.onClick\.AddListener\(\(\) =>\s*\{\s*if \(isStartingGame\) return;\s*isStartingGame = true;\s*if \(UnityEngine\.EventSystems\.EventSystem\.current != null\) UnityEngine\.EventSystems\.EventSystem\.current\.SetSelectedGameObject\(null\);\s*// We do NOT set interactable.*?StartNewGame\(overlay\);\s*\}\);''',
r'''btn.onClick.AddListener(() =>
            {
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                Destroy(overlay);
            });''', content, flags=re.DOTALL)
print("Modified Photosensitivity Warning.")

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
