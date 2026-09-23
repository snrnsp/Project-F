import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                int capturedIndex = ci;
                tabBtn.onClick.AddListener(() => { extraUi.SelectCharacter(capturedIndex); });
                extraUi.RegisterTab(tabBtn);
            }'''

replacement = '''                int capturedIndex = ci;
                tabBtn.onClick.AddListener(() => { extraUi.SelectCharacter(capturedIndex); });
                extraUi.RegisterTab(tabBtn);
            }
            
            // Render tabs ON TOP of the main content panel
            tabBar.transform.SetAsLastSibling();'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Added SetAsLastSibling to tabBar')
else:
    print('Target not found')
