import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'private void UpdateContinueButton()' in line:
        start_idx = i
    if 'private void OnNewGameClicked()' in line and start_idx != -1:
        end_idx = i - 1
        break

print(f"Start: {start_idx}, End: {end_idx}")

new_code = '''        private void UpdateContinueButton()
        {
            if (continueButton != null)
            {
                bool hasSave = UnityEngine.PlayerPrefs.HasKey("HalloweenVN_Save_0");
                continueButton.interactable = hasSave;
                
                CanvasGroup cg = continueButton.GetComponent<CanvasGroup>();
                if (cg != null) cg.alpha = hasSave ? 1f : 0.5f;
            }
        }
'''

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx] = [new_code]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Replaced successfully.")
else:
    print("Could not find the block.")
