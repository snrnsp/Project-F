import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                // TabContainer with Mask to cut off the bottom border of the tab
                GameObject tabContainerObj = UIHelper.CreateUIObject("TabContainer", folder.transform);
                RectTransform tabContainerRt = tabContainerObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabContainerRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                // Taller tab: increased height to 55, anchored top shifted to 53 (so bottom is still at -2)
                tabContainerRt.anchoredPosition = new Vector2(0, 53);
                tabContainerRt.sizeDelta = new Vector2(-6, 55);
                
                // Add invisible image to container to receive clicks
                UIHelper.AddImage(tabContainerObj, new Color(0, 0, 0, 0));
                tabContainerObj.AddComponent<UnityEngine.UI.RectMask2D>();

                // The actual Tab Image inside the mask
                GameObject tabObj = UIHelper.CreateUIObject("Tab", tabContainerObj.transform);
                RectTransform tabRt = tabObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(tabRt);
                // Extend downwards by 10 pixels so the bottom border is drawn OUTSIDE the mask and gets clipped
                tabRt.offsetMin = new Vector2(0, -10);
                tabRt.offsetMax = new Vector2(0, 0);

                Image tabImg = UIHelper.AddImage(tabObj, folderBodyDefault);
                tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 4, Color.white, folderBorder);
                tabImg.type = Image.Type.Sliced;'''

replacement = '''                // TabContainer
                GameObject tabContainerObj = UIHelper.CreateUIObject("TabContainer", folder.transform);
                RectTransform tabContainerRt = tabContainerObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabContainerRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                // Sit flush with the body (no overlap needed because we use a seam hider)
                tabContainerRt.anchoredPosition = new Vector2(0, 55);
                tabContainerRt.sizeDelta = new Vector2(-6, 55);
                
                // Add invisible image to container to receive clicks
                UIHelper.AddImage(tabContainerObj, new Color(0, 0, 0, 0));

                // The actual Tab Image
                GameObject tabObj = UIHelper.CreateUIObject("Tab", tabContainerObj.transform);
                RectTransform tabRt = tabObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(tabRt);

                Image tabImg = UIHelper.AddImage(tabObj, folderBodyDefault);
                tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 4, Color.white, folderBorder);
                tabImg.type = Image.Type.Sliced;

                // ===== Seam Hider =====
                // A solid block of color that covers the Tab's bottom border AND the Body's top border
                GameObject seamObj = UIHelper.CreateUIObject("Seam", tabContainerObj.transform);
                RectTransform seamRt = seamObj.GetComponent<RectTransform>();
                // Anchor to the bottom of the TabContainer
                UIHelper.SetAnchors(seamRt, new Vector2(0, 0), new Vector2(1, 0), new Vector2(0.5f, 0.5f));
                // Height is 12px to safely cover both 4px borders with some padding
                seamRt.sizeDelta = new Vector2(-8, 12);
                // Center it on the joint
                seamRt.anchoredPosition = new Vector2(0, 0);
                
                Image seamImg = UIHelper.AddImage(seamObj, folderBodyDefault);
                // No sprite, just a solid block of color!'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Replaced mask approach with a robust Seam Hider block')
else:
    print('Target not found')
