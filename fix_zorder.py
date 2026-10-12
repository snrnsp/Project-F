import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the Dropdown and Help panels
start_drop = content.find('            // Dropdown Panel')
end_drop = content.find('            // 〓〓〓 4. Font Style')

if start_drop == -1 or end_drop == -1:
    print("Could not find dropdown block.")
    sys.exit(1)

dropdown_block = content[start_drop:end_drop]

# Remove it from current position
content = content[:start_drop] + content[end_drop:]

# Insert it at the end, before Attach SettingsUI
attach_marker = '            // Attach SettingsUI'
attach_idx = content.find(attach_marker)

if attach_idx == -1:
    print("Could not find attach marker.")
    sys.exit(1)

content = content[:attach_idx] + dropdown_block + '\n' + content[attach_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Moved dropdown and help panel to the end for Z-order fix.")
