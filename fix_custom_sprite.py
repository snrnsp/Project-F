import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/UIHelper.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        public static Sprite CreateCustomRoundedRectSprite(int radius, int borderSize, Color32 bgColor, Color32 borderColor, bool tl, bool tr, bool bl, bool br)
        {
            int size = radius * 2 + borderSize * 2 + 4;
            int centerStart = radius + borderSize;
            int centerEnd = size - centerStart - 1;
            
            Texture2D tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.wrapMode = TextureWrapMode.Clamp;
            Color32 clear = new Color32(0, 0, 0, 0);
            
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    float dx = 0;
                    float dy = 0;
                    bool isCorner = false;
                    bool shouldRound = true;

                    if (x < centerStart && y < centerStart) { // Bottom-Left
                        dx = centerStart - x; dy = centerStart - y; 
                        isCorner = true; shouldRound = bl;
                    }
                    else if (x > centerEnd && y < centerStart) { // Bottom-Right
                        dx = x - centerEnd; dy = centerStart - y; 
                        isCorner = true; shouldRound = br;
                    }
                    else if (x < centerStart && y > centerEnd) { // Top-Left
                        dx = centerStart - x; dy = y - centerEnd; 
                        isCorner = true; shouldRound = tl;
                    }
                    else if (x > centerEnd && y > centerEnd) { // Top-Right
                        dx = x - centerEnd; dy = y - centerEnd; 
                        isCorner = true; shouldRound = tr;
                    }

                    float dist = 0;
                    if (isCorner) {
                        if (shouldRound) dist = Mathf.Sqrt(dx * dx + dy * dy);
                        else dist = Mathf.Max(dx, dy);
                    }
                    
                    if (dist > radius + borderSize) tex.SetPixel(x, y, clear);
                    else if (dist > radius) tex.SetPixel(x, y, borderColor);
                    else tex.SetPixel(x, y, bgColor);
                }
            }
            tex.Apply();
            return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100, 0, SpriteMeshType.FullRect, new Vector4(centerStart, centerStart, centerStart, centerStart));
        }'''

replacement = '''        public static Sprite CreateCustomRoundedRectSprite(int radius, int borderSize, Color32 bgColor, Color32 borderColor, bool tl, bool tr, bool bl, bool br)
        {
            int size = radius * 2 + borderSize * 2 + 4;
            int centerStart = radius + borderSize;
            int centerEnd = size - centerStart - 1;
            
            Texture2D tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.wrapMode = TextureWrapMode.Clamp;
            Color32 clear = new Color32(0, 0, 0, 0);
            
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    float dx = Mathf.Max(0, Mathf.Max(centerStart - x, x - centerEnd));
                    float dy = Mathf.Max(0, Mathf.Max(centerStart - y, y - centerEnd));
                    
                    bool isCorner = (dx > 0 && dy > 0);
                    bool shouldRound = true;

                    if (isCorner) {
                        if (x < centerStart && y < centerStart) shouldRound = bl;
                        else if (x > centerEnd && y < centerStart) shouldRound = br;
                        else if (x < centerStart && y > centerEnd) shouldRound = tl;
                        else if (x > centerEnd && y > centerEnd) shouldRound = tr;
                    }

                    float dist = 0;
                    if (isCorner && shouldRound) {
                        dist = Mathf.Sqrt(dx * dx + dy * dy);
                    } else {
                        // For straight edges OR square corners, use Chebyshev distance
                        dist = Mathf.Max(dx, dy);
                    }
                    
                    if (dist > radius + borderSize) tex.SetPixel(x, y, clear);
                    else if (dist > radius) tex.SetPixel(x, y, borderColor);
                    else tex.SetPixel(x, y, bgColor);
                }
            }
            tex.Apply();
            return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100, 0, SpriteMeshType.FullRect, new Vector4(centerStart, centerStart, centerStart, centerStart));
        }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Fixed CreateCustomRoundedRectSprite logic to restore straight borders')
else:
    print('Target not found')
