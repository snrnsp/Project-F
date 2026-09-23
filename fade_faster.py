import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''        private IEnumerator DelayedNewGameRoutine(Theme.ScreenTransition transition, GameObject popupOverlay)
        {
            float fadeTime = 2.2f; // 0.3s faster than previous 2.5f'''

replacement = '''        private IEnumerator DelayedNewGameRoutine(Theme.ScreenTransition transition, GameObject popupOverlay)
        {
            float fadeTime = 1.7f; // 0.5s faster than previous 2.2f'''

if target in text:
    text = text.replace(target, replacement)
    
    # Also let's check the fade in
    target2 = 'transition.FadeIn(1.0f);'
    replacement2 = 'transition.FadeIn(0.5f); // Fade in faster as well'
    text = text.replace(target2, replacement2)

    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated fade time to be 0.5s faster')
else:
    print('Target not found')
