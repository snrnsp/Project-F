import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_highlight = '''        private void UpdateSpeakerHighlight(string speaker, bool instant = false)
        {
            if (string.IsNullOrWhiteSpace(speaker))
            {
                // Narrator ? all active characters stay bright
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), true, instant);
                }
                return;
            }'''

new_highlight = '''        private void UpdateSpeakerHighlight(string speaker, bool instant = false)
        {
            if (string.IsNullOrWhiteSpace(speaker))
            {
                // Narrator -> all characters should be dimmed
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), false, instant);
                }
                return;
            }'''

if old_highlight in content:
    content = content.replace(old_highlight, new_highlight)
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed DialogueUI.cs speaker highlight!")
else:
    print("Could not find old_highlight in DialogueUI.cs")
