import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'while (visibleCount <= totalVisibleChars && target != null)' in line:
        start_idx = i
    if 'isTyping = false;' in line and start_idx != -1:
        end_idx = i
        break

print(f"Start: {start_idx}, End: {end_idx}")

new_code = '''            float nextCharTime = Time.unscaledTime;
            while (visibleCount <= totalVisibleChars && target != null)
            {
                target.maxVisibleCharacters = visibleCount;
                
                if (visibleCount > 0 && visibleCount <= target.textInfo.characterCount)
                {
                    char c = target.textInfo.characterInfo[visibleCount - 1].character;
                    if (c == '\\n')
                    {
                        yield return _cachedNewlineDelay;
                        nextCharTime = Time.unscaledTime;
                    }
                }
                
                visibleCount++;
                
                nextCharTime += SettingsData.TextSpeed;
                while (Time.unscaledTime < nextCharTime)
                {
                    yield return null;
                }
            }
'''

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx] = [new_code]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Replaced successfully.")
else:
    print("Could not find the block.")
