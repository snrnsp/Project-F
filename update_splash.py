import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = '''        private void CreateSplashUI()
        {
            splashRoot = UIHelper.CreateUIObject("SplashScreen", mainCanvas.transform);
            UIHelper.StretchFull(splashRoot.GetComponent<RectTransform>());
            
            Image bg = UIHelper.AddImage(splashRoot, Color.black);
            
            GameObject textObj = UIHelper.CreateUIObject("StudioText", splashRoot.transform);
            RectTransform textRt = textObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(textRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            textRt.sizeDelta = new Vector2(800, 200);
            
            TextMeshProUGUI studioText = UIHelper.AddText(textObj, "Lost Studio", Color.white, 72, TextAlignmentOptions.Center);
            studioText.fontStyle = FontStyles.Bold;

            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 0f;
            splashCanvasGroup.blocksRaycasts = true; // Block clicks during splash
            
            splashRoot.SetActive(false);
        }'''

new_str = '''        private void CreateSplashUI()
        {
            splashRoot = UIHelper.CreateUIObject("SplashScreen", mainCanvas.transform);
            UIHelper.StretchFull(splashRoot.GetComponent<RectTransform>());
            
            Image bg = UIHelper.AddImage(splashRoot, Color.black);
            
            GameObject logoObj = UIHelper.CreateUIObject("StudioLogo", splashRoot.transform);
            RectTransform logoRt = logoObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(logoRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            logoRt.sizeDelta = new Vector2(600, 600);
            
            Image logoImg = UIHelper.AddImage(logoObj, Color.white);
            logoImg.preserveAspect = true;
            
            Sprite logoSprite = Resources.Load<Sprite>("Images/Logos/LOST_STUDIO_Logo");
            if (logoSprite != null)
            {
                logoImg.sprite = logoSprite;
            }
            else
            {
                Texture2D tex = Resources.Load<Texture2D>("Images/Logos/LOST_STUDIO_Logo");
                if (tex != null)
                {
                    logoImg.sprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));
                }
                else
                {
                    GameObject textObj = UIHelper.CreateUIObject("StudioText", splashRoot.transform);
                    RectTransform textRt = textObj.GetComponent<RectTransform>();
                    UIHelper.SetAnchors(textRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
                    textRt.sizeDelta = new Vector2(800, 200);
                    TextMeshProUGUI studioText = UIHelper.AddText(textObj, "Lost Studio", Color.white, 72, TextAlignmentOptions.Center);
                    studioText.fontStyle = FontStyles.Bold;
                    logoImg.enabled = false;
                }
            }

            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 0f;
            splashCanvasGroup.blocksRaycasts = true;
            
            splashRoot.SetActive(false);
        }'''

content = content.replace(old_str, new_str)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Splash Screen to use image.")
