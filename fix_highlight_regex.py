import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'if \(string\.IsNullOrWhiteSpace\(speaker\)\)\s*\{\s*//[^\n]*\n\s*foreach \(var kvp in _activeSpeakerPositions\)\s*\{\s*DimCharacterImage\(GetCharacterImage\(kvp\.Value\), true, instant\);\s*\}\s*return;\s*\}'

replacement = r'''if (string.IsNullOrWhiteSpace(speaker))
            {
                // Narrator -> all active characters are dimmed
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), false, instant);
                }
                return;
            }'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed DialogueUI.cs speaker highlight with regex!")
else:
    print("Regex failed to match!")
