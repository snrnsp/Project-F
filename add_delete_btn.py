import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // Close Button
            var closeTuple = CreateLegacyButton(panel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 40);

            // Attach SettingsUI'''

replacement = '''            // Delete Data Button
            var deleteTuple = CreateLegacyButton(panel.transform, "데이터 삭제", 200, 50, new Color32(180, 40, 40, 255));
            RectTransform deleteRt = deleteTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(deleteRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            deleteRt.anchoredPosition = new Vector2(-120, 40);

            // Close Button
            var closeTuple = CreateLegacyButton(panel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(120, 40);

            // Attach SettingsUI'''

text = text.replace(target, replacement)

target2 = '''            UIHelper.SetField(settingsUi, "closeButton", closeTuple.btn);
            UIHelper.SetField(settingsUi, "previewTextLabel", previewText);
            UIHelper.SetField(settingsUi, "titleTextLabel", titleText);
            UIHelper.SetField(settingsUi, "closeButtonText", closeTuple.text);'''

replacement2 = '''            UIHelper.SetField(settingsUi, "closeButton", closeTuple.btn);
            UIHelper.SetField(settingsUi, "deleteDataButton", deleteTuple.btn);
            UIHelper.SetField(settingsUi, "previewTextLabel", previewText);
            UIHelper.SetField(settingsUi, "titleTextLabel", titleText);
            UIHelper.SetField(settingsUi, "closeButtonText", closeTuple.text);
            UIHelper.SetField(settingsUi, "deleteDataButtonText", deleteTuple.text);'''

text = text.replace(target2, replacement2)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated HalloweenUIBuilder.cs to inject Delete Data button')
