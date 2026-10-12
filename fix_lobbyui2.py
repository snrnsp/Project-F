import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace the first ShowPhotosensitivityWarning() back to ShowPreAlphaWarning()
content = content.replace('        private void ShowPhotosensitivityWarning()\r\n        {\r\n            GameObject overlay = new GameObject("PreAlphaOverlay");', '        private void ShowPreAlphaWarning()\r\n        {\r\n            GameObject overlay = new GameObject("PreAlphaOverlay");')
content = content.replace('        private void ShowPhotosensitivityWarning()\n        {\n            GameObject overlay = new GameObject("PreAlphaOverlay");', '        private void ShowPreAlphaWarning()\n        {\n            GameObject overlay = new GameObject("PreAlphaOverlay");')

# Change OnNewGameClicked to call ShowPhotosensitivityWarning
pattern_newgame = r'''        private void OnNewGameClicked\(\)\r?\n\s*\{\r?\n\s*if \(UnityEngine\.EventSystems\.EventSystem\.current != null\) UnityEngine\.EventSystems\.EventSystem\.current\.SetSelectedGameObject\(null\);\r?\n\s*if \(isStartingGame\) return;\r?\n\s*isStartingGame = true;\r?\n\s*ShowPhotosensitivityWarning\(\);\r?\n\s*\}'''
# It's already calling ShowPhotosensitivityWarning, so leave it.

# In ShowPreAlphaWarning (the restored one), change its OK button back to Destroy(overlay)
pattern_prealpha = r'''Destroy\(overlay\);\r?\n\s*ShowPhotosensitivityWarning\(\);\r?\n\s*\}\);\r?\n\s*\}'''
replacement_prealpha = r'''Destroy(overlay);
            });
        }'''
content = re.sub(pattern_prealpha, replacement_prealpha, content, count=1)

# Fix the overlay click in ShowPreAlphaWarning
pattern_prealpha_overlay = r'''overlayBtn\.onClick\.AddListener\(\(\) => \{\r?\n\s*if \(isStartingGame && !overlay\.activeSelf\) return; // Prevent closing if already transitioning\r?\n\s*isStartingGame = false;\r?\n\s*Destroy\(overlay\);\r?\n\s*\}\);'''
replacement_prealpha_overlay = r'''overlayBtn.onClick.AddListener(() => {
                Destroy(overlay);
            });'''
content = re.sub(pattern_prealpha_overlay, replacement_prealpha_overlay, content, count=1)

# Add ShowPreAlphaWarning back to Start
pattern_start = r'''        private void Start\(\)\r?\n\s*\{\r?\n\s*if \(newGameButton != null\)'''
replacement_start = r'''        private void Start()
        {
            ShowPreAlphaWarning();
            if (newGameButton != null)'''
content = re.sub(pattern_start, replacement_start, content, count=1)

# Fix the REAL ShowPhotosensitivityWarning
pattern_photo = r'''void ShowPhotosensitivityWarning\(\)\r?\n\s*\{\r?\n(.*?)overlayBtn\.onClick\.AddListener\(\(\) => \{\r?\n\s*if \(isStartingGame\) return;\r?\n\s*Destroy\(overlay\);\r?\n\s*\}\);(.*?)btn\.onClick\.AddListener\(\(\) =>\r?\n\s*\{\r?\n\s*if \(UnityEngine\.EventSystems\.EventSystem\.current != null\) UnityEngine\.EventSystems\.EventSystem\.current\.SetSelectedGameObject\(null\);\r?\n\s*Destroy\(overlay\);\r?\n\s*\}\);\r?\n\s*\}'''
replacement_photo = r'''private void ShowPhotosensitivityWarning()
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
content = re.sub(pattern_photo, replacement_photo, content, flags=re.DOTALL)

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Restored LobbyUI logic correctly!")
