import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target1 = '''            // Dim/Highlight based on speaker
            UpdateSpeakerHighlight(node.speaker);'''

replacement1 = '''            // Dim/Highlight based on speaker
            bool wasNarrator = !_currentlyInDialoguePanel;
            bool isNarratorNow = string.IsNullOrEmpty(node.speaker);
            bool usePanelNow = !isNarratorNow;
            bool instantHighlight = wasNarrator && usePanelNow; // 컷신(독백)에서 대화로 넘어올 때는 깜빡임 방지를 위해 즉시 색상 적용
            UpdateSpeakerHighlight(node.speaker, instantHighlight);'''

target2 = '''        private void UpdateSpeakerHighlight(string speaker)
        {
            if (string.IsNullOrWhiteSpace(speaker))
            {
                // Narrator — all active characters stay bright
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), true);
                }
                return;
            }

            foreach (var kvp in _activeSpeakerPositions)
            {
                bool isSpeaking = kvp.Key == speaker;
                DimCharacterImage(GetCharacterImage(kvp.Value), isSpeaking);
            }
        }'''

replacement2 = '''        private void UpdateSpeakerHighlight(string speaker, bool instant = false)
        {
            if (string.IsNullOrWhiteSpace(speaker))
            {
                // Narrator — all active characters stay bright
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), true, instant);
                }
                return;
            }

            foreach (var kvp in _activeSpeakerPositions)
            {
                bool isSpeaking = kvp.Key == speaker;
                DimCharacterImage(GetCharacterImage(kvp.Value), isSpeaking, instant);
            }
        }'''

target3 = '''        private void DimCharacterImage(Image image, bool isActive, float duration = 0.2f)
        {
            if (image == null) return;
            if (!image.gameObject.activeSelf) return;

            Color targetColor = isActive ? ACTIVE_COLOR : DIM_COLOR;

            if (_highlightCoroutines.ContainsKey(image) && _highlightCoroutines[image] != null)
            {
                StopCoroutine(_highlightCoroutines[image]);
            }
            _highlightCoroutines[image] = StartCoroutine(FadeColorCoroutine(image, targetColor, duration));
        }'''

replacement3 = '''        private void DimCharacterImage(Image image, bool isActive, bool instant = false)
        {
            if (image == null) return;
            if (!image.gameObject.activeSelf) return;

            Color targetColor = isActive ? ACTIVE_COLOR : DIM_COLOR;
            float duration = instant ? 0f : 0.2f;

            if (_highlightCoroutines.ContainsKey(image) && _highlightCoroutines[image] != null)
            {
                StopCoroutine(_highlightCoroutines[image]);
            }
            
            if (duration <= 0f)
            {
                Color finalC = targetColor;
                finalC.a = image.color.a;
                image.color = finalC;
            }
            else
            {
                _highlightCoroutines[image] = StartCoroutine(FadeColorCoroutine(image, targetColor, duration));
            }
        }'''

target_win1 = target1.replace('\n', '\r\n')
replacement_win1 = replacement1.replace('\n', '\r\n')
target_win2 = target2.replace('\n', '\r\n')
replacement_win2 = replacement2.replace('\n', '\r\n')
target_win3 = target3.replace('\n', '\r\n')
replacement_win3 = replacement3.replace('\n', '\r\n')

if target_win1 in text:
    text = text.replace(target_win1, replacement_win1)
    text = text.replace(target_win2, replacement_win2)
    text = text.replace(target_win3, replacement_win3)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Fixed (win lf)')
elif target1 in text:
    text = text.replace(target1, replacement1)
    text = text.replace(target2, replacement2)
    text = text.replace(target3, replacement3)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Fixed (lf)')
else:
    print('Target not found')
