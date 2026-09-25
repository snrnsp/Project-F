import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

# Add _fadeCoroutines
target_dict = 'private Dictionary<Image, Coroutine> _highlightCoroutines = new Dictionary<Image, Coroutine>();'
replacement_dict = 'private Dictionary<Image, Coroutine> _highlightCoroutines = new Dictionary<Image, Coroutine>();\n        private Dictionary<Image, Coroutine> _fadeCoroutines = new Dictionary<Image, Coroutine>();'

# FadeInCharacter
target_fadein1 = '''        // ═══════════ Character FadeIn / FadeOut ═══════════
        private IEnumerator FadeInCharacter(Image img)'''
replacement_fadein1 = '''        // ═══════════ Character FadeIn / FadeOut ═══════════
        private void StartFadeIn(Image img)
        {
            if (img == null) return;
            if (_fadeCoroutines.ContainsKey(img) && _fadeCoroutines[img] != null) StopCoroutine(_fadeCoroutines[img]);
            _fadeCoroutines[img] = StartCoroutine(FadeInCharacter(img));
        }

        private IEnumerator FadeInCharacter(Image img)'''

target_fadein2 = 'StartCoroutine(FadeInCharacter(img));'
replacement_fadein2 = 'StartFadeIn(img);'

# FadeOutCharacter
target_fadeout = '''        private void FadeOutCharacter(CharacterPosition pos)
        {
            Image img = GetCharacterImage(pos);
            if (img != null && img.gameObject.activeSelf)
            {
                StartCoroutine(FadeOutCharacterCoroutine(img));
            }
        }'''
replacement_fadeout = '''        private void FadeOutCharacter(CharacterPosition pos)
        {
            Image img = GetCharacterImage(pos);
            if (img != null && img.gameObject.activeSelf)
            {
                if (_fadeCoroutines.ContainsKey(img) && _fadeCoroutines[img] != null) StopCoroutine(_fadeCoroutines[img]);
                _fadeCoroutines[img] = StartCoroutine(FadeOutCharacterCoroutine(img));
            }
        }'''

# noFade hide image
target_nofade = '''                    // Instant hide
                    Image hideImg = GetCharacterImage(_activeSpeakerPositions[name]);
                    if (hideImg != null) hideImg.gameObject.SetActive(false);'''
replacement_nofade = '''                    // Instant hide
                    Image hideImg = GetCharacterImage(_activeSpeakerPositions[name]);
                    if (hideImg != null) 
                    {
                        if (_fadeCoroutines.ContainsKey(hideImg) && _fadeCoroutines[hideImg] != null) StopCoroutine(_fadeCoroutines[hideImg]);
                        hideImg.gameObject.SetActive(false);
                    }'''
                    
target_nofade2 = '''                        img.gameObject.SetActive(true);
                        Color c = img.color;
                        c.a = 1f;
                        img.color = c;'''
replacement_nofade2 = '''                        if (_fadeCoroutines.ContainsKey(img) && _fadeCoroutines[img] != null) StopCoroutine(_fadeCoroutines[img]);
                        img.gameObject.SetActive(true);
                        Color c = img.color;
                        c.a = 1f;
                        img.color = c;'''


# We need to replace these correctly. Let's do it manually.
text = text.replace(target_dict, replacement_dict)
text = text.replace(target_fadein1.replace('\n', '\r\n'), replacement_fadein1.replace('\n', '\r\n'))
text = text.replace(target_fadein1, replacement_fadein1)
text = text.replace(target_fadein2, replacement_fadein2)
text = text.replace(target_fadeout.replace('\n', '\r\n'), replacement_fadeout.replace('\n', '\r\n'))
text = text.replace(target_fadeout, replacement_fadeout)
text = text.replace(target_nofade.replace('\n', '\r\n'), replacement_nofade.replace('\n', '\r\n'))
text = text.replace(target_nofade, replacement_nofade)
text = text.replace(target_nofade2.replace('\n', '\r\n'), replacement_nofade2.replace('\n', '\r\n'))
text = text.replace(target_nofade2, replacement_nofade2)

with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueUI to track fade coroutines')
