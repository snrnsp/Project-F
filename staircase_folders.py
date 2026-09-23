import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            for (int ci = 0; ci < folderCount; ci++)
            {
                // ===== Folder Root =====
                GameObject folder = UIHelper.CreateUIObject("Folder_" + charNames[ci], extraRoot.transform);
                RectTransform folderRt = folder.GetComponent<RectTransform>();
                UIHelper.SetAnchors(folderRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
                folderRt.offsetMin = new Vector2(150, 80);
                folderRt.offsetMax = new Vector2(-150, -150);'''

replacement = '''            for (int ci = 0; ci < folderCount; ci++)
            {
                // ===== Folder Root =====
                GameObject folder = UIHelper.CreateUIObject("Folder_" + charNames[ci], extraRoot.transform);
                
                // SetAsFirstSibling ensures that Folder 0 is front-most, Folder 1 is behind 0, etc.
                folder.transform.SetAsFirstSibling();
                
                RectTransform folderRt = folder.GetComponent<RectTransform>();
                UIHelper.SetAnchors(folderRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
                
                // Staircase Y shift: Each subsequent folder is pushed UP by 35 pixels!
                float yShift = ci * 35f;
                folderRt.offsetMin = new Vector2(150, 80 + yShift);
                folderRt.offsetMax = new Vector2(-150, -150 + yShift);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated folder root to apply staircase Y shift and SetAsFirstSibling')
else:
    print('Target not found')
