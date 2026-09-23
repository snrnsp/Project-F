import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Change img.color = Color.black; to semi-transparent
text = text.replace('img.color = Color.black; // Solid black background for centered monologues', 'img.color = new Color(0, 0, 0, 0.75f); // Semi-transparent black background')

# Change usePanel logic
# bool hasBackground = (backgroundImage != null && backgroundImage.sprite != null && backgroundImage.color.a > 0.01f);
# bool usePanel = !isNarrator || hasBackground;
# We want usePanel = !isNarrator ALWAYS.
old_logic = '''bool hasBackground = (backgroundImage != null && backgroundImage.sprite != null && backgroundImage.color.a > 0.01f);
            bool usePanel = !isNarrator || hasBackground;'''
new_logic = '''bool usePanel = !isNarrator;'''
text = text.replace(old_logic, new_logic)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueUI to always use centered narrator text over semi-transparent background')
