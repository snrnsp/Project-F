import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

# Change the yesBtn click listener to not destroy the overlay
target = """            yesBtn.onClick.AddListener(() => {
                Destroy(overlay);
                ExecuteDeleteData();
            });"""

replacement = """            yesBtn.onClick.AddListener(() => {
                // Do not destroy the overlay so it remains visible during the fade out!
                ExecuteDeleteData();
            });"""

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Modified SettingsUI.cs overlay destroy logic")
else:
    print("Could not find target.")
