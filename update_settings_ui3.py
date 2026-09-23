import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            yesBtn.onClick.AddListener(() => {
                // Do not destroy the overlay so it remains visible during the fade out!
                ExecuteDeleteData();
            });"""

replacement = """            yesBtn.onClick.AddListener(() => {
                yesBtn.interactable = false;
                noBtn.interactable = false;
                // Do not destroy the overlay so it remains visible during the fade out!
                ExecuteDeleteData();
            });"""

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Modified SettingsUI.cs interactable logic")
else:
    print("Could not find target.")
