import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 1. Remove ShowPreAlphaWarning from Start
pattern1 = r'''        private void Start\(\)\r?\n\s*\{\r?\n\s*ShowPreAlphaWarning\(\);'''
replacement1 = r'''        private void Start()
        {'''
content = re.sub(pattern1, replacement1, content)

# 2. Change OnNewGameClicked to call the renamed ShowPhotosensitivityWarning
pattern2 = r'''        private void OnNewGameClicked\(\)\r?\n\s*\{\r?\n\s*if \(UnityEngine\.EventSystems\.EventSystem\.current != null\) UnityEngine\.EventSystems\.EventSystem\.current\.SetSelectedGameObject\(null\);\r?\n\s*if \(isStartingGame\) return;\r?\n\s*isStartingGame = true;\r?\n\s*StartNewGame\(null\);\r?\n\s*\}'''
replacement2 = r'''        private void OnNewGameClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            if (isStartingGame) return;
            isStartingGame = true;
            ShowPhotosensitivityWarning();
        }'''
content = re.sub(pattern2, replacement2, content)

# 3. Rename ShowPreAlphaWarning and update the buttons
pattern3 = r'''        private void ShowPreAlphaWarning\(\)\r?\n\s*\{\r?\n(.*?)overlayBtn\.onClick\.AddListener\(\(\) => \{\r?\n\s*if \(isStartingGame\) return;\r?\n\s*Destroy\(overlay\);\r?\n\s*\}\);(.*?)btn\.onClick\.AddListener\(\(\) =>\r?\n\s*\{\r?\n\s*if \(UnityEngine\.EventSystems\.EventSystem\.current != null\) UnityEngine\.EventSystems\.EventSystem\.current\.SetSelectedGameObject\(null\);\r?\n\s*Destroy\(overlay\);\r?\n\s*\}\);\r?\n\s*\}'''
replacement3 = r'''        private void ShowPhotosensitivityWarning()
        {
\1overlayBtn.onClick.AddListener(() => {
                if (isStartingGame && !overlay.activeSelf) return; // Prevent closing if already transitioning
                isStartingGame = false;
                Destroy(overlay);
            });\2btn.onClick.AddListener(() =>
            {
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                StartNewGame(overlay);
            });
        }'''
content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Fixed LobbyUI warning logic!")
