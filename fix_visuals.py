import codecs

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

target = '''            if (!string.IsNullOrEmpty(node.characterSprite))
            {
                requested[0] = null; requested[1] = node.characterSprite; requested[2] = null;
            }'''

replacement = '''            if (!string.IsNullOrEmpty(node.characterSprite))
            {
                requested[0] = null; requested[1] = node.characterSprite; requested[2] = null;
            }

            bool noSpritesRequested = string.IsNullOrEmpty(requested[0]) && string.IsNullOrEmpty(requested[1]) && string.IsNullOrEmpty(requested[2]);
            bool bgChanging = !string.IsNullOrEmpty(node.backgroundSprite) && node.backgroundSprite != _currentBgPath;

            if (string.IsNullOrWhiteSpace(node.speaker) && noSpritesRequested && !bgChanging && !_freshDialogue)
            {
                bool instantHighlight = instant || (wasNarrator && usePanelNow);
                UpdateSpeakerHighlight(node.speaker, instantHighlight);
                UpdateBackground(node.backgroundSprite);
                return;
            }'''

if target in content:
    content = content.replace(target, replacement)
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Injected early return logic successfully!")
else:
    print("Could not find target!")
