import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''            UIHelper.SetField(langUi, "panelRoot", langRoot);
            UIHelper.SetField(langUi, "languageButtons", langBtns);
            UIHelper.SetField(langUi, "closeButton", closeTuple.btn);'''

# Note: The title object is called titleObj and its text is the TextMeshProUGUI returned from AddText.
# Wait, did we save the returned titleTxt?
# Let's check HalloweenUIBuilder.cs for the Title creation.
# It is: TextMeshProUGUI titleTxt = UIHelper.AddText(titleObj, ...);
# Let's hope it is named titleTxt! I will just use titleObj.GetComponent<TextMeshProUGUI>()

replacement = '''            UIHelper.SetField(langUi, "panelRoot", langRoot);
            UIHelper.SetField(langUi, "languageButtons", langBtns);
            UIHelper.SetField(langUi, "closeButton", closeTuple.btn);
            UIHelper.SetField(langUi, "titleText", titleObj.GetComponent<TextMeshProUGUI>());
            UIHelper.SetField(langUi, "closeText", closeTuple.txt);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated HalloweenUIBuilder.cs to bind the localized texts')
else:
    print('Target not found')
