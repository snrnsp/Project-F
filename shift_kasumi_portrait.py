import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''            if (portrait != null)
            {
                Sprite sprite = Resources.Load<Sprite>(profile.spritePath);
                if (sprite != null) { portrait.sprite = sprite; portrait.color = Color.white; }
                else { portrait.color = new Color(0, 0, 0, 0); }
            }'''

replacement = '''            if (portrait != null)
            {
                Sprite sprite = Resources.Load<Sprite>(profile.spritePath);
                if (sprite != null) { portrait.sprite = sprite; portrait.color = Color.white; }
                else { portrait.color = new Color(0, 0, 0, 0); }
                
                RectTransform portRt = portrait.GetComponent<RectTransform>();
                if (profile.name.Contains("카스미") || profile.name.Contains("Kasumi")) {
                    // Shift Kasumi slightly to the right (move by +30px X)
                    portRt.offsetMin = new Vector2(60, 60);
                    portRt.offsetMax = new Vector2(10, -50);
                } else {
                    // Default portrait placement
                    portRt.offsetMin = new Vector2(30, 60);
                    portRt.offsetMax = new Vector2(-20, -50);
                }
            }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated ExtraUI to shift Kasumi portrait to the right')
else:
    print('Target not found')
