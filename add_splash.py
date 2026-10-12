import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Add fields
for i, line in enumerate(lines):
    if 'private GameObject globalSettingsBtnObj;' in line:
        lines.insert(i+1, '        private GameObject splashRoot;\n        private CanvasGroup splashCanvasGroup;\n')
        break

# 2. Add CreateSplashUI call in Awake
for i, line in enumerate(lines):
    if 'CreateScreenTransition();' in line:
        lines.insert(i+1, '            CreateSplashUI();\n')
        break

# 3. Add PlaySplashSequence call in Start
for i, line in enumerate(lines):
    if 'GameManager.Instance.OnPhaseChanged += OnPhaseChanged;' in line:
        # After the if block
        pass
    if 'void OnDestroy()' in line:
        # Insert before OnDestroy
        lines.insert(i-1, '            StartCoroutine(PlaySplashSequence());\n')
        break

# 4. Add the methods
new_methods = '''
        private void CreateSplashUI()
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
        }

        private System.Collections.IEnumerator PlaySplashSequence()
        {
            // Wait a frame so Lobby is fully active underneath
            yield return null; 

            splashRoot.SetActive(true);
            splashRoot.transform.SetAsLastSibling(); 
            
            splashCanvasGroup.alpha = 0f;
            
            // Fade In
            float fadeTime = 1.0f;
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                splashCanvasGroup.alpha = t / fadeTime;
                yield return null;
            }
            splashCanvasGroup.alpha = 1f;
            
            // Hold
            yield return new UnityEngine.WaitForSecondsRealtime(2.0f);
            
            // Fade Out
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

lines.append(new_methods)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Added Splash Screen.")
