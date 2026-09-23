import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                // ===== Tab (upper protruding part of the folder) =====
                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                float tabRight = tabFraction * (ci + 1);

                GameObject tabObj = UIHelper.CreateUIObject("Tab", folder.transform);
                RectTransform tabRt = tabObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                tabRt.anchoredPosition = new Vector2(0, 35);
                tabRt.sizeDelta = new Vector2(-6, 35);

                // Tab image with rounded top corners
                Image tabImg = UIHelper.AddImage(tabObj, folderBodyDefault);
                tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, Color.white, folderBorder);
                tabImg.type = Image.Type.Sliced;

                // Tab text
                GameObject tabTextObj = UIHelper.CreateUIObject("Text", tabObj.transform);
                UIHelper.StretchFull(tabTextObj.GetComponent<RectTransform>());
                TextMeshProUGUI tabText = UIHelper.AddText(tabTextObj, charNames[ci], new Color32(60, 40, 20, 255), 18, TextAlignmentOptions.Center);
                tabText.fontStyle = FontStyles.Bold;

                // Tab click handler
                Button tabBtn = tabObj.AddComponent<Button>();
                tabBtn.transition = Selectable.Transition.None;
                int capturedIndex = ci;
                tabBtn.onClick.AddListener(() => { extraUi.SelectCharacter(capturedIndex); });

                // ===== Body (main content area) =====
                GameObject bodyObj = UIHelper.CreateUIObject("Body", folder.transform);
                RectTransform bodyRt = bodyObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(bodyRt);

                Image bodyImg = UIHelper.AddImage(bodyObj, folderBodyDefault);
                bodyImg.sprite = UIHelper.CreateRoundedRectSprite(10, 2, Color.white, folderBorder);
                bodyImg.type = Image.Type.Sliced;'''

replacement = '''                // ===== Body (main content area) =====
                // Create body FIRST so it renders behind the tab
                GameObject bodyObj = UIHelper.CreateUIObject("Body", folder.transform);
                RectTransform bodyRt = bodyObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(bodyRt);

                Image bodyImg = UIHelper.AddImage(bodyObj, folderBodyDefault);
                bodyImg.sprite = UIHelper.CreateRoundedRectSprite(10, 2, Color.white, folderBorder);
                bodyImg.type = Image.Type.Sliced;

                // ===== Tab (upper protruding part of the folder) =====
                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                float tabRight = tabFraction * (ci + 1);

                // TabContainer with Mask to cut off the bottom border of the tab
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
                tabText.fontStyle = FontStyles.Bold;

                // Tab click handler goes on the Container
                Button tabBtn = tabContainerObj.AddComponent<Button>();
                tabBtn.transition = Selectable.Transition.None;
                int capturedIndex = ci;
                tabBtn.onClick.AddListener(() => { extraUi.SelectCharacter(capturedIndex); });'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated tab and body creation order and added mask')
else:
    print('Target not found')
