import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_render = '''            mainCanvas.renderMode = RenderMode.ScreenSpaceCamera;
            mainCanvas.worldCamera = cam;
            mainCanvas.planeDistance = 100f; // Put UI in front of camera'''

new_render = '''            mainCanvas.renderMode = RenderMode.ScreenSpaceOverlay;
            // mainCanvas.worldCamera = cam;
            // mainCanvas.planeDistance = 100f; // ScreenSpaceOverlay avoids 1-pixel rounding gaps'''

if old_render in content:
    content = content.replace(old_render, new_render)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed RenderMode.")
else:
    print("Could not find RenderMode.")
