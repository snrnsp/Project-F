import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''            Button btn = narratorObj\.AddComponent<Button>\(\);\r?\n\s*btn\.transition = Selectable\.Transition\.None;\r?\n\s*btn\.onClick\.AddListener\(OnClick\);'''

replacement = r'''            Button btn = narratorObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.None;
            // Use PointerDown to prevent drag threshold from ignoring clicks
            UnityEngine.EventSystems.EventTrigger nTrigger = narratorObj.AddComponent<UnityEngine.EventSystems.EventTrigger>();
            var nEntry = new UnityEngine.EventSystems.EventTrigger.Entry { eventID = UnityEngine.EventSystems.EventTriggerType.PointerDown };
            nEntry.callback.AddListener((data) => OnClick());
            nTrigger.triggers.Add(nEntry);'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed narrator panel OnClick!")
else:
    print("Failed to match narrator panel!")
