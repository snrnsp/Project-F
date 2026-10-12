import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '[SerializeField] private Button returnToTitleButton;' in line:
        lines.insert(i+1, '        [SerializeField] private Button deleteDataButton;\n')
        break

for i, line in enumerate(lines):
    if 'if (returnToTitleButton != null)' in line and 'returnToTitleButton.onClick.AddListener' in line:
        lines.insert(i+4, '            if (deleteDataButton != null) deleteDataButton.onClick.AddListener(OnDeleteDataClicked);\n')
        break

for i, line in enumerate(lines):
    if 'if (returnToTitleButton != null) returnToTitleButton.onClick.RemoveListener' in line:
        lines.insert(i+1, '            if (deleteDataButton != null) deleteDataButton.onClick.RemoveListener(OnDeleteDataClicked);\n')
        break

# Add OnDeleteDataClicked at the end before the last two braces
new_method = '''
        private void OnDeleteDataClicked()
        {
            UnityEngine.PlayerPrefs.DeleteKey("HalloweenVN_Save_0");
            UnityEngine.PlayerPrefs.Save();
            Hide();
            if (HalloweenVN.Core.GameManager.Instance != null && HalloweenVN.Core.GameManager.Instance.CurrentPhase != HalloweenVN.Core.GamePhase.Lobby)
            {
                HalloweenVN.Core.GameManager.Instance.ChangePhase(HalloweenVN.Core.GamePhase.Lobby);
            }
        }
'''

for i in range(len(lines)-1, -1, -1):
    if '}' in lines[i]:
        if '}' in lines[i-1]:
            lines.insert(i-1, new_method)
            break

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Updated SettingsUI.cs")
