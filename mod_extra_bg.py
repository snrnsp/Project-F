import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Insert UnifiedBg right before Content area
target_content = '''            // ===== Content area ====='''
replacement_content = '''            // ===== Content area =====
            // Unified solid background for both portrait and info panel
            GameObject unifiedBgObj = UIHelper.CreateUIObject("UnifiedBg", extraRoot.transform);
            RectTransform unifiedBgRt = unifiedBgObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(unifiedBgRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
            unifiedBgRt.offsetMin = new Vector2(40, 20);
            unifiedBgRt.offsetMax = new Vector2(-20, -150);
            // Adding outline for a clean border, using the exact color requested for the body
            Image unifiedBgImg = UIHelper.AddImage(unifiedBgObj, new Color32(25, 12, 40, 255));
            Outline unifiedOutline = unifiedBgObj.AddComponent<UnityEngine.UI.Outline>();
            unifiedOutline.effectColor = HalloweenTheme.PanelBorder;
            unifiedOutline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);
'''
text = text.replace(target_content, replacement_content)

# 2. Make scrollObj transparent since we now have unifiedBg
target_scroll = '''            scrollRect.movementType = ScrollRect.MovementType.Clamped;
            UIHelper.AddImage(scrollObj, new Color32(25, 12, 40, 255));'''

replacement_scroll = '''            scrollRect.movementType = ScrollRect.MovementType.Clamped;
            UIHelper.AddImage(scrollObj, new Color(0, 0, 0, 0));'''

text = text.replace(target_scroll, replacement_scroll)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added unified background to ExtraUI')
