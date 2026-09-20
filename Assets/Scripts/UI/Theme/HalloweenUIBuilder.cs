using HalloweenVN.Core;
using HalloweenVN.Dialogue;
using HalloweenVN.Investigation;
using HalloweenVN.Deduction;
using HalloweenVN.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem.UI;

namespace HalloweenVN.UI.Theme
{
    public class HalloweenUIBuilder : MonoBehaviour
    {
        private static bool isInitialized;

        [Header("Settings")]
        [SerializeField] private bool autoCreateManagers = true;
        [SerializeField] private string initialDialogueId = "test_dialogue_intro";
        
        private Canvas mainCanvas;
        private GameObject dialoguePanelRoot;
        private GameObject investigationPanelRoot;
        private GameObject deductionPanelRoot;
        private GameObject screenTransitionOverlay;
        private Transform templatesRoot;
        private GameObject lobbyPanelRoot;
        private Button settingsButtonRef;
        private BacklogUI backlogUiRef;
        
        void Awake()
        {
            if (isInitialized)
            {
                Destroy(gameObject);
                return;
            }
            isInitialized = true;

            if (autoCreateManagers) CreateManagers();
            CreateCanvas();
            
            // Create a hidden templates root
            GameObject templatesObj = new GameObject("_Templates");
            templatesObj.transform.SetParent(mainCanvas.transform, false);
            templatesObj.SetActive(false);
            templatesRoot = templatesObj.transform;

            CreateBackground();
            CreateDialogueUI();
            CreateInvestigationUI();
            CreateDeductionUI();
            CreateLobbyUI();
            CreateSettingsUI();
            CreateBacklogUI();
            CreateScreenTransition();
        }
        
        void Start()
        {
            // Start in Lobby — hide all game panels
            if (dialoguePanelRoot) dialoguePanelRoot.SetActive(false);
            if (investigationPanelRoot) investigationPanelRoot.SetActive(false);
            if (deductionPanelRoot) deductionPanelRoot.SetActive(false);

            // Show lobby
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);

            // Listen for phase changes to toggle panels
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += OnPhaseChanged;
            }
        }

        void OnDestroy()
        {
            isInitialized = false;
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= OnPhaseChanged;
            }
        }

        private void OnPhaseChanged(GamePhase phase)
        {
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(phase == GamePhase.Lobby);
            if (dialoguePanelRoot) dialoguePanelRoot.SetActive(phase == GamePhase.Dialogue || phase == GamePhase.Result);
            if (investigationPanelRoot) investigationPanelRoot.SetActive(phase == GamePhase.Investigation);
            if (deductionPanelRoot) deductionPanelRoot.SetActive(phase == GamePhase.Deduction);
        }

        private void CreateLobbyUI()
        {
            lobbyPanelRoot = UIHelper.CreateUIObject("LobbyRoot", mainCanvas.transform);
            UIHelper.StretchFull(lobbyPanelRoot.GetComponent<RectTransform>());

            // Background - AI Generated Halloween Mansion
            GameObject bgObj = UIHelper.CreateUIObject("Background", lobbyPanelRoot.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            Sprite bgSprite = Resources.Load<Sprite>("Images/lobby_bg");
            Image bgImg = UIHelper.AddImage(bgObj, Color.white, bgSprite);
            if (bgSprite == null)
            {
                // Fallback if image not found
                bgImg.color = new Color32(15, 8, 25, 255);
            }

            // Decorative top vignette
            GameObject topVig = UIHelper.CreateUIObject("TopVignette", lobbyPanelRoot.transform);
            RectTransform topVigRt = topVig.GetComponent<RectTransform>();
            UIHelper.SetAnchors(topVigRt, new Vector2(0, 0.7f), new Vector2(1, 1), new Vector2(0.5f, 1));
            topVigRt.offsetMin = Vector2.zero;
            topVigRt.offsetMax = Vector2.zero;
            UIHelper.AddImage(topVig, new Color32(40, 15, 60, 120));

            // ════════ Title Area ════════
            
            // Main Title (large, bright orange)
            GameObject titleObj = UIHelper.CreateUIObject("Title", lobbyPanelRoot.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            titleRt.anchoredPosition = new Vector2(0, 160);
            titleRt.sizeDelta = new Vector2(900, 80);
            TextMeshProUGUI titleText = UIHelper.AddText(titleObj, "할로윈 저택의 비밀",
                new Color32(255, 160, 30, 255), 56, TextAlignmentOptions.Center);
            titleText.fontStyle = FontStyles.Bold;
            titleText.enableWordWrapping = false;

            // Pumpkin emoji decoration above title
            GameObject decoObj = UIHelper.CreateUIObject("Decoration", lobbyPanelRoot.transform);
            RectTransform decoRt = decoObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(decoRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            decoRt.anchoredPosition = new Vector2(0, 230);
            decoRt.sizeDelta = new Vector2(300, 50);
            UIHelper.AddText(decoObj, "~ Halloween Mystery ~",
                new Color32(200, 120, 50, 180), 20, TextAlignmentOptions.Center);

            // Subtitle
            GameObject subObj = UIHelper.CreateUIObject("Subtitle", lobbyPanelRoot.transform);
            RectTransform subRt = subObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(subRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            subRt.anchoredPosition = new Vector2(0, 95);
            subRt.sizeDelta = new Vector2(700, 35);
            TextMeshProUGUI subtitleText = UIHelper.AddText(subObj, "The Secret of Halloween Mansion",
                new Color32(220, 200, 170, 200), 22, TextAlignmentOptions.Center);

            // Decorative divider line
            GameObject divider = UIHelper.CreateUIObject("Divider", lobbyPanelRoot.transform);
            RectTransform divRt = divider.GetComponent<RectTransform>();
            UIHelper.SetAnchors(divRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            divRt.anchoredPosition = new Vector2(0, 60);
            divRt.sizeDelta = new Vector2(400, 2);
            UIHelper.AddImage(divider, new Color32(255, 140, 0, 100));

            // ════════ Buttons ════════
            Color32 btnBg = new Color32(60, 30, 80, 240);
            Color32 btnBorder = new Color32(200, 110, 20, 255);

            // New Game Button
            var newGameTuple = CreateLobbyButton(lobbyPanelRoot.transform, "▶  새 게임", new Vector2(0, -10), btnBg, btnBorder);

            // Continue Button
            var continueTuple = CreateLobbyButton(lobbyPanelRoot.transform, "↻  이어하기", new Vector2(0, -85), btnBg, btnBorder);

            // Settings Button
            var settingsTuple = CreateLobbyButton(lobbyPanelRoot.transform, "⚙  설정", new Vector2(0, -160), btnBg, btnBorder);

            // ════════ Bottom ════════

            // Atmosphere text
            GameObject atmosObj = UIHelper.CreateUIObject("Atmosphere", lobbyPanelRoot.transform);
            RectTransform atmosRt = atmosObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(atmosRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            atmosRt.anchoredPosition = new Vector2(0, 80);
            atmosRt.sizeDelta = new Vector2(600, 30);
            UIHelper.AddText(atmosObj, "\"그 저택에는 숨겨진 비밀이 있다...\"",
                new Color32(180, 150, 120, 120), 16, TextAlignmentOptions.Center);

            // Credits / version
            GameObject creditObj = UIHelper.CreateUIObject("Credits", lobbyPanelRoot.transform);
            RectTransform creditRt = creditObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(creditRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            creditRt.anchoredPosition = new Vector2(0, 30);
            creditRt.sizeDelta = new Vector2(400, 25);
            UIHelper.AddText(creditObj, "v0.2 — Project F",
                new Color32(150, 150, 150, 80), 13, TextAlignmentOptions.Center);

            // Attach LobbyUI and wire fields
            LobbyUI lobbyUi = lobbyPanelRoot.AddComponent<LobbyUI>();
            UIHelper.SetField(lobbyUi, "lobbyPanel", lobbyPanelRoot);
            UIHelper.SetField(lobbyUi, "titleText", titleText);
            UIHelper.SetField(lobbyUi, "subtitleText", subtitleText);
            UIHelper.SetField(lobbyUi, "newGameButton", newGameTuple.btn);
            UIHelper.SetField(lobbyUi, "continueButton", continueTuple.btn);

            // Store settings button reference for later binding
            settingsButtonRef = settingsTuple.btn;
        }

        /// <summary>
        /// Creates a styled lobby button with bright border and clear text.
        /// </summary>
        private (Button btn, TextMeshProUGUI btnText) CreateLobbyButton(Transform parent, string label, Vector2 pos, Color32 bgColor, Color32 borderColor)
        {
            GameObject btnObj = UIHelper.CreateUIObject("LobbyBtn_" + label, parent);
            RectTransform rt = btnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            rt.anchoredPosition = pos;
            rt.sizeDelta = new Vector2(320, 60);

            Image img = UIHelper.AddImage(btnObj, bgColor);

            // Bright border
            Outline outline = btnObj.AddComponent<Outline>();
            outline.effectColor = borderColor;
            outline.effectDistance = new Vector2(2, 2);

            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = bgColor;
            cb.highlightedColor = new Color32(90, 50, 120, 255);
            cb.pressedColor = new Color32(150, 80, 30, 255);
            cb.colorMultiplier = 1f;
            cb.fadeDuration = 0.15f;
            btn.colors = cb;
            btn.targetGraphic = img;

            // Text (bright and readable)
            GameObject textObj = UIHelper.CreateUIObject("Text", btnObj.transform);
            UIHelper.StretchFull(textObj.GetComponent<RectTransform>());
            TextMeshProUGUI tmp = UIHelper.AddText(textObj, label,
                new Color32(255, 200, 100, 255), 26, TextAlignmentOptions.Center);
            tmp.fontStyle = FontStyles.Bold;

            return (btn, tmp);
        }

        private void CreateManagers()
        {
            CreateManagerIfNotExists<GameManager>("GameManager");
            CreateManagerIfNotExists<DialogueManager>("DialogueManager");
            CreateManagerIfNotExists<EvidenceInventory>("EvidenceInventory");
            CreateManagerIfNotExists<InvestigationManager>("InvestigationManager");
            CreateManagerIfNotExists<DeductionManager>("DeductionManager");
        }

        private void CreateManagerIfNotExists<T>(string name) where T : MonoBehaviour
        {
            if (Object.FindFirstObjectByType<T>() == null)
            {
                GameObject obj = new GameObject(name);
                obj.AddComponent<T>();
            }
        }

        private void CreateCanvas()
        {
            GameObject canvasObj = new GameObject("MainCanvas");
            mainCanvas = canvasObj.AddComponent<Canvas>();
            mainCanvas.renderMode = RenderMode.ScreenSpaceOverlay;
            mainCanvas.sortingOrder = 0;
            
            CanvasScaler scaler = canvasObj.AddComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1920, 1080);
            scaler.matchWidthOrHeight = 0.5f;
            
            canvasObj.AddComponent<GraphicRaycaster>();
            
            if (Object.FindFirstObjectByType<EventSystem>() == null)
            {
                GameObject esObj = new GameObject("EventSystem");
                esObj.AddComponent<EventSystem>();
                esObj.AddComponent<InputSystemUIInputModule>();
            }
        }

        private void CreateBackground()
        {
            GameObject bgObj = UIHelper.CreateUIObject("BackgroundOverlay", mainCanvas.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            UIHelper.AddImage(bgObj, HalloweenTheme.BackgroundDark);
        }

        private void CreateDialogueUI()
        {
            dialoguePanelRoot = UIHelper.CreateUIObject("DialogueRoot", mainCanvas.transform);
            UIHelper.StretchFull(dialoguePanelRoot.GetComponent<RectTransform>());
            
            // Background Image
            GameObject bgImgObj = UIHelper.CreateUIObject("BackgroundImage", dialoguePanelRoot.transform);
            UIHelper.StretchFull(bgImgObj.GetComponent<RectTransform>());
            Image backgroundImage = UIHelper.AddImage(bgImgObj, new Color(1,1,1,0));

            // Character Image
            GameObject charImgObj = UIHelper.CreateUIObject("CharacterImage", dialoguePanelRoot.transform);
            RectTransform charRt = charImgObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(charRt, new Vector2(0.2f, 0.5f), new Vector2(0.2f, 0.5f), new Vector2(0.5f, 0.5f));
            charRt.sizeDelta = new Vector2(600, 800);
            Image characterImage = UIHelper.AddImage(charImgObj, new Color(1,1,1,0));

            // Dialogue Panel
            GameObject dialoguePanel = UIHelper.CreatePanel("DialoguePanel", dialoguePanelRoot.transform, HalloweenTheme.PanelBackground);
            RectTransform panelRt = dialoguePanel.GetComponent<RectTransform>();
            UIHelper.SetBottom(panelRt, HalloweenTheme.DialoguePanelHeight);
            panelRt.offsetMin = new Vector2(50, 20); // padding
            panelRt.offsetMax = new Vector2(-50, HalloweenTheme.DialoguePanelHeight + 20);

            // Speaker Name
            GameObject speakerObj = UIHelper.CreateUIObject("SpeakerName", dialoguePanel.transform);
            RectTransform speakerRt = speakerObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(speakerRt, new Vector2(0, 1), new Vector2(0, 1), new Vector2(0, 1));
            speakerRt.anchoredPosition = new Vector2(30, -20);
            speakerRt.sizeDelta = new Vector2(400, 40);
            TextMeshProUGUI speakerName = UIHelper.AddText(speakerObj, "Speaker", HalloweenTheme.TextSpeaker, HalloweenTheme.SpeakerFontSize);
            speakerName.fontStyle = FontStyles.Bold;

            // Dialogue Text
            GameObject textObj = UIHelper.CreateUIObject("DialogueText", dialoguePanel.transform);
            RectTransform textRt = textObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(textRt);
            textRt.offsetMin = new Vector2(30, 20);
            textRt.offsetMax = new Vector2(-30, -70);
            TextMeshProUGUI dialogueText = UIHelper.AddText(textObj, "Dialogue text...", HalloweenTheme.TextPrimary, HalloweenTheme.DialogueFontSize);

            // Click Area
            GameObject clickObj = UIHelper.CreateUIObject("ClickArea", dialoguePanel.transform);
            UIHelper.StretchFull(clickObj.GetComponent<RectTransform>());
            Image clickImg = UIHelper.AddImage(clickObj, new Color(0,0,0,0));
            Button clickButton = clickObj.AddComponent<Button>();
            clickButton.targetGraphic = clickImg;

            // Choice Panel
            GameObject choicePanel = UIHelper.CreateUIObject("ChoicePanel", dialoguePanelRoot.transform);
            RectTransform choiceRt = choicePanel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(choiceRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            choiceRt.sizeDelta = new Vector2(600, 400);

            GameObject choiceContainer = UIHelper.CreateUIObject("ChoiceContainer", choicePanel.transform);
            UIHelper.StretchFull(choiceContainer.GetComponent<RectTransform>());
            VerticalLayoutGroup choiceVlg = choiceContainer.AddComponent<VerticalLayoutGroup>();
            choiceVlg.spacing = 10;
            choiceVlg.childAlignment = TextAnchor.MiddleCenter;
            choiceVlg.childControlHeight = true;
            choiceVlg.childControlWidth = true;

            // Choice Button Prefab Template
            var choiceBtnTuple = UIHelper.CreateButton(templatesRoot, "Choice", 500, HalloweenTheme.ChoiceButtonHeight);
            GameObject choiceButtonPrefab = choiceBtnTuple.btn.gameObject;

            // Auto / Skip / Log Buttons (top-right of dialogue panel)
            float btnW = 90, btnH = 35, btnSpacing = 8;
            
            var autoTuple = UIHelper.CreateButton(dialoguePanel.transform, "AUTO", btnW, btnH);
            RectTransform autoRt = autoTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            autoRt.anchoredPosition = new Vector2(-(btnW * 3 + btnSpacing * 2 + 10), -8);
            TextMeshProUGUI autoText = autoTuple.btn.GetComponentInChildren<TextMeshProUGUI>();

            var skipTuple = UIHelper.CreateButton(dialoguePanel.transform, "SKIP", btnW, btnH);
            RectTransform skipRt = skipTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            skipRt.anchoredPosition = new Vector2(-(btnW * 2 + btnSpacing + 10), -8);

            var logTuple = UIHelper.CreateButton(dialoguePanel.transform, "LOG", btnW, btnH);
            RectTransform logRt = logTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(logRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            logRt.anchoredPosition = new Vector2(-(btnW + 10), -8);

            // Attach DialogueUI and wire fields
            DialogueUI ui = dialoguePanelRoot.AddComponent<DialogueUI>();
            UIHelper.SetField(ui, "dialoguePanel", dialoguePanel);
            UIHelper.SetField(ui, "speakerNameText", speakerName);
            UIHelper.SetField(ui, "dialogueText", dialogueText);
            UIHelper.SetField(ui, "characterImage", characterImage);
            UIHelper.SetField(ui, "backgroundImage", backgroundImage);
            UIHelper.SetField(ui, "choicePanel", choicePanel);
            UIHelper.SetField(ui, "choiceButtonPrefab", choiceButtonPrefab);
            UIHelper.SetField(ui, "choiceButtonContainer", choiceContainer.transform);
            UIHelper.SetField(ui, "autoButton", autoTuple.btn);
            UIHelper.SetField(ui, "skipButton", skipTuple.btn);
            UIHelper.SetField(ui, "backlogButton", logTuple.btn);
            UIHelper.SetField(ui, "autoButtonText", autoText);

            clickButton.onClick.AddListener(() => {
                var method = ui.GetType().GetMethod("OnClick", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
                if (method != null) method.Invoke(ui, null);
            });

            // Wire LOG button to backlog toggle
            logTuple.btn.onClick.AddListener(() => {
                if (backlogUiRef != null) backlogUiRef.ToggleBacklog();
            });
        }

        private void CreateInvestigationUI()
        {
            investigationPanelRoot = UIHelper.CreateUIObject("InvestigationRoot", mainCanvas.transform);
            UIHelper.StretchFull(investigationPanelRoot.GetComponent<RectTransform>());

            // Evidence List Panel
            GameObject listPanel = UIHelper.CreatePanel("EvidenceListPanel", investigationPanelRoot.transform, HalloweenTheme.PanelBackground);
            RectTransform listRt = listPanel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(listRt, new Vector2(1, 0), new Vector2(1, 1), new Vector2(1, 0.5f));
            listRt.sizeDelta = new Vector2(350, 0);

            GameObject titleObj = UIHelper.CreateUIObject("Title", listPanel.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            titleRt.anchoredPosition = new Vector2(0, -30);
            titleRt.sizeDelta = new Vector2(0, 40);
            UIHelper.AddText(titleObj, "수집한 증거", HalloweenTheme.AccentOrange, HalloweenTheme.HeaderFontSize, TextAlignmentOptions.Center);

            GameObject countObj = UIHelper.CreateUIObject("EvidenceCountText", listPanel.transform);
            RectTransform countRt = countObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(countRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            countRt.anchoredPosition = new Vector2(0, -70);
            countRt.sizeDelta = new Vector2(0, 30);
            TextMeshProUGUI countText = UIHelper.AddText(countObj, "0/0", HalloweenTheme.TextPrimary, HalloweenTheme.BodyFontSize, TextAlignmentOptions.Center);

            var scrollTuple = UIHelper.CreateScrollView("EvidenceListScroll", listPanel.transform, 330, 700);
            RectTransform scrollRt = scrollTuple.scrollRect.GetComponent<RectTransform>();
            UIHelper.SetAnchors(scrollRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
            scrollRt.offsetMin = new Vector2(10, 100);
            scrollRt.offsetMax = new Vector2(-10, -110);
            Transform evidenceListContainer = scrollTuple.content;

            var proceedTuple = UIHelper.CreateButton(listPanel.transform, "추리 시작", 300, 60);
            Button proceedBtn = proceedTuple.btn;
            proceedBtn.interactable = false;
            RectTransform proceedRt = proceedBtn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(proceedRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            proceedRt.anchoredPosition = new Vector2(0, 40);

            // Evidence Detail Panel
            GameObject detailPanelRoot = UIHelper.CreateUIObject("EvidenceDetailPanel", investigationPanelRoot.transform);
            UIHelper.StretchFull(detailPanelRoot.GetComponent<RectTransform>());
            detailPanelRoot.SetActive(false);

            GameObject detailPanel = UIHelper.CreatePanel("DetailBG", detailPanelRoot.transform, HalloweenTheme.InventoryBg);
            RectTransform detailRt = detailPanel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(detailRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            detailRt.sizeDelta = new Vector2(500, 600);

            GameObject iconObj = UIHelper.CreateUIObject("EvidenceDetailIcon", detailPanel.transform);
            RectTransform iconRt = iconObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(iconRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            iconRt.anchoredPosition = new Vector2(0, -100);
            iconRt.sizeDelta = new Vector2(150, 150);
            Image detailIcon = UIHelper.AddImage(iconObj, Color.white);

            GameObject nameObj = UIHelper.CreateUIObject("EvidenceDetailName", detailPanel.transform);
            RectTransform nameRt = nameObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(nameRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            nameRt.anchoredPosition = new Vector2(0, -280);
            nameRt.sizeDelta = new Vector2(0, 50);
            TextMeshProUGUI detailName = UIHelper.AddText(nameObj, "Name", HalloweenTheme.AccentOrange, HalloweenTheme.HeaderFontSize, TextAlignmentOptions.Center);

            GameObject descObj = UIHelper.CreateUIObject("EvidenceDetailDescription", detailPanel.transform);
            RectTransform descRt = descObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(descRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            descRt.anchoredPosition = new Vector2(0, -350);
            descRt.sizeDelta = new Vector2(0, 150);
            TextMeshProUGUI detailDesc = UIHelper.AddText(descObj, "Description", HalloweenTheme.TextPrimary, HalloweenTheme.BodyFontSize, TextAlignmentOptions.Center);

            var closeTuple = UIHelper.CreateButton(detailPanel.transform, "닫기", 200, 50);
            Button closeBtn = closeTuple.btn;
            RectTransform closeRt = closeBtn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 30);

            // Evidence Item Prefab
            var itemTuple = UIHelper.CreateButton(templatesRoot, "Evidence", HalloweenTheme.EvidenceSlotWidth, 50);
            GameObject evidenceItemPrefab = itemTuple.btn.gameObject;
            evidenceItemPrefab.GetComponent<Image>().color = HalloweenTheme.SlotEmpty;
            itemTuple.btnText.color = HalloweenTheme.TextPrimary;
            itemTuple.btnText.fontSize = 20;
            LayoutElement itemLe = evidenceItemPrefab.AddComponent<LayoutElement>();
            itemLe.preferredHeight = 50;

            // Attach and wire InvestigationUI
            InvestigationUI invUi = investigationPanelRoot.AddComponent<InvestigationUI>();
            UIHelper.SetField(invUi, "evidenceListPanel", listPanel);
            UIHelper.SetField(invUi, "evidenceCountText", countText);
            UIHelper.SetField(invUi, "evidenceListContainer", evidenceListContainer);
            UIHelper.SetField(invUi, "proceedButton", proceedBtn);
            UIHelper.SetField(invUi, "evidenceDetailPanel", detailPanelRoot);
            UIHelper.SetField(invUi, "evidenceDetailIcon", detailIcon);
            UIHelper.SetField(invUi, "evidenceDetailName", detailName);
            UIHelper.SetField(invUi, "evidenceDetailDescription", detailDesc);
            UIHelper.SetField(invUi, "evidenceItemPrefab", evidenceItemPrefab);

            closeBtn.onClick.AddListener(() => {
                var method = invUi.GetType().GetMethod("HideEvidenceDetail", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                if (method != null) method.Invoke(invUi, null);
                else detailPanelRoot.SetActive(false);
            });
        }

        private void CreateDeductionUI()
        {
            deductionPanelRoot = UIHelper.CreateUIObject("DeductionRoot", mainCanvas.transform);
            UIHelper.StretchFull(deductionPanelRoot.GetComponent<RectTransform>());

            GameObject deductionPanel = UIHelper.CreatePanel("DeductionPanel", deductionPanelRoot.transform, HalloweenTheme.PanelBackground);
            UIHelper.StretchFull(deductionPanel.GetComponent<RectTransform>());

            GameObject caseObj = UIHelper.CreateUIObject("CaseNameText", deductionPanel.transform);
            RectTransform caseRt = caseObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(caseRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            caseRt.anchoredPosition = new Vector2(0, -30);
            caseRt.sizeDelta = new Vector2(600, 50);
            TextMeshProUGUI caseNameText = UIHelper.AddText(caseObj, "Case Name", HalloweenTheme.AccentOrange, HalloweenTheme.HeaderFontSize, TextAlignmentOptions.Center);

            // Questions Area
            GameObject qArea = UIHelper.CreateUIObject("QuestionsArea", deductionPanel.transform);
            RectTransform qRt = qArea.GetComponent<RectTransform>();
            UIHelper.SetAnchors(qRt, new Vector2(0, 0), new Vector2(0.6f, 1), new Vector2(0.5f, 0.5f));
            qRt.offsetMin = new Vector2(20, 100);
            qRt.offsetMax = new Vector2(-20, -100);

            GameObject qContainer = UIHelper.CreateUIObject("QuestionContainer", qArea.transform);
            UIHelper.StretchFull(qContainer.GetComponent<RectTransform>());
            VerticalLayoutGroup qVlg = qContainer.AddComponent<VerticalLayoutGroup>();
            qVlg.spacing = 15;
            qVlg.childControlHeight = true;
            qVlg.childControlWidth = true;

            // Evidence Area
            GameObject evArea = UIHelper.CreateUIObject("EvidenceArea", deductionPanel.transform);
            RectTransform evRt = evArea.GetComponent<RectTransform>();
            UIHelper.SetAnchors(evRt, new Vector2(0.6f, 0), new Vector2(1f, 1), new Vector2(0.5f, 0.5f));
            evRt.offsetMin = new Vector2(20, 100);
            evRt.offsetMax = new Vector2(-20, -100);

            GameObject evTitleObj = UIHelper.CreateUIObject("Title", evArea.transform);
            RectTransform evTitleRt = evTitleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(evTitleRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            evTitleRt.anchoredPosition = new Vector2(0, -10);
            evTitleRt.sizeDelta = new Vector2(0, 40);
            UIHelper.AddText(evTitleObj, "증거 목록", HalloweenTheme.TextPrimary, HalloweenTheme.HeaderFontSize, TextAlignmentOptions.Center);

            GameObject evContainer = UIHelper.CreateUIObject("EvidenceInventoryContainer", evArea.transform);
            RectTransform evContRt = evContainer.GetComponent<RectTransform>();
            UIHelper.SetAnchors(evContRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
            evContRt.offsetMin = new Vector2(0, 0);
            evContRt.offsetMax = new Vector2(0, -60);
            GridLayoutGroup glg = evContainer.AddComponent<GridLayoutGroup>();
            glg.cellSize = new Vector2(HalloweenTheme.EvidenceItemSize, HalloweenTheme.EvidenceItemSize);
            glg.spacing = new Vector2(10, 10);
            glg.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            glg.constraintCount = 2;

            // Submit Button
            var submitTuple = UIHelper.CreateButton(deductionPanel.transform, "추리 제출", 250, 60);
            Button submitBtn = submitTuple.btn;
            RectTransform submitRt = submitBtn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(submitRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            submitRt.anchoredPosition = new Vector2(0, 40);

            // Result Panel
            GameObject resPanelRoot = UIHelper.CreateUIObject("ResultPanel", deductionPanelRoot.transform);
            UIHelper.StretchFull(resPanelRoot.GetComponent<RectTransform>());
            resPanelRoot.SetActive(false);

            GameObject resBg = UIHelper.CreatePanel("ResultBG", resPanelRoot.transform, HalloweenTheme.InventoryBg);
            RectTransform resBgRt = resBg.GetComponent<RectTransform>();
            UIHelper.SetAnchors(resBgRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            resBgRt.sizeDelta = new Vector2(600, 300);

            GameObject resTextObj = UIHelper.CreateUIObject("ResultText", resBg.transform);
            UIHelper.StretchFull(resTextObj.GetComponent<RectTransform>());
            TextMeshProUGUI resultText = UIHelper.AddText(resTextObj, "Result", HalloweenTheme.TextPrimary, HalloweenTheme.HeaderFontSize, TextAlignmentOptions.Center);

            // QuestionSlotPrefab
            GameObject qSlotPrefab = UIHelper.CreateUIObject("QuestionSlot", templatesRoot);
            RectTransform qSlotRt = qSlotPrefab.GetComponent<RectTransform>();
            qSlotRt.sizeDelta = new Vector2(600, HalloweenTheme.EvidenceSlotHeight);
            HorizontalLayoutGroup hlg = qSlotPrefab.AddComponent<HorizontalLayoutGroup>();
            hlg.spacing = 10;
            hlg.childControlHeight = true;
            hlg.childControlWidth = true;

            GameObject qTextObj = UIHelper.CreateUIObject("QuestionText", qSlotPrefab.transform);
            TextMeshProUGUI qText = UIHelper.AddText(qTextObj, "Question?", HalloweenTheme.TextPrimary, HalloweenTheme.BodyFontSize);
            LayoutElement qLe = qTextObj.AddComponent<LayoutElement>();
            qLe.preferredWidth = 360;

            GameObject dropZoneObj = UIHelper.CreateUIObject("DropZone", qSlotPrefab.transform);
            Image dropBg = UIHelper.AddImage(dropZoneObj, HalloweenTheme.SlotEmpty);
            LayoutElement dropLe = dropZoneObj.AddComponent<LayoutElement>();
            dropLe.preferredWidth = HalloweenTheme.EvidenceItemSize;
            
            GameObject dropIconObj = UIHelper.CreateUIObject("Icon", dropZoneObj.transform);
            UIHelper.StretchFull(dropIconObj.GetComponent<RectTransform>());
            Image dropIcon = UIHelper.AddImage(dropIconObj, new Color(1,1,1,0));

            EvidenceSlot evidenceSlot = dropZoneObj.AddComponent<EvidenceSlot>();
            UIHelper.SetField(evidenceSlot, "slotIcon", dropIcon);
            UIHelper.SetField(evidenceSlot, "questionText", qText);
            UIHelper.SetField(evidenceSlot, "slotBackground", dropBg);
            UIHelper.SetField(evidenceSlot, "emptyColor", HalloweenTheme.SlotEmpty);
            UIHelper.SetField(evidenceSlot, "filledColor", HalloweenTheme.SlotFilled);

            // EvidenceDragItemPrefab
            GameObject dragPrefab = UIHelper.CreateUIObject("EvidenceDragItem", templatesRoot);
            dragPrefab.GetComponent<RectTransform>().sizeDelta = new Vector2(HalloweenTheme.EvidenceItemSize, HalloweenTheme.EvidenceItemSize);
            UIHelper.AddImage(dragPrefab, HalloweenTheme.SlotEmpty);
            
            GameObject dragIconObj = UIHelper.CreateUIObject("Icon", dragPrefab.transform);
            UIHelper.StretchFull(dragIconObj.GetComponent<RectTransform>());
            Image dragIcon = UIHelper.AddImage(dragIconObj, new Color(1,1,1,1));
            
            dragPrefab.AddComponent<CanvasGroup>();
            EvidenceDragItem dragItem = dragPrefab.AddComponent<EvidenceDragItem>();
            UIHelper.SetField(dragItem, "iconImage", dragIcon);

            // Attach DeductionUI
            DeductionUI dedUi = deductionPanelRoot.AddComponent<DeductionUI>();
            UIHelper.SetField(dedUi, "deductionPanel", deductionPanel);
            UIHelper.SetField(dedUi, "caseNameText", caseNameText);
            UIHelper.SetField(dedUi, "questionContainer", qContainer.transform);
            UIHelper.SetField(dedUi, "evidenceInventoryContainer", evContainer.transform);
            UIHelper.SetField(dedUi, "submitButton", submitBtn);
            UIHelper.SetField(dedUi, "resultPanel", resPanelRoot);
            UIHelper.SetField(dedUi, "resultText", resultText);
            UIHelper.SetField(dedUi, "questionSlotPrefab", qSlotPrefab);
            UIHelper.SetField(dedUi, "evidenceDragItemPrefab", dragPrefab);
        }

        private void CreateSettingsUI()
        {
            GameObject settingsRoot = UIHelper.CreateUIObject("SettingsRoot", mainCanvas.transform);
            UIHelper.StretchFull(settingsRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay
            UIHelper.AddImage(settingsRoot, new Color(0, 0, 0, 0.7f));

            // Settings panel
            GameObject panel = UIHelper.CreatePanel("SettingsPanel", settingsRoot.transform, HalloweenTheme.PanelBackground);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(500, 450);

            // Title
            GameObject titleObj = UIHelper.CreateUIObject("Title", panel.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleRt.anchoredPosition = new Vector2(0, -30);
            titleRt.sizeDelta = new Vector2(400, 40);
            UIHelper.AddText(titleObj, "⚙ 설정", HalloweenTheme.AccentOrange, 32, TextAlignmentOptions.Center);

            // Text Speed Slider
            float yPos = -80;
            var textSpeedLabel = CreateSettingsLabel(panel.transform, "텍스트 속도", yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // BGM Volume
            yPos -= 80;
            var bgmLabel = CreateSettingsLabel(panel.transform, "BGM", yPos);
            Slider bgmSlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // SFX Volume
            yPos -= 80;
            var sfxLabel = CreateSettingsLabel(panel.transform, "SFX", yPos);
            Slider sfxSlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // Fullscreen Toggle
            yPos -= 80;
            GameObject toggleObj = UIHelper.CreateUIObject("FullscreenToggle", panel.transform);
            RectTransform toggleRt = toggleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(toggleRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            toggleRt.anchoredPosition = new Vector2(0, yPos);
            toggleRt.sizeDelta = new Vector2(400, 30);
            Toggle fullscreenToggle = toggleObj.AddComponent<Toggle>();
            UIHelper.AddText(toggleObj, "전체 화면", HalloweenTheme.TextPrimary, 20);

            // Close Button
            var closeTuple = UIHelper.CreateButton(panel.transform, "닫기", 200, 50);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 40);

            // Attach SettingsUI
            SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();
            UIHelper.SetField(settingsUi, "settingsPanel", settingsRoot);
            UIHelper.SetField(settingsUi, "textSpeedSlider", textSpeedSlider);
            UIHelper.SetField(settingsUi, "textSpeedLabel", textSpeedLabel);
            UIHelper.SetField(settingsUi, "bgmVolumeSlider", bgmSlider);
            UIHelper.SetField(settingsUi, "bgmVolumeLabel", bgmLabel);
            UIHelper.SetField(settingsUi, "sfxVolumeSlider", sfxSlider);
            UIHelper.SetField(settingsUi, "sfxVolumeLabel", sfxLabel);
            UIHelper.SetField(settingsUi, "fullscreenToggle", fullscreenToggle);
            UIHelper.SetField(settingsUi, "closeButton", closeTuple.btn);

            settingsRoot.SetActive(false);

            // Wire lobby settings button
            if (settingsButtonRef != null)
            {
                settingsButtonRef.onClick.AddListener(() => settingsUi.Show());
            }
        }

        private TextMeshProUGUI CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(400, 25);
            return UIHelper.AddText(obj, text, HalloweenTheme.TextPrimary, 18);
        }

        private Slider CreateSettingsSlider(Transform parent, float yPos)
        {
            GameObject sliderObj = UIHelper.CreateUIObject("Slider", parent);
            RectTransform rt = sliderObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(350, 20);

            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", sliderObj.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            Image bgImg = UIHelper.AddImage(bgObj, HalloweenTheme.SlotEmpty);

            // Fill Area
            GameObject fillArea = UIHelper.CreateUIObject("Fill Area", sliderObj.transform);
            UIHelper.StretchFull(fillArea.GetComponent<RectTransform>());
            GameObject fill = UIHelper.CreateUIObject("Fill", fillArea.transform);
            UIHelper.StretchFull(fill.GetComponent<RectTransform>());
            Image fillImg = UIHelper.AddImage(fill, HalloweenTheme.AccentOrange);

            Slider slider = sliderObj.AddComponent<Slider>();
            slider.fillRect = fill.GetComponent<RectTransform>();
            slider.targetGraphic = bgImg;

            return slider;
        }

        private void CreateBacklogUI()
        {
            GameObject backlogRoot = UIHelper.CreateUIObject("BacklogRoot", mainCanvas.transform);
            UIHelper.StretchFull(backlogRoot.GetComponent<RectTransform>());

            // Semi-transparent overlay
            UIHelper.AddImage(backlogRoot, new Color(0, 0, 0, 0.8f));

            // Scroll area
            GameObject scrollObj = UIHelper.CreateUIObject("ScrollView", backlogRoot.transform);
            RectTransform scrollRt = scrollObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(scrollRt);
            scrollRt.offsetMin = new Vector2(100, 80);
            scrollRt.offsetMax = new Vector2(-100, -60);

            ScrollRect scrollRect = scrollObj.AddComponent<ScrollRect>();
            scrollRect.horizontal = false;
            scrollRect.vertical = true;

            // Content container
            GameObject content = UIHelper.CreateUIObject("Content", scrollObj.transform);
            RectTransform contentRt = content.GetComponent<RectTransform>();
            UIHelper.SetAnchors(contentRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            contentRt.sizeDelta = new Vector2(0, 0);
            ContentSizeFitter fitter = content.AddComponent<ContentSizeFitter>();
            fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            VerticalLayoutGroup vlg = content.AddComponent<VerticalLayoutGroup>();
            vlg.spacing = 8;
            vlg.padding = new RectOffset(10, 10, 10, 10);
            vlg.childControlWidth = true;
            vlg.childControlHeight = true;
            vlg.childForceExpandWidth = true;
            vlg.childForceExpandHeight = false;

            scrollRect.content = contentRt;

            // Entry prefab template
            GameObject entryPrefab = UIHelper.CreateUIObject("BacklogEntry", templatesRoot);
            RectTransform entryRt = entryPrefab.GetComponent<RectTransform>();
            entryRt.sizeDelta = new Vector2(0, 30);
            TextMeshProUGUI entryText = UIHelper.AddText(entryPrefab, "", HalloweenTheme.TextPrimary, 18);
            entryText.richText = true;

            // Title
            GameObject titleObj = UIHelper.CreateUIObject("BacklogTitle", backlogRoot.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleRt.anchoredPosition = new Vector2(0, -25);
            titleRt.sizeDelta = new Vector2(400, 40);
            UIHelper.AddText(titleObj, "📜 백로그", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);

            // Close button
            var closeTuple = UIHelper.CreateButton(backlogRoot.transform, "닫기", 200, 50);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 30);

            // Attach BacklogUI
            backlogUiRef = backlogRoot.AddComponent<BacklogUI>();
            UIHelper.SetField(backlogUiRef, "backlogPanel", backlogRoot);
            UIHelper.SetField(backlogUiRef, "contentContainer", content.transform);
            UIHelper.SetField(backlogUiRef, "backlogEntryPrefab", entryPrefab);
            UIHelper.SetField(backlogUiRef, "closeButton", closeTuple.btn);
            UIHelper.SetField(backlogUiRef, "scrollRect", scrollRect);

            backlogRoot.SetActive(false);
        }

        private void CreateScreenTransition()
        {
            GameObject transObj = new GameObject("ScreenTransition");
            Canvas canvas = transObj.AddComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = 100;

            CanvasScaler scaler = transObj.AddComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1920, 1080);

            GameObject overlayObj = UIHelper.CreateUIObject("Overlay", transObj.transform);
            UIHelper.StretchFull(overlayObj.GetComponent<RectTransform>());
            Image img = UIHelper.AddImage(overlayObj, HalloweenTheme.TransitionColor);
            
            Color c = img.color;
            c.a = 0;
            img.color = c;

            transObj.AddComponent<ScreenTransition>();
            screenTransitionOverlay = transObj;
        }
    }
}
