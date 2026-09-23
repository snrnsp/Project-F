import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add fields
fields_code = '''
        [SerializeField] private TextMeshProUGUI autoButtonText;
        [SerializeField] private TextMeshProUGUI skipButtonText;
        [SerializeField] private TextMeshProUGUI backlogButtonText;
'''
text = re.sub(r'        \[SerializeField\] private TextMeshProUGUI autoButtonText;\s*', fields_code, text)

# 2. Add UpdateLanguage method
update_lang_code = '''
        public void UpdateLanguage()
        {
            if (skipButtonText == null) return;
            var lang = HalloweenVN.Core.SettingsData.Language;
            string autoOff = "AUTO";
            string autoOn = "AUTO ON";
            
            if (lang == HalloweenVN.Core.GameLanguage.Korean)
            {
                autoOff = "오토"; autoOn = "오토 중";
                skipButtonText.text = "스킵";
                backlogButtonText.text = "로그";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.English)
            {
                autoOff = "AUTO"; autoOn = "AUTO ON";
                skipButtonText.text = "SKIP";
                backlogButtonText.text = "LOG";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.Japanese)
            {
                autoOff = "オート"; autoOn = "オート中";
                skipButtonText.text = "スキップ";
                backlogButtonText.text = "ログ";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.ChineseSimplified)
            {
                autoOff = "自动"; autoOn = "自动中";
                skipButtonText.text = "跳过";
                backlogButtonText.text = "记录";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.ChineseTraditional)
            {
                autoOff = "自動"; autoOn = "自動中";
                skipButtonText.text = "跳過";
                backlogButtonText.text = "紀錄";
            }
            
            if (autoButtonText != null)
            {
                autoButtonText.text = isAutoPlay ? autoOn : autoOff;
            }
        }
        
        private void Start()
        {
            UpdateLanguage();
        }
'''

# Find OnEnable or just insert before OnEnable
if 'private void OnEnable()' in text:
    text = text.replace('private void OnEnable()', update_lang_code + '\n        private void OnEnable()')
else:
    # Just insert it before ToggleAutoPlay
    text = text.replace('public void ToggleAutoPlay()', update_lang_code + '\n        public void ToggleAutoPlay()')


# 3. Fix auto text in ToggleAutoPlay and StopAutoPlay
text = re.sub(r'autoButtonText\.text = isAutoPlay \? "AUTO ON" : "AUTO";', 'UpdateLanguage();', text)
text = re.sub(r'autoButtonText\.text = "AUTO";', 'UpdateLanguage();', text)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)
