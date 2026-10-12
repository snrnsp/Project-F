import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

insert_idx = -1
for i, line in enumerate(lines):
    if 'titleBtnRt.anchoredPosition = new Vector2(0, yPos - 45);' in line:
        insert_idx = i + 1
        break

if insert_idx != -1:
    new_code = '''
            // --- Delete Data Button ---
            var deleteDataTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.delete_data", "데이터 삭제"), 220, 44, new Color32(180, 50, 50, 255));
            RectTransform deleteDataBtnRt = deleteDataTuple.btn.GetComponent<RectTransform>();
            yPos -= 70;
            UIHelper.SetAnchors(deleteDataBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            deleteDataBtnRt.anchoredPosition = new Vector2(0, yPos - 45);
'''
    lines.insert(insert_idx, new_code)
    
    # Also attach it to SettingsUI
    for j in range(insert_idx, len(lines)):
        if 'UIHelper.SetField(settingsUi, "returnToTitleButton", titleTuple.btn);' in lines[j]:
            lines.insert(j+1, '            UIHelper.SetField(settingsUi, "deleteDataButton", deleteDataTuple.btn);\n')
            break
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Added Delete Data button to UI Builder")
else:
    print("Could not find insertion point")
