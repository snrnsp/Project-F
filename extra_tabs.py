import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        public void SelectCharacter(int index)
        {
            if (index < 0 || index >= profiles.Count) return;'''
            
replacement = '''        public void SelectCharacter(int index)
        {
            if (index < 0 || index >= profiles.Count) return;

            // Update Tab Visuals
            for (int i = 0; i < characterTabs.Count; i++)
            {
                Button tabBtn = characterTabs[i];
                if (tabBtn == null) continue;
                
                UnityEngine.UI.Image img = tabBtn.GetComponent<UnityEngine.UI.Image>();
                TMPro.TextMeshProUGUI txt = tabBtn.GetComponentInChildren<TMPro.TextMeshProUGUI>();
                
                if (i == index)
                {
                    // Selected state: Darker color, larger text
                    if (img != null) img.color = new Color32(40, 15, 5, 255);
                    if (txt != null) txt.fontSize = 24;
                }
                else
                {
                    // Normal state
                    if (img != null) img.color = new Color32(80, 35, 10, 255);
                    if (txt != null) txt.fontSize = 18;
                }
            }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated ExtraUI.cs with Tab Selection visuals')
else:
    print('Target not found')
