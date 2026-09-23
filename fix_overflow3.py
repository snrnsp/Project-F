import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add auto-sizing setup in Start or UpdateLanguage
setup_code = '''
            if (skipButtonText != null)
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
            }
'''

text = re.sub(r'public void UpdateLanguage\(\)\s*\{', 'public void UpdateLanguage()\n        {\n' + setup_code, text)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Applied targeted auto-sizing to DialogueUI buttons')
