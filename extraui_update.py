import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target_field = 'private List<Button> characterTabs = new List<Button>();'
replacement_field = '''private List<Button> characterTabs = new List<Button>();
        [SerializeField] private GameObject globalSettingsButton;'''

target_show = '''        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (extraPanel != null)
            {
                extraPanel.SetActive(true);
                SelectCharacter(0); // Show Seika by default
            }
        }'''
replacement_show = '''        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (extraPanel != null)
            {
                extraPanel.SetActive(true);
                SelectCharacter(0); // Show Seika by default
            }
            if (globalSettingsButton != null) globalSettingsButton.SetActive(false);
        }'''

target_hide = '''        public void Hide()
        {
            if (extraPanel != null)
            {
                extraPanel.SetActive(false);
            }
        }'''
replacement_hide = '''        public void Hide()
        {
            if (extraPanel != null)
            {
                extraPanel.SetActive(false);
            }
            if (globalSettingsButton != null) globalSettingsButton.SetActive(true);
        }'''

text = text.replace(target_field, replacement_field).replace(target_show, replacement_show).replace(target_hide, replacement_hide)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated ExtraUI.cs to hide globalSettingsButton on Show/Hide')
