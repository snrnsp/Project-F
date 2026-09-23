import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                else if (charNames[ci] == "카스미") {
                    portraitImg.sprite = Resources.Load<Sprite>("Images/Characters/kasumi_default");
                    // Shift Kasumi down and left a bit to balance her wider stance
                    portraitRt.offsetMin = new Vector2(0, -60);
                    portraitRt.offsetMax = new Vector2(-40, -60);
                }'''

replacement = '''                else if (charNames[ci] == "카스미") {
                    portraitImg.sprite = Resources.Load<Sprite>("Images/Characters/kasumi_default");
                    // Shift Kasumi down, and move her to the right as requested
                    portraitRt.offsetMin = new Vector2(30, -60);
                    portraitRt.offsetMax = new Vector2(-10, -60);
                }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Kasumi position to move her to the right')
else:
    print('Target not found')
