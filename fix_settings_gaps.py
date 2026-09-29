import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []

for i, line in enumerate(lines):
    # Fix slider Y offset
    if 'Slider textSpeedSlider = CreateSettingsSlider' in line:
        line = line.replace('yPos - 30', 'yPos - 45')
    elif 'Slider autoPlaySlider = CreateSettingsSlider' in line:
        line = line.replace('yPos - 30', 'yPos - 45')
    elif 'Slider opacitySlider = CreateSettingsSlider' in line:
        line = line.replace('yPos - 30', 'yPos - 45')
        
    # Fix section gaps
    elif 'yPos -= 65;' in line and 'Preview Text' in lines[i-1]:
        line = line.replace('yPos -= 65', 'yPos -= 80')
    elif 'yPos -= 60;' in line and '2. Auto-play Delay' in lines[i-1]:
        line = line.replace('yPos -= 60', 'yPos -= 75')
    elif 'yPos -= 70;' in line and '3. Dialogue Box Opacity' in lines[i-1]:
        line = line.replace('yPos -= 70', 'yPos -= 85')
    elif 'yPos -= 70;' in line and '4. Skip Mode' in lines[i-1]:
        line = line.replace('yPos -= 70', 'yPos -= 85')
        
    new_lines.append(line)

content = '\n'.join(new_lines)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("HalloweenUIBuilder layout spacing fixed")
