import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        private void CreateBacklogUI()
        {
            GameObject backlogRoot = UIHelper.CreateUIObject("BacklogRoot", mainCanvas.transform);
            UIHelper.StretchFull(backlogRoot.GetComponent<RectTransform>());

            // Semi-transparent overlay
            UIHelper.AddImage(backlogRoot, new Color(0, 0, 0, 0.8f));

            // Scroll area
            GameObject scrollObj = UIHelper.CreateUIObject("ScrollView", backlogRoot.transform);'''

replacement = '''        private void CreateBacklogUI()
        {
            GameObject backlogRoot = UIHelper.CreateUIObject("BacklogRoot", mainCanvas.transform);
            UIHelper.StretchFull(backlogRoot.GetComponent<RectTransform>());
            
            // The actual panel that gets toggled
            GameObject backlogPanel = UIHelper.CreateUIObject("BacklogPanel", backlogRoot.transform);
            UIHelper.StretchFull(backlogPanel.GetComponent<RectTransform>());

            // Semi-transparent overlay
            UIHelper.AddImage(backlogPanel, new Color(0, 0, 0, 0.8f));

            // Scroll area
            GameObject scrollObj = UIHelper.CreateUIObject("ScrollView", backlogPanel.transform);'''

text = text.replace(target, replacement)

# Change title and close button parents
text = text.replace('GameObject titleObj = UIHelper.CreateUIObject("BacklogTitle", backlogRoot.transform);', 'GameObject titleObj = UIHelper.CreateUIObject("BacklogTitle", backlogPanel.transform);')
text = text.replace('var closeTuple = UIHelper.CreateButton(backlogRoot.transform,', 'var closeTuple = UIHelper.CreateButton(backlogPanel.transform,')
text = text.replace('UIHelper.SetField(backlogUiRef, "backlogPanel", backlogRoot);', 'UIHelper.SetField(backlogUiRef, "backlogPanel", backlogPanel);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated Backlog UI hierarchy')
