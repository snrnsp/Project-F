import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            unifiedBgRt.offsetMin = new Vector2(40, 20);
            unifiedBgRt.offsetMax = new Vector2(-20, -115); // Closed the gap between tabs and panel'''

replacement = '''            unifiedBgRt.offsetMin = new Vector2(40, 20);
            unifiedBgRt.offsetMax = new Vector2(-20, -135); // Overlap slightly with tabs'''

target2 = '''            extraUiRef = extraUi;'''
replacement2 = '''            // Move tabBar to front so it renders ON TOP of the unifiedBg panel
            tabBar.transform.SetAsLastSibling();
            extraUiRef = extraUi;'''

if target in text:
    text = text.replace(target, replacement)
    
    # We must find where tabBar is defined. Let's just put SetAsLastSibling at the very end of CreateExtraUI.
    # extraUiRef = extraUi; is around the middle. Let's find the end of CreateExtraUI.
    pass

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated offsetMax.y')
