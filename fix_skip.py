import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''        public void SkipTyping\(\)\r?\n\s*\{\r?\n\s*Debug\.Log\(\$"\[DialogueUI\] SkipTyping called\."\);\r?\n\s*if \(typingCoroutine != null\) StopCoroutine\(typingCoroutine\);\r?\n\s*if \(dialogueText != null\) dialogueText\.maxVisibleCharacters = 99999;\r?\n\s*if \(narratorText != null\) narratorText\.maxVisibleCharacters = 99999;\r?\n\s*isTyping = false;\r?\n\s*_typingEndTime = Time\.unscaledTime;'''

replacement = r'''        public void SkipTyping()
        {
            Debug.Log($"[DialogueUI] SkipTyping called.");
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            if (dialogueText != null) dialogueText.maxVisibleCharacters = 99999;
            if (narratorText != null) narratorText.maxVisibleCharacters = 99999;
            isTyping = false;
            _typingEndTime = 0f; // Allow immediate next click when manually skipped'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed SkipTyping!")
else:
    print("Failed to match pattern!")
