import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('[SerializeField] private TextMeshProUGUI autoButtonText;', '[SerializeField] private Text autoButtonText;')
text = text.replace('[SerializeField] private TextMeshProUGUI skipButtonText;', '[SerializeField] private Text skipButtonText;')
text = text.replace('[SerializeField] private TextMeshProUGUI backlogButtonText;', '[SerializeField] private Text backlogButtonText;')

# Remove enableAutoSizing and fontSizeMin/Max which belong to TMP
target_sizing = '''            if (skipButtonText != null)
            {
                skipButtonText.enableAutoSizing = true;
                skipButtonText.fontSizeMin = 10f;
                skipButtonText.fontSizeMax = 22f;
            }
            if (backlogButtonText != null)
            {
                backlogButtonText.enableAutoSizing = true;
                backlogButtonText.fontSizeMin = 10f;
                backlogButtonText.fontSizeMax = 22f;
            }
            if (autoButtonText != null)
            {
                autoButtonText.enableAutoSizing = true;
                autoButtonText.fontSizeMin = 10f;
                autoButtonText.fontSizeMax = 22f;
            }'''

rep_sizing = '''            if (skipButtonText != null) skipButtonText.resizeTextForBestFit = true;
            if (backlogButtonText != null) backlogButtonText.resizeTextForBestFit = true;
            if (autoButtonText != null) autoButtonText.resizeTextForBestFit = true;'''

text = text.replace(target_sizing, rep_sizing)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueUI.cs to use Text instead of TextMeshProUGUI for control buttons')
