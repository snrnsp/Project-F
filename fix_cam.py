import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_cam = '''                GameObject camObj = new GameObject("Main Camera");
                camObj.tag = "MainCamera";
                cam = camObj.AddComponent<Camera>();
                cam.clearFlags = CameraClearFlags.SolidColor;
                cam.backgroundColor = Color.black;'''

new_cam = '''                GameObject camObj = new GameObject("Main Camera");
                camObj.tag = "MainCamera";
                cam = camObj.AddComponent<Camera>();
                cam.clearFlags = CameraClearFlags.SolidColor;
                cam.backgroundColor = Color.black;
                cam.orthographic = true; // Fix sub-pixel gaps in ScreenSpaceCamera'''

if old_cam in content:
    content = content.replace(old_cam, new_cam)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed camera orthographic.")
else:
    print("Could not find the camera setup.")
