import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''            // Warning panel
            GameObject panel = new GameObject("WarningPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.anchorMin = new Vector2(0.5f, 0.5f);
            panelRt.anchorMax = new Vector2(0.5f, 0.5f);
            panelRt.sizeDelta = new Vector2(820, 500);
            Image panelImg = panel.AddComponent<Image>();
            panelImg.color = new Color32(25, 20, 35, 255);'''

replacement1 = '''            // Warning panel
            GameObject panel = new GameObject("WarningPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.anchorMin = new Vector2(0.5f, 0.5f);
            panelRt.anchorMax = new Vector2(0.5f, 0.5f);
            panelRt.sizeDelta = new Vector2(820, 500);
            Image panelImg = panel.AddComponent<Image>();
            panelImg.type = Image.Type.Sliced;
            panelImg.sprite = CreateRoundedRectSprite(16, 2, new Color32(25, 20, 35, 255), new Color32(255, 180, 50, 255));'''

target2 = '''        private void HandlePhaseChanged(GamePhase phase)'''
replacement2 = '''        private Sprite CreateRoundedRectSprite(int radius, int borderSize, Color32 bgColor, Color32 borderColor)
        {
            int size = radius * 2 + borderSize * 2 + 4; // Add a bit of padding for safe slicing
            int centerStart = radius + borderSize;
            int centerEnd = centerStart + 3;
            
            Texture2D tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
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

        private void HandlePhaseChanged(GamePhase phase)'''

if target1 in text and target2 in text:
    text = text.replace(target1, replacement1)
    text = text.replace(target2, replacement2)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated LobbyUI with rounded warning panel')
else:
    print('Target strings not found in LobbyUI.cs')
