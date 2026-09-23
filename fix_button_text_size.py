import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            if (skipButtonText != null) skipButtonText.resizeTextForBestFit = true;
            if (backlogButtonText != null) backlogButtonText.resizeTextForBestFit = true;
            if (autoButtonText != null) autoButtonText.resizeTextForBestFit = true;'''

replacement = '''            if (skipButtonText != null) skipButtonText.resizeTextForBestFit = false;
            if (backlogButtonText != null) backlogButtonText.resizeTextForBestFit = false;
            if (autoButtonText != null) autoButtonText.resizeTextForBestFit = false;
            
            if (skipButtonText != null) skipButtonText.fontSize = 20;
            if (backlogButtonText != null) backlogButtonText.fontSize = 20;
            if (autoButtonText != null) autoButtonText.fontSize = 20;'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Disabled resizeTextForBestFit and fixed font size to 20')
else:
    print('Target not found')
