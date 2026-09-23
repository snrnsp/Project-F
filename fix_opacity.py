import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenTheme.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'public static readonly Color PanelBackground = new Color32\(30, 15, 45, 220\);', r'public static readonly Color PanelBackground = new Color32(30, 15, 45, 255);', text)
text = re.sub(r'public static readonly Color ButtonNormal = new Color32\(50, 25, 70, 230\);', r'public static readonly Color ButtonNormal = new Color32(50, 25, 70, 255);', text)
text = re.sub(r'public static readonly Color SlotEmpty = new Color32\(35, 30, 50, 180\);', r'public static readonly Color SlotEmpty = new Color32(35, 30, 50, 255);', text)
text = re.sub(r'public static readonly Color SlotFilled = new Color32\(50, 80, 50, 200\);', r'public static readonly Color SlotFilled = new Color32(50, 80, 50, 255);', text)
text = re.sub(r'public static readonly Color SlotHighlight = new Color32\(180, 100, 20, 200\);', r'public static readonly Color SlotHighlight = new Color32(180, 100, 20, 255);', text)
text = re.sub(r'public static readonly Color InventoryBg = new Color32\(20, 12, 30, 230\);', r'public static readonly Color InventoryBg = new Color32(20, 12, 30, 255);', text)
text = re.sub(r'public static readonly Color ButtonDisabled = new Color32\(40, 40, 40, 180\);', r'public static readonly Color ButtonDisabled = new Color32(40, 40, 40, 255);', text)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated opacity to 100% in HalloweenTheme')
