import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                if (i == index)
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
                }'''
                
replacement = '''                if (i == index)
                {
                    // Selected state: Bright highlighted color, larger text
                    if (img != null) img.color = new Color32(230, 100, 20, 255); // Bright pumpkin orange
                    if (txt != null) {
                        txt.fontSize = 24;
                        txt.color = Color.white;
                    }
                }
                else
                {
                    // Normal state: Darker faded color
                    if (img != null) img.color = new Color32(60, 25, 10, 255);
                    if (txt != null) {
                        txt.fontSize = 18;
                        txt.color = new Color32(200, 200, 200, 255); // Slightly faded text
                    }
                }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated ExtraUI.cs tab colors to be brighter when selected')
else:
    print('Target not found')
