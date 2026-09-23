import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            Color c = img.color;
            c.a = 0;
            img.color = c;

            transObj.AddComponent<ScreenTransition>();"""

replacement = """            Color c = img.color;
            if (PlayerPrefs.GetInt("StartFaded", 0) == 1) {
                c.a = 1f;
                PlayerPrefs.SetInt("StartFaded", 0);
                PlayerPrefs.Save();
            } else {
                c.a = 0f;
            }
            img.color = c;

            var st = transObj.AddComponent<ScreenTransition>();
            if (c.a > 0f) {
                // Defer the fade in slightly so UI has time to build
                st.StartCoroutine(DelayedFadeIn(st));
            }"""

if target in text:
    text = text.replace(target, replacement)
    
    # Add DelayedFadeIn coroutine
    coroutine = """        private System.Collections.IEnumerator DelayedFadeIn(ScreenTransition st)
        {
            yield return null;
            st.FadeIn(0.5f);
        }
        
        private void CreateScreenTransition()"""
    text = text.replace("private void CreateScreenTransition()", coroutine)

    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Modified CreateScreenTransition")
else:
    print("Could not find target.")
