import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''            Sprite bgSprite = Resources.Load<Sprite>("Images/bg_lobby");
            if (bgSprite == null)
            {
                Texture2D tex = Resources.Load<Texture2D>("Images/bg_lobby");
                if (tex != null)
                {
                    bgSprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));
                }
            }'''

new_code = '''            Sprite bgSprite = null;
            Sprite[] sprites = Resources.LoadAll<Sprite>("Images/bg_lobby");
            if (sprites != null && sprites.Length > 0)
            {
                bgSprite = sprites[0];
            }
            if (bgSprite == null)
            {
                Texture2D tex = Resources.Load<Texture2D>("Images/bg_lobby");
                if (tex != null)
                {
                    bgSprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));
                }
            }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed Sprite loading for bg_lobby.")
else:
    print("Could not find the bg_lobby loading code.")
