import re

with open('Assets/Scripts/Effects/ScreenEffects.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace(
    "public Coroutine ShakeCamera(float duration = 0.5f, float magnitude = 10f)\n        {",
    "public Coroutine ShakeCamera(float duration = 0.5f, float magnitude = 10f)\n        {\n            if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects) return null;"
)

content = content.replace(
    "public Coroutine FlashScreen(Color color, float duration = 0.5f)\n        {",
    "public Coroutine FlashScreen(Color color, float duration = 0.5f)\n        {\n            if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects) return null;"
)

with open('Assets/Scripts/Effects/ScreenEffects.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Patched ScreenEffects.cs")
