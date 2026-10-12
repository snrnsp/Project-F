import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''            bgClick\.onClick\.AddListener\(onScreenClick\);\r?\n\s*panelClick\.onClick\.AddListener\(onScreenClick\);'''

replacement = r'''            // Use PointerDown instead of Button Click to prevent drag threshold from dropping clicks!
            UnityEngine.EventSystems.EventTrigger bgTrigger = bgImgObj.AddComponent<UnityEngine.EventSystems.EventTrigger>();
            var bgEntry = new UnityEngine.EventSystems.EventTrigger.Entry { eventID = UnityEngine.EventSystems.EventTriggerType.PointerDown };
            bgEntry.callback.AddListener((data) => onScreenClick());
            bgTrigger.triggers.Add(bgEntry);

            UnityEngine.EventSystems.EventTrigger panelTrigger = dialoguePanel.AddComponent<UnityEngine.EventSystems.EventTrigger>();
            var panelEntry = new UnityEngine.EventSystems.EventTrigger.Entry { eventID = UnityEngine.EventSystems.EventTriggerType.PointerDown };
            panelEntry.callback.AddListener((data) => onScreenClick());
            panelTrigger.triggers.Add(panelEntry);'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed HalloweenUIBuilder OnClick!")
else:
    print("Failed to match HalloweenUIBuilder!")
