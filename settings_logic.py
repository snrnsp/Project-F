import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add fields
target1 = '[SerializeField] private Button closeButton;'
replacement1 = '''[SerializeField] private Button closeButton;
        [SerializeField] private Button deleteDataButton;'''
text = text.replace(target1, replacement1)

target2 = '[SerializeField] private Text closeButtonText;'
replacement2 = '''[SerializeField] private Text closeButtonText;
        [SerializeField] private Text deleteDataButtonText;'''
text = text.replace(target2, replacement2)

# Add listener
target3 = '''            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }'''
replacement3 = '''            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }
            if (deleteDataButton != null)
            {
                deleteDataButton.onClick.AddListener(OnDeleteDataClicked);
            }'''
text = text.replace(target3, replacement3)

# Add Delete method
target4 = '''        public void Hide()'''
replacement4 = '''        private void OnDeleteDataClicked()
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
        }

        public void Hide()'''
text = text.replace(target4, replacement4)

# Translation support
target5 = 'if (closeButtonText != null) closeButtonText.text = "닫기";'
replacement5 = '''if (closeButtonText != null) closeButtonText.text = "닫기";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "데이터 삭제";'''
text = text.replace(target5, replacement5)

target6 = 'if (closeButtonText != null) closeButtonText.text = "Close";'
replacement6 = '''if (closeButtonText != null) closeButtonText.text = "Close";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "Delete Data";'''
text = text.replace(target6, replacement6)

target7 = 'if (closeButtonText != null) closeButtonText.text = "閉じる";'
replacement7 = '''if (closeButtonText != null) closeButtonText.text = "閉じる";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "データ削除";'''
text = text.replace(target7, replacement7)

target8 = 'if (closeButtonText != null) closeButtonText.text = "关闭";'
replacement8 = '''if (closeButtonText != null) closeButtonText.text = "关闭";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "删除数据";'''
text = text.replace(target8, replacement8)

target9 = 'if (closeButtonText != null) closeButtonText.text = "關閉";'
replacement9 = '''if (closeButtonText != null) closeButtonText.text = "關閉";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "刪除數據";'''
text = text.replace(target9, replacement9)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated SettingsUI.cs logic with Delete Data button')
