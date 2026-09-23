import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                // TabContainer with Mask to cut off the bottom border of the tab
                GameObject tabContainerObj = UIHelper.CreateUIObject("TabContainer", folder.transform);
                RectTransform tabContainerRt = tabContainerObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabContainerRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                // Move down by 2 pixels so the bottom edge overlaps and hides the Body's top border
                tabContainerRt.anchoredPosition = new Vector2(0, 33);
                tabContainerRt.sizeDelta = new Vector2(-6, 35);
                
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
                tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, Color.white, folderBorder);
                tabImg.type = Image.Type.Sliced;

                // Tab text
                GameObject tabTextObj = UIHelper.CreateUIObject("Text", tabObj.transform);
                UIHelper.StretchFull(tabTextObj.GetComponent<RectTransform>());
                TextMeshProUGUI tabText = UIHelper.AddText(tabTextObj, charNames[ci], new Color32(60, 40, 20, 255), 18, TextAlignmentOptions.Center);
                tabText.fontStyle = FontStyles.Bold;'''

replacement = '''                // TabContainer with Mask to cut off the bottom border of the tab
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
                tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, Color.white, folderBorder);
                tabImg.type = Image.Type.Sliced;

                // Tab text - Make it a child of TabContainer so it perfectly centers in the visible area!
                GameObject tabTextObj = UIHelper.CreateUIObject("Text", tabContainerObj.transform);
                RectTransform textRt = tabTextObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(textRt);
                // Shift text up slightly within the container so it's vertically balanced
                textRt.offsetMin = new Vector2(0, 5);
                textRt.offsetMax = new Vector2(0, 5);
                TextMeshProUGUI tabText = UIHelper.AddText(tabTextObj, charNames[ci], new Color32(60, 40, 20, 255), 18, TextAlignmentOptions.Center);
                tabText.fontStyle = FontStyles.Bold;'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Tab height and text position')
else:
    print('Target not found')
