import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'bool instantHighlight = instant \|\| \(wasNarrator && usePanelNow\);\s*UpdateSpeakerHighlight\(node\.speaker, instantHighlight\);\s*UpdateBackground\(node\.backgroundSprite\);\s*return;'

replacement = r'''UpdateSpeakerHighlight(node.speaker, instant || (wasNarrator && usePanelNow));
                UpdateBackground(node.backgroundSprite);
                return;'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed compilation error in DialogueUI.cs!")
else:
    print("Failed to match pattern!")
