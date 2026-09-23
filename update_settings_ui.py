import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """        private void ExecuteDeleteData()
        {
            // Delete all save slots (0 to 9 just in case)
            for (int i = 0; i < 10; i++)
            {
                HalloweenVN.Core.SaveManager.Delete(i);
            }
            // Delete PlayerPrefs completely
            PlayerPrefs.DeleteAll();
            PlayerPrefs.Save();
            
            // Reload the current scene to reset the game completely back to the title screen
            UnityEngine.SceneManagement.SceneManager.LoadScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name);
        }"""

replacement = """        private void ExecuteDeleteData()
        {
            var st = FindObjectOfType<HalloweenVN.UI.Theme.ScreenTransition>();
            if (st != null)
            {
                st.FadeOut(0.5f, () => 
                {
                    PerformDeleteAndReload();
                });
            }
            else
            {
                PerformDeleteAndReload();
            }
        }

        private void PerformDeleteAndReload()
        {
            for (int i = 0; i < 10; i++)
            {
                HalloweenVN.Core.SaveManager.Delete(i);
            }
            PlayerPrefs.DeleteAll();
            PlayerPrefs.SetInt("StartFaded", 1);
            PlayerPrefs.Save();
            
            UnityEngine.SceneManagement.SceneManager.LoadScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name);
        }"""

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Modified SettingsUI.cs ExecuteDeleteData")
else:
    print("Could not find target.")
