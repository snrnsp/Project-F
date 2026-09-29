import sys

with open('Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

target1 = '''        [SerializeField] private Button autoButton;
        [SerializeField] private Button backlogButton;

        [SerializeField] private Text autoButtonText;
        [SerializeField] private Text backlogButtonText;
// ??????????? Typing & Auto ???????????
        private Coroutine typingCoroutine;
        private Coroutine autoPlayCoroutine;
        private bool isTyping;
        private bool isAutoPlay;'''

replacement1 = '''        [SerializeField] private Button autoButton;
        [SerializeField] private Button skipButton;
        [SerializeField] private Button backlogButton;

        [SerializeField] private Text autoButtonText;
        [SerializeField] private Text skipButtonText;
        [SerializeField] private Text backlogButtonText;
// ??????????? Typing & Auto ???????????
        private Coroutine typingCoroutine;
        private Coroutine autoPlayCoroutine;
        private Coroutine skipModeCoroutine;
        private bool isTyping;
        private bool isAutoPlay;
        private bool isSkipMode;'''

if target1 in content:
    content = content.replace(target1, replacement1)
    print("Replaced 1")

target2 = '''            if (backlogButtonText != null) backlogButtonText.resizeTextForBestFit = false;
            if (autoButtonText != null) autoButtonText.resizeTextForBestFit = false;'''

replacement2 = '''            if (backlogButtonText != null) backlogButtonText.resizeTextForBestFit = false;
            if (autoButtonText != null) autoButtonText.resizeTextForBestFit = false;
            if (skipButtonText != null) skipButtonText.resizeTextForBestFit = false;'''

if target2 in content:
    content = content.replace(target2, replacement2)
    print("Replaced 2")

target3 = '''            if (backlogButtonText != null) backlogButtonText.fontSize = btnSize;
            if (autoButtonText != null) autoButtonText.fontSize = btnSize;'''

replacement3 = '''            if (backlogButtonText != null) backlogButtonText.fontSize = btnSize;
            if (autoButtonText != null) autoButtonText.fontSize = btnSize;
            if (skipButtonText != null) skipButtonText.fontSize = btnSize;'''

if target3 in content:
    content = content.replace(target3, replacement3)
    print("Replaced 3")

target4 = '''            string autoOff = "AUTO";
            string autoOn = "AUTO ON";'''

replacement4 = '''            string autoOff = "AUTO";
            string autoOn = "AUTO ON";
            string skipOff = "SKIP";
            string skipOn = "SKIP ON";'''

if target4 in content:
    content = content.replace(target4, replacement4)
    print("Replaced 4")

target5 = '''            if (lang == HalloweenVN.Core.GameLanguage.Korean)
            {
                autoOff = "오토"; autoOn = "오토 중";
                backlogButtonText.text = "로그";
            }'''

replacement5 = '''            if (lang == HalloweenVN.Core.GameLanguage.Korean)
            {
                autoOff = "오토"; autoOn = "오토 중";
                skipOff = "스킵"; skipOn = "스킵 중";
                backlogButtonText.text = "로그";
            }'''

if target5 in content:
    content = content.replace(target5, replacement5)
    print("Replaced 5")

target6 = '''            if (autoButtonText != null)
            {
                autoButtonText.text = isAutoPlay ? autoOn : autoOff;
            }'''

replacement6 = '''            if (autoButtonText != null)
            {
                autoButtonText.text = isAutoPlay ? autoOn : autoOff;
            }
            if (skipButtonText != null)
            {
                skipButtonText.text = isSkipMode ? skipOn : skipOff;
            }'''

if target6 in content:
    content = content.replace(target6, replacement6)
    print("Replaced 6")

target7 = '''            if (autoButton != null) autoButton.onClick.AddListener(ToggleAutoPlay);'''
replacement7 = '''            if (autoButton != null) autoButton.onClick.AddListener(ToggleAutoPlay);
            if (skipButton != null) skipButton.onClick.AddListener(ToggleSkipMode);'''

if target7 in content:
    content = content.replace(target7, replacement7)
    print("Replaced 7")

target8 = '''            if (autoButton != null) autoButton.onClick.RemoveListener(ToggleAutoPlay);
            StopAutoPlay();'''
replacement8 = '''            if (autoButton != null) autoButton.onClick.RemoveListener(ToggleAutoPlay);
            if (skipButton != null) skipButton.onClick.RemoveListener(ToggleSkipMode);
            StopAutoPlay();
            StopSkipMode();'''

if target8 in content:
    content = content.replace(target8, replacement8)
    print("Replaced 8")

target9 = '''        public void HideDialoguePanel()
        {
            if (dialoguePanel != null)
                dialoguePanel.SetActive(false);
            ClearChoices();
            StopAutoPlay();
            HideAllCharacters();
        }'''
replacement9 = '''        public void HideDialoguePanel()
        {
            if (dialoguePanel != null)
                dialoguePanel.SetActive(false);
            ClearChoices();
            StopAutoPlay();
            StopSkipMode();
            HideAllCharacters();
        }'''

if target9 in content:
    content = content.replace(target9, replacement9)
    print("Replaced 9")

target10 = '''        public void ShowChoices(List<DialogueChoice> choices)
        {
            ClearChoices();'''
replacement10 = '''        public void ShowChoices(List<DialogueChoice> choices)
        {
            ClearChoices();
            StopAutoPlay();
            StopSkipMode();'''

if target10 in content:
    content = content.replace(target10, replacement10)
    print("Replaced 10")

target11 = '''        private void StopAutoPlay()
        {
            isAutoPlay = false;
            if (autoButtonText != null) UpdateLanguage();
            if (autoPlayCoroutine != null)
            {
                StopCoroutine(autoPlayCoroutine);
                autoPlayCoroutine = null;
            }
        }'''
replacement11 = '''        private void StopAutoPlay()
        {
            isAutoPlay = false;
            if (autoButtonText != null) UpdateLanguage();
            if (autoPlayCoroutine != null)
            {
                StopCoroutine(autoPlayCoroutine);
                autoPlayCoroutine = null;
            }
        }

        public void ToggleSkipMode()
        {
            isSkipMode = !isSkipMode;
            if (isSkipMode) StopAutoPlay();
            if (skipButtonText != null) UpdateLanguage();

            if (isSkipMode && !isTyping && DialogueManager.Instance != null && DialogueManager.Instance.IsPlaying)
            {
                if (skipModeCoroutine != null) StopCoroutine(skipModeCoroutine);
                skipModeCoroutine = StartCoroutine(SkipAdvanceDelay());
            }
            else if (!isSkipMode && skipModeCoroutine != null)
            {
                StopCoroutine(skipModeCoroutine);
                skipModeCoroutine = null;
            }
        }

        private void StopSkipMode()
        {
            isSkipMode = false;
            if (skipButtonText != null) UpdateLanguage();
            if (skipModeCoroutine != null)
            {
                StopCoroutine(skipModeCoroutine);
                skipModeCoroutine = null;
            }
        }

        private IEnumerator SkipAdvanceDelay()
        {
            yield return new WaitForSeconds(0.05f);
            if (isSkipMode && DialogueManager.Instance != null && GameManager.Instance != null && GameManager.Instance.CurrentPhase == GamePhase.Dialogue)
            {
                DialogueManager.Instance.AdvanceDialogue();
            }
        }'''

if target11 in content:
    content = content.replace(target11, replacement11)
    print("Replaced 11")

target12 = '''            if (isAutoPlay)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }'''
replacement12 = '''            if (isSkipMode)
            {
                if (skipModeCoroutine != null) StopCoroutine(skipModeCoroutine);
                skipModeCoroutine = StartCoroutine(SkipAdvanceDelay());
            }
            else if (isAutoPlay)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }'''

if target12 in content:
    content = content.replace(target12, replacement12)
    print("Replaced 12")


target13 = '''        public void OnClick() { if (Time.unscaledTime - _lastClickTime < 0.05f) return; // Prevent double-trigger from UI Event System + Input System
            _lastClickTime = Time.unscaledTime;

            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");'''
replacement13 = '''        public void OnClick() { if (Time.unscaledTime - _lastClickTime < 0.05f) return; // Prevent double-trigger from UI Event System + Input System
            _lastClickTime = Time.unscaledTime;

            if (isSkipMode)
            {
                StopSkipMode();
                return;
            }

            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");'''

if target13 in content:
    content = content.replace(target13, replacement13)
    print("Replaced 13")

with open('Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

