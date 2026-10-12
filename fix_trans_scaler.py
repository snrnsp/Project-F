import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'(CanvasScaler scaler = transObj\.AddComponent<CanvasScaler>\(\);\s*scaler\.uiScaleMode = CanvasScaler\.ScaleMode\.ScaleWithScreenSize;\s*scaler\.referenceResolution = new Vector2\(1920, 1080\);)'

replacement = r'\1\n            scaler.screenMatchMode = CanvasScaler.ScreenMatchMode.Expand;'

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed ScreenTransition CanvasScaler!")
else:
    print("Failed to match ScreenTransition CanvasScaler!")
