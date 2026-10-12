import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''        public void OnClick() { 
            if (IsModalOpen()) return;
            if (_isTransitioningScene) return; // Prevent double-trigger from UI Event System + Input System
            if (Time.unscaledTime - _lastClickTime < 0.05f) return; // Prevent double-trigger from UI Event System + Input System
            _lastClickTime = Time.unscaledTime;
            CancelAutoPlayTimer();

            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");
            if (isTyping)
            {
                SkipTyping();
            }
            else
            {


                if (DialogueManager.Instance != null)'''

new_code = '''        public void OnClick() { 
            if (IsModalOpen()) return;
            if (_isTransitioningScene) return; // Prevent double-trigger from UI Event System + Input System
            
            // 1. Prevent physical double-trigger from Unity Input System (0.05s)
            if (Time.unscaledTime - _lastClickTime < 0.05f) return; 

            // 2. Prevent accidental advance right after text finishes typing (0.1s)
            if (!isTyping && Time.unscaledTime - _typingEndTime < 0.1f) 
            {
                return; // Do NOT update _lastClickTime here, so the player isn't penalized for mashing!
            }

            // Only update last click time when the click is actually accepted!
            _lastClickTime = Time.unscaledTime;
            CancelAutoPlayTimer();

            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");
            if (isTyping)
            {
                SkipTyping();
            }
            else
            {
                if (DialogueManager.Instance != null)'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed logic flow for OnClick.")
else:
    print("Could not find the target code string.")
