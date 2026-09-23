import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/UIHelper.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        public static Image AddImage(GameObject obj, Color color, Sprite sprite = null)
        {'''
replacement = '''        public static Sprite CreateRoundedRectSprite(int radius, int borderSize, Color32 bgColor, Color32 borderColor)
        {
            int size = radius * 2 + borderSize * 2 + 4; // Add a bit of padding for safe slicing
            int centerStart = radius + borderSize;
            int centerEnd = centerStart + 3;
            
            Texture2D tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.wrapMode = TextureWrapMode.Clamp;
            Color32 clear = new Color32(0, 0, 0, 0);
            
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    float dx = Mathf.Max(0, Mathf.Max(centerStart - x, x - centerEnd));
                    float dy = Mathf.Max(0, Mathf.Max(centerStart - y, y - centerEnd));
                    float dist = Mathf.Sqrt(dx * dx + dy * dy);
                    
                    if (dist > radius + borderSize) tex.SetPixel(x, y, clear);
                    else if (dist > radius) tex.SetPixel(x, y, borderColor);
                    else tex.SetPixel(x, y, bgColor);
                }
            }
            tex.Apply();
            return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100, 0, SpriteMeshType.FullRect, new Vector4(centerStart, centerStart, centerStart, centerStart));
        }

        public static Image AddImage(GameObject obj, Color color, Sprite sprite = null)
        {'''

text = text.replace(target, replacement)
with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added CreateRoundedRectSprite to UIHelper')
