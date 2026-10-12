import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Add fields
for i, line in enumerate(lines):
    if 'private Canvas mainCanvas;' in line:
        lines.insert(i, '        private GameObject splashRoot;\n        private CanvasGroup splashCanvasGroup;\n')
        break

# 2. Add CreateSplashUI call in Awake
for i, line in enumerate(lines):
    if 'CreateScreenTransition();' in line:
        lines.insert(i+1, '            CreateSplashUI();\n')
        break

# 3. Add PlaySplashSequence call in Start
for i, line in enumerate(lines):
    if 'if (GameManager.Instance != null)' in line:
        lines.insert(i, '            StartCoroutine(PlaySplashSequence());\n')
        break

# 4. Add methods
splash_methods = '''
        private void CreateSplashUI()
        {
            splashRoot = UIHelper.CreateUIObject("SplashScreen", mainCanvas.transform);
            UIHelper.StretchFull(splashRoot.GetComponent<RectTransform>());
            
            // White background for the logo
            UnityEngine.UI.Image bg = UIHelper.AddImage(splashRoot, Color.white);
            
            GameObject logoObj = UIHelper.CreateUIObject("StudioLogo", splashRoot.transform);
            RectTransform logoRt = logoObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(logoRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            logoRt.sizeDelta = new Vector2(800, 800);
            
            UnityEngine.UI.Image logoImg = UIHelper.AddImage(logoObj, Color.white);
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
            }

            // CanvasGroup to fade logo independently
            logoObj.AddComponent<CanvasGroup>().alpha = 0f;

            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 1f; // Background starts fully opaque
            splashCanvasGroup.blocksRaycasts = true;
            
            splashRoot.SetActive(false);
        }

        private System.Collections.IEnumerator PlaySplashSequence()
        {
            yield return null; 

            // 1. Hide Lobby while Splash is playing
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);

            splashRoot.SetActive(true);
            splashRoot.transform.SetAsLastSibling(); 
            
            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
            // 2. Fade Logo In (Background is already white)
            float fadeTime = 1.0f;
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                logoCG.alpha = t / fadeTime;
                yield return null;
            }
            logoCG.alpha = 1f;
            
            // 3. Hold
            yield return new UnityEngine.WaitForSecondsRealtime(2.0f);
            
            // 4. Fade Logo Out
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                logoCG.alpha = 1f - (t / fadeTime);
                yield return null;
            }
            logoCG.alpha = 0f;
            
            // 5. Briefly hold white screen
            yield return new UnityEngine.WaitForSecondsRealtime(0.5f);
            
            // Enable Lobby behind the white screen
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);
            
            // Fade the white background out to reveal Lobby
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                splashCanvasGroup.alpha = 1f - (t / fadeTime);
                yield return null;
            }
            splashCanvasGroup.alpha = 0f;
            
            splashRoot.SetActive(false);
            splashCanvasGroup.blocksRaycasts = false;
        }
'''

for i, line in enumerate(lines):
    if 'private void CreateLobbyUI()' in line:
        lines.insert(i, splash_methods)
        break

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("Restored Splash Screen UI.")
