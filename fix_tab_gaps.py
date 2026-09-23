import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // ===== Character Tabs (horizontal, below header) =====
            GameObject tabBar = UIHelper.CreateUIObject("TabBar", extraRoot.transform);
            RectTransform tabBarRt = tabBar.GetComponent<RectTransform>();
            UIHelper.SetAnchors(tabBarRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            tabBarRt.anchoredPosition = new Vector2(0, -90);
            tabBarRt.sizeDelta = new Vector2(-60, 50);'''

replacement = '''            // ===== Character Tabs (horizontal, below header) =====
            GameObject tabBar = UIHelper.CreateUIObject("TabBar", extraRoot.transform);
            RectTransform tabBarRt = tabBar.GetComponent<RectTransform>();
            UIHelper.SetAnchors(tabBarRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            tabBarRt.anchoredPosition = new Vector2(0, -90);
            tabBarRt.sizeDelta = new Vector2(-60, 50);
            
            // Add an invisible image to block raycasts from falling through the gaps between tabs!
            UIHelper.AddImage(tabBar, new Color(0,0,0,0));'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Added invisible raycast blocker to tabBar')
else:
    print('Target not found')
