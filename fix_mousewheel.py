import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''        private void Update\(\)\r?\n\s*\{\r?\n\s*if \(GameManager\.Instance != null && GameManager\.Instance\.CurrentPhase != GamePhase\.Dialogue\) return;\r?\n\s*if \(choicePanel != null && choicePanel\.activeSelf\) return;\r?\n\s*if \(IsModalOpen\(\)\) return;\r?\n\s*// 1\. Right click to toggle UI visibility \(to see CG/Backgrounds\)'''

replacement = r'''        private void Update()
        {
            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase != GamePhase.Dialogue) return;
            if (IsModalOpen()) return;

            // 3. Mouse wheel up to open log (Allow this even during choices)
            if (UnityEngine.InputSystem.Mouse.current != null && UnityEngine.InputSystem.Mouse.current.scroll.ReadValue().y > 0)
            {
                if (_cachedBacklogUI != null && !_cachedBacklogUI.IsOpen)
                {
                    _cachedBacklogUI.ShowBacklog();
                    return; // Stop processing further input for this frame
                }
            }

            if (choicePanel != null && choicePanel.activeSelf) return;

            // 1. Right click to toggle UI visibility (to see CG/Backgrounds)'''

new_content = re.sub(pattern, replacement, content)

# Remove the old mouse wheel check down below
pattern2 = r'''            // 3\. Mouse wheel up to open log\r?\n\s*if \(Mouse\.current != null && Mouse\.current\.scroll\.ReadValue\(\)\.y > 0\)\r?\n\s*\{\r?\n\s*if \(_cachedBacklogUI != null && !_cachedBacklogUI\.IsOpen\)\r?\n\s*\{\r?\n\s*_cachedBacklogUI\.ShowBacklog\(\);\r?\n\s*\}\r?\n\s*\}'''
replacement2 = r'''            // (Mouse wheel check moved to top to allow opening during choices)'''
new_content = re.sub(pattern2, replacement2, new_content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed Mouse Wheel backlog opening during choices!")
else:
    print("Failed to match Mouse Wheel logic!")
