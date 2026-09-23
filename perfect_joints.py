import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                // ===== Body (main content area) =====
                // Create body FIRST so it renders behind the tab
                GameObject bodyObj = UIHelper.CreateUIObject("Body", folder.transform);
                RectTransform bodyRt = bodyObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(bodyRt);

                Image bodyImg = UIHelper.AddImage(bodyObj, folderBodyDefault);
                bodyImg.sprite = UIHelper.CreateRoundedRectSprite(10, 4, Color.white, folderBorder);
                bodyImg.type = Image.Type.Sliced;

                // ===== Tab (upper protruding part of the folder) =====
                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                float tabRight = tabFraction * (ci + 1);

                // TabContainer
                GameObject tabContainerObj = UIHelper.CreateUIObject("TabContainer", folder.transform);
                RectTransform tabContainerRt = tabContainerObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabContainerRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                
                // Determine horizontal offsets for flush edges on first and last tabs
                float leftOffset = (ci == 0) ? 0f : 3f;
                float rightOffset = (ci == folderCount - 1) ? 0f : -3f;
                
                // Sit flush with the body vertically
                tabContainerRt.anchoredPosition = new Vector2(0, 55);
                tabContainerRt.offsetMin = new Vector2(leftOffset, 0);
                tabContainerRt.offsetMax = new Vector2(rightOffset, 55);
                
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
                // Span the FULL width of the tab container to cover the rounded corners completely!
                seamRt.sizeDelta = new Vector2(0, 12);
                // Center it on the joint
                seamRt.anchoredPosition = new Vector2(0, 0);
                
                Image seamImg = UIHelper.AddImage(seamObj, folderBodyDefault);

                // Add straight border patches to restore the vertical borders that were covered by the full-width seam hider!
                GameObject seamLeftObj = UIHelper.CreateUIObject("SeamLeft", seamObj.transform);
                RectTransform seamLeftRt = seamLeftObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(seamLeftRt, new Vector2(0, 0), new Vector2(0, 1), new Vector2(0, 0.5f));
                seamLeftRt.sizeDelta = new Vector2(4, 0);
                UIHelper.AddImage(seamLeftObj, folderBorder);

                GameObject seamRightObj = UIHelper.CreateUIObject("SeamRight", seamObj.transform);
                RectTransform seamRightRt = seamRightObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(seamRightRt, new Vector2(1, 0), new Vector2(1, 1), new Vector2(1, 0.5f));
                seamRightRt.sizeDelta = new Vector2(4, 0);
                UIHelper.AddImage(seamRightObj, folderBorder);'''

replacement = '''                // ===== Body (main content area) =====
                // Create body FIRST so it renders behind the tab
                GameObject bodyObj = UIHelper.CreateUIObject("Body", folder.transform);
                RectTransform bodyRt = bodyObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(bodyRt);

                Image bodyImg = UIHelper.AddImage(bodyObj, folderBodyDefault);
                // Body has square top corners so it perfectly aligns with the tabs!
                bodyImg.sprite = UIHelper.CreateCustomRoundedRectSprite(10, 4, Color.white, folderBorder, false, false, true, true);
                bodyImg.type = Image.Type.Sliced;

                // ===== Tab (upper protruding part of the folder) =====
                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                float tabRight = tabFraction * (ci + 1);

                // TabContainer
                GameObject tabContainerObj = UIHelper.CreateUIObject("TabContainer", folder.transform);
                RectTransform tabContainerRt = tabContainerObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabContainerRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                
                // Determine horizontal offsets for flush edges on first and last tabs
                float leftOffset = (ci == 0) ? 0f : 3f;
                float rightOffset = (ci == folderCount - 1) ? 0f : -3f;
                
                // Sit flush with the body vertically
                tabContainerRt.anchoredPosition = new Vector2(0, 55);
                tabContainerRt.offsetMin = new Vector2(leftOffset, 0);
                tabContainerRt.offsetMax = new Vector2(rightOffset, 55);
                
                // Add invisible image to container to receive clicks
                UIHelper.AddImage(tabContainerObj, new Color(0, 0, 0, 0));

                // The actual Tab Image
                GameObject tabObj = UIHelper.CreateUIObject("Tab", tabContainerObj.transform);
                RectTransform tabRt = tabObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(tabRt);

                Image tabImg = UIHelper.AddImage(tabObj, folderBodyDefault);
                // Tab has square bottom corners to seamlessly connect to the Body!
                tabImg.sprite = UIHelper.CreateCustomRoundedRectSprite(8, 4, Color.white, folderBorder, true, true, false, false);
                tabImg.type = Image.Type.Sliced;

                // ===== Seam Hider =====
                // A solid block of color that covers the Tab's bottom horizontal border AND the Body's top horizontal border.
                GameObject seamObj = UIHelper.CreateUIObject("Seam", tabContainerObj.transform);
                RectTransform seamRt = seamObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(seamRt, new Vector2(0, 0), new Vector2(1, 0), new Vector2(0.5f, 0.5f));
                // Inset by 4px on both sides so we DO NOT cover the straight vertical borders!
                seamRt.offsetMin = new Vector2(4, -6);
                seamRt.offsetMax = new Vector2(-4, 6);
                
                Image seamImg = UIHelper.AddImage(seamObj, folderBodyDefault);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated to use perfectly square joints and simple seam hider')
else:
    print('Target not found')
