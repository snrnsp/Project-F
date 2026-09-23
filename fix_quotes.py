import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

def fix_speech_style(match):
    prefix = match.group(1) # speechStyle = "
    content = match.group(2)
    suffix = match.group(3) # ",
    # Escape any unescaped quotes in content
    # First unescape all to be safe, then escape
    content = content.replace('\\"', '"').replace('"', '\\"')
    return prefix + content + suffix

# The regex looks for speechStyle = ", then grabs everything until ", at the end of the line
text = re.sub(r'(speechStyle\s*=\s*")(.*?)(",\s*\n)', fix_speech_style, text)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print("Fixed speechStyle quotes")
