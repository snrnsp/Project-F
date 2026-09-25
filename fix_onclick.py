import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''        public void OnClick()
        {
            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");
            if (isTyping)'''

replacement = '''        private float _lastClickTime = 0f;

        public void OnClick()
        {
            if (Time.unscaledTime - _lastClickTime < 0.05f) return; // Prevent double-trigger from UI Event System + Input System
            _lastClickTime = Time.unscaledTime;

            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");
            if (isTyping)'''

target_win = target.replace('\n', '\r\n')
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated OnClick logic (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated OnClick logic (lf)')
else:
    print('Target not found')
