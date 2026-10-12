import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_layout = '''            // Layout Group for the Panel
            VerticalLayoutGroup vlg = panel.AddComponent<VerticalLayoutGroup>();
            vlg.padding = new RectOffset(40, 40, 30, 30);
            vlg.spacing = 8;
            vlg.childControlWidth = true;
            vlg.childControlHeight = false;
            vlg.childForceExpandWidth = true;
            vlg.childForceExpandHeight = false;
            vlg.childAlignment = TextAnchor.UpperCenter;'''

new_layout = '''            // Layout Group for the Panel
            VerticalLayoutGroup vlg = panel.AddComponent<VerticalLayoutGroup>();
            vlg.padding = new RectOffset(40, 40, 40, 40);
            vlg.spacing = 15; // Increased spacing for more breathing room
            vlg.childControlWidth = true;
            vlg.childControlHeight = false;
            vlg.childForceExpandWidth = true;
            vlg.childForceExpandHeight = false;
            vlg.childAlignment = TextAnchor.MiddleCenter; // Centered vertically!'''

if old_layout in content:
    content = content.replace(old_layout, new_layout)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Updated VerticalLayoutGroup to MiddleCenter and increased spacing.")
else:
    print("Could not find the layout group setup.")
