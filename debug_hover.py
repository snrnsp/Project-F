import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/UIHoverSound.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''        public void OnPointerClick(PointerEventData eventData)
        {
            if (!playClick || !IsInteractable()) return;
            if (eventData != null && eventData.button != PointerEventData.InputButton.Left) return;

            if (Core.AudioManager.Instance != null)
                Core.AudioManager.Instance.PlaySFX(clickSoundName);
        }'''

new_code = '''        public void OnPointerClick(PointerEventData eventData)
        {
            if (!playClick || !IsInteractable()) return;
            if (eventData != null && eventData.button != PointerEventData.InputButton.Left) return;

            if (Core.AudioManager.Instance != null) {
                Debug.Log($"[UIHoverSound] Clicked! Playing sound: {clickSoundName}");
                Core.AudioManager.Instance.PlaySFX(clickSoundName);
            }
        }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Added debug to UIHoverSound.")
else:
    print("Could not find the target code string.")
