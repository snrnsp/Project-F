import codecs

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

bad_shadow = """            shadowImg.type = Image.Type.Sliced;

            // ===== Create 6 Folder objects ====="""

good_shadow = """            shadowImg.type = Image.Type.Sliced;
            
            // Add a dummy button to block clicks from passing through to the background
            UnityEngine.UI.Button shadowBtn = shadowBox.AddComponent<UnityEngine.UI.Button>();
            shadowBtn.transition = UnityEngine.UI.Selectable.Transition.None;

            // ===== Create 6 Folder objects ====="""

bad_body = """                bodyImg.type = Image.Type.Sliced;

                // ===== Tab (upper protruding part of the folder) ====="""

good_body = """                bodyImg.type = Image.Type.Sliced;
                
                // Add a dummy button to block clicks from passing through to the background
                UnityEngine.UI.Button bodyBtn = bodyObj.AddComponent<UnityEngine.UI.Button>();
                bodyBtn.transition = UnityEngine.UI.Selectable.Transition.None;

                // ===== Tab (upper protruding part of the folder) ====="""

# Fix ShadowBox
if bad_shadow in text:
    text = text.replace(bad_shadow, good_shadow)
    print("Fixed ShadowBox clicks (LF)!")
elif bad_shadow.replace('\n', '\r\n') in text:
    text = text.replace(bad_shadow.replace('\n', '\r\n'), good_shadow.replace('\n', '\r\n'))
    print("Fixed ShadowBox clicks (CRLF)!")
else:
    print("Could not find ShadowBox block.")

# Fix Body
if bad_body in text:
    text = text.replace(bad_body, good_body)
    print("Fixed Body clicks (LF)!")
elif bad_body.replace('\n', '\r\n') in text:
    text = text.replace(bad_body.replace('\n', '\r\n'), good_body.replace('\n', '\r\n'))
    print("Fixed Body clicks (CRLF)!")
else:
    print("Could not find Body block.")

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

