import sys
sys.stdout.reconfigure(encoding='utf-8')

# Update HalloweenUIBuilder.cs
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

# Fix ShadowBox
target_shadow = '''            shadowRt.offsetMin = new Vector2(160, 0);
            shadowRt.offsetMax = new Vector2(-100, -170);'''
rep_shadow = '''            shadowRt.offsetMin = new Vector2(240, 70);
            shadowRt.offsetMax = new Vector2(-200, -130);'''
text = text.replace(target_shadow.replace('\n', '\r\n'), rep_shadow.replace('\n', '\r\n'))
text = text.replace(target_shadow, rep_shadow)

# Fix Base Folder
target_folder = '''                folderRt.offsetMin = new Vector2(150 + xShift, 10 + yShift);
                folderRt.offsetMax = new Vector2(-150 + xShift, -220 + yShift);'''
rep_folder = '''                folderRt.offsetMin = new Vector2(250 + xShift, 80 + yShift);
                folderRt.offsetMax = new Vector2(-250 + xShift, -180 + yShift);'''
text = text.replace(target_folder.replace('\n', '\r\n'), rep_folder.replace('\n', '\r\n'))
text = text.replace(target_folder, rep_folder)

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text)


# Update ExtraUI.cs
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text2 = f.read()

target_extra = '''                    rt.offsetMin = new Vector2(150, 10);
                    rt.offsetMax = new Vector2(-150, -220);'''
rep_extra = '''                    rt.offsetMin = new Vector2(250, 80);
                    rt.offsetMax = new Vector2(-250, -180);'''

text2 = text2.replace(target_extra.replace('\n', '\r\n'), rep_extra.replace('\n', '\r\n'))
text2 = text2.replace(target_extra, rep_extra)

with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text2)

print('Folder sizes reduced and moved up')
