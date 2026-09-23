﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿using HalloweenVN.Core;
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
        
        private Canvas mainCanvas;
        private GameObject dialoguePanelRoot;
        private GameObject investigationPanelRoot;
        private GameObject deductionPanelRoot;
        private GameObject screenTransitionOverlay;
        private Transform templatesRoot;
        private GameObject lobbyPanelRoot;
        private Button settingsButtonRef;
        private Button langButtonRef;
        private BacklogUI backlogUiRef;
        private ExtraUI extraUiRef;
        private SettingsUI settingsUiRef;
        private GlobalUIManager globalMgrRef;
        private GameObject globalSettingsBtnObj;
        private GameObject lobbySettingsBtnObj;
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
            CreateGlobalUI();
            CreateSettingsUI();
            CreateLanguageUI();
            CreateBacklogUI();
            CreateExtraUI();
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

            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", lobbyPanelRoot.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            Sprite bgSprite = Resources.Load<Sprite>("Images/lobby_bg");
            Image bgImg = UIHelper.AddImage(bgObj, new Color(1f, 1f, 1f, 1f), bgSprite); // 100% opacity
            if (bgSprite == null)
            {
                bgImg.color = new Color32(15, 8, 25, 255);
            }

            // Title Text (Top Left)
            GameObject titleObj = UIHelper.CreateUIObject("LobbyTitleText", lobbyPanelRoot.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            titleRt.anchoredPosition = new Vector2(110, 310);
            titleRt.sizeDelta = new Vector2(400, 120);
            Text lobbyTitleText = CreateLegacyText(titleObj, "오블리비언\n<size=22>OBLIVION</size>", new Color32(255, 150, 40, 255), 56, TextAnchor.MiddleCenter);
            lobbyTitleText.fontStyle = FontStyle.Bold;
            lobbyTitleText.lineSpacing = 0.65f;
            UnityEngine.UI.Outline titleOutline = titleObj.AddComponent<UnityEngine.UI.Outline>();
            titleOutline.effectColor = new Color32(0, 0, 0, 255);
            titleOutline.effectDistance = new Vector2(2, -2);

            // Buttons (Left side, Halloween, 100% Opacity)
            Color32 btnBg = new Color32(230, 100, 20, 255); // Pumpkin orange
            
            float startY = 160f; // Center adjusted (+160 to -160 for 5 buttons)
            float spacing = 80f;
            int i = 0;

            var loadTuple = CreateLegacyButton(lobbyPanelRoot.transform, "이어하기", 260, 55, btnBg);
            UIHelper.SetAnchors(loadTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            loadTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var startTuple = CreateLegacyButton(lobbyPanelRoot.transform, "새 게임", 260, 55, btnBg);
            UIHelper.SetAnchors(startTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            startTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var extraTuple = CreateLegacyButton(lobbyPanelRoot.transform, "캐릭터", 260, 55, btnBg);
            UIHelper.SetAnchors(extraTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            extraTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var langTuple = CreateLegacyButton(lobbyPanelRoot.transform, "Language", 260, 55, btnBg);
            UIHelper.SetAnchors(langTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            langTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var settingsTuple = CreateLegacyButton(lobbyPanelRoot.transform, "환경 설정", 260, 55, btnBg);
            lobbySettingsBtnObj = settingsTuple.btn.gameObject;
            UIHelper.SetAnchors(settingsTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            settingsTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            langButtonRef = langTuple.btn;
            
            // Bottom text removed per user request

            // Version Text (Bottom Left)
            GameObject verObj = UIHelper.CreateUIObject("VersionText", lobbyPanelRoot.transform);
            RectTransform verRt = verObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(verRt, new Vector2(0, 0), new Vector2(0, 0), new Vector2(0, 0));
            verRt.anchoredPosition = new Vector2(20, 20);
            verRt.sizeDelta = new Vector2(300, 30);
            Text versionText = CreateLegacyText(verObj, "버전 1.0.2", new Color32(80, 80, 80, 255), 14, TextAnchor.MiddleCenter);

            // Events
            Button newGameBtn = startTuple.btn;
            Button continueBtn = loadTuple.btn;
            Button settingsBtn = settingsTuple.btn;

            // Attach LobbyUI
            LobbyUI lobbyUi = lobbyPanelRoot.AddComponent<LobbyUI>();
            UIHelper.SetField(lobbyUi, "lobbyPanel", lobbyPanelRoot);
            UIHelper.SetField(lobbyUi, "titleText", null); // Title text removed
            UIHelper.SetField(lobbyUi, "newGameButton", newGameBtn);
            UIHelper.SetField(lobbyUi, "continueButton", continueBtn);
            
            // Text references for translation
            UIHelper.SetField(lobbyUi, "newGameText", startTuple.text);
            UIHelper.SetField(lobbyUi, "continueText", loadTuple.text);
            UIHelper.SetField(lobbyUi, "extraText", extraTuple.text);
            UIHelper.SetField(lobbyUi, "settingsText", settingsTuple.text);
            UIHelper.SetField(lobbyUi, "lobbyTitleText", lobbyTitleText);
            UIHelper.SetField(lobbyUi, "versionText", versionText);

            settingsButtonRef = settingsBtn; // for CreateSettingsUI to attach

            // Extra button opens character profiles
            extraTuple.btn.onClick.AddListener(() => {
                if (extraUiRef != null) extraUiRef.Show();
            });
        }

        private (Button btn, TextMeshProUGUI btnText) CreateLobbyButton(Transform parent, string label, Vector2 pos, Color32 bgColor)
        {
            GameObject btnObj = UIHelper.CreateUIObject("LobbyBtn_" + label, parent);
            RectTransform rt = btnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            rt.anchoredPosition = pos;
            rt.sizeDelta = new Vector2(260, 55); // Increased size for visibility

            Image img = UIHelper.AddImage(btnObj, bgColor);

            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = bgColor;
            cb.highlightedColor = new Color32(255, 150, 40, 255); // Bright yellow-orange
            cb.pressedColor = new Color32(180, 60, 10, 255);      // Deep orange
            cb.colorMultiplier = 1f;
            cb.fadeDuration = 0.15f;
            btn.colors = cb;
            btn.targetGraphic = img;

            // Hover animation if present
            if (System.Type.GetType("HalloweenVN.UI.LobbyButtonHover") != null)
                btnObj.AddComponent<LobbyButtonHover>();

            GameObject textObj = UIHelper.CreateUIObject("Text", btnObj.transform);
            UIHelper.StretchFull(textObj.GetComponent<RectTransform>());
            TextMeshProUGUI text = UIHelper.AddText(textObj, label, Color.white, 24, TextAlignmentOptions.Center); // Increased font size
            text.fontStyle = FontStyles.Bold;

            return (btn, text);
        }

        /// <summary>
        /// Creates a character image slot using anchor-based positioning (ported from old project).
        /// anchorX: 0.2 for left, 0.5 for center, 0.8 for right
        /// </summary>
        private Image CreateCharacterSlot(string name, Transform parent, float anchorX)
        {
            GameObject obj = UIHelper.CreateUIObject(name, parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            // Span 90% of screen width centered on anchorX, from below screen to near top
            rt.anchorMin = new Vector2(anchorX - 0.45f, -0.6f);
            rt.anchorMax = new Vector2(anchorX + 0.45f, 0.95f);
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            
            Image image = UIHelper.AddImage(obj, new Color(1f, 1f, 1f, 0f));
            image.preserveAspect = true;
            image.raycastTarget = false;
            obj.SetActive(false); // Start hidden, DialogueUI will activate via FadeIn
            return image;
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
            
            Camera cam = Camera.main;
            if (cam == null)
            {
                GameObject camObj = new GameObject("Main Camera");
                camObj.tag = "MainCamera";
                cam = camObj.AddComponent<Camera>();
                cam.clearFlags = CameraClearFlags.SolidColor;
                cam.backgroundColor = Color.black;
            }
            
            mainCanvas.renderMode = RenderMode.ScreenSpaceCamera;
            mainCanvas.worldCamera = cam;
            mainCanvas.planeDistance = 100f; // Put UI in front of camera

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

            // Character Images (Left, Center, Right) — Anchor-based like old project
            Image characterImageLeft = CreateCharacterSlot("CharacterImageLeft", dialoguePanelRoot.transform, 0.2f);
            Image characterImageCenter = CreateCharacterSlot("CharacterImageCenter", dialoguePanelRoot.transform, 0.5f);
            Image characterImageRight = CreateCharacterSlot("CharacterImageRight", dialoguePanelRoot.transform, 0.8f);

            // Dialogue Panel
            GameObject dialoguePanel = UIHelper.CreatePanel("DialoguePanel", dialoguePanelRoot.transform, HalloweenTheme.PanelBackground);
            RectTransform panelRt = dialoguePanel.GetComponent<RectTransform>();
            UIHelper.SetBottom(panelRt, HalloweenTheme.DialoguePanelHeight);
            panelRt.offsetMin = new Vector2(180, 50); // padding reduced horizontal size
            panelRt.offsetMax = new Vector2(-180, HalloweenTheme.DialoguePanelHeight + 50);

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
            float btnW = 120, btnH = 40, btnSpacing = 10;
            
            var autoTuple = CreateLegacyButton(dialoguePanel.transform, "AUTO", btnW, btnH, new Color32(40, 25, 60, 255));
            RectTransform autoRt = autoTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            autoRt.anchoredPosition = new Vector2(-(btnW * 3 + btnSpacing * 2 + 10), -8);
            Text autoText = autoTuple.text;

            var skipTuple = CreateLegacyButton(dialoguePanel.transform, "SKIP", btnW, btnH, new Color32(40, 25, 60, 255));
            RectTransform skipRt = skipTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            skipRt.anchoredPosition = new Vector2(-(btnW * 2 + btnSpacing + 10), -8);

            var logTuple = CreateLegacyButton(dialoguePanel.transform, "LOG", btnW, btnH, new Color32(40, 25, 60, 255));
            RectTransform logRt = logTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(logRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            logRt.anchoredPosition = new Vector2(-(btnW + 10), -8);

            // Attach DialogueUI and wire fields
            DialogueUI ui = dialoguePanelRoot.AddComponent<DialogueUI>();
            UIHelper.SetField(ui, "dialoguePanel", dialoguePanel);
            UIHelper.SetField(ui, "speakerNameText", speakerName);
            UIHelper.SetField(ui, "dialogueText", dialogueText);
            UIHelper.SetField(ui, "characterImageLeft", characterImageLeft);
            UIHelper.SetField(ui, "characterImageCenter", characterImageCenter);
            UIHelper.SetField(ui, "characterImageRight", characterImageRight);
            UIHelper.SetField(ui, "backgroundImage", backgroundImage);
            
            UIHelper.SetField(ui, "choicePanel", choicePanel);
            UIHelper.SetField(ui, "choiceButtonPrefab", choiceButtonPrefab);
            UIHelper.SetField(ui, "choiceButtonContainer", choiceContainer.transform);
            UIHelper.SetField(ui, "autoButton", autoTuple.btn);
            UIHelper.SetField(ui, "skipButton", skipTuple.btn);
            UIHelper.SetField(ui, "backlogButton", logTuple.btn);
            UIHelper.SetField(ui, "autoButtonText", autoText);
            UIHelper.SetField(ui, "skipButtonText", skipTuple.text);
            UIHelper.SetField(ui, "backlogButtonText", logTuple.text);

            // Wire up fullscreen click (Background + DialoguePanel itself)
            Button bgClick = bgImgObj.AddComponent<Button>();
            bgClick.targetGraphic = backgroundImage;
            bgClick.transition = Selectable.Transition.None;
            Button panelClick = dialoguePanel.AddComponent<Button>();
            Image panelImg = dialoguePanel.GetComponent<Image>();
            if (panelImg != null) panelClick.targetGraphic = panelImg;
            panelClick.transition = Selectable.Transition.None;

            UnityEngine.Events.UnityAction onScreenClick = () => {
                var method = ui.GetType().GetMethod("OnClick", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
                if (method != null) method.Invoke(ui, null);
            };
            bgClick.onClick.AddListener(onScreenClick);
            panelClick.onClick.AddListener(onScreenClick);

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
            UIHelper.AddText(titleObj, "\uc5b8\uc5b4 \uc124\uc815", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);

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

            var closeTuple = CreateLegacyButton(detailPanel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
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

            // Semi-transparent dark overlay (now a button to close)
            GameObject bgBtnObj = UIHelper.CreateUIObject("BackgroundButton", settingsRoot.transform);
            UIHelper.StretchFull(bgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(bgBtnObj, new Color(0, 0, 0, 0.7f));
            UnityEngine.UI.Button bgBtn = bgBtnObj.AddComponent<UnityEngine.UI.Button>();
            bgBtn.transition = UnityEngine.UI.Selectable.Transition.None;

            // Settings panel
            GameObject panel = UIHelper.CreatePanel("SettingsPanel", settingsRoot.transform, HalloweenTheme.PanelBackground);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(700, 600);

            // Title
            GameObject titleObj = UIHelper.CreateUIObject("Title", panel.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleRt.anchoredPosition = new Vector2(0, -30);
            titleRt.sizeDelta = new Vector2(400, 40);
            Text titleText = CreateLegacyText(titleObj, "설정", HalloweenTheme.AccentOrange, 32, TextAnchor.UpperCenter);

            // Text Speed Slider
            float yPos = -70;
            var textSpeedLabel = CreateSettingsLabel(panel.transform, "텍스트 속도", yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos - 30);
            
            // Preview Text
            yPos -= 70;
            GameObject previewObj = UIHelper.CreateUIObject("PreviewText", panel.transform);
            RectTransform previewRt = previewObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(previewRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            previewRt.anchoredPosition = new Vector2(0, yPos);
            previewRt.sizeDelta = new Vector2(600, 40);
            Text previewText = CreateLegacyText(previewObj, "", HalloweenTheme.TextPrimary, 18, TextAnchor.MiddleCenter);
            

            // BGM Volume
            yPos -= 90;
            var bgmLabel = CreateSettingsLabel(panel.transform, "BGM", yPos);
            Slider bgmSlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // SFX Volume
            yPos -= 90;
            var sfxLabel = CreateSettingsLabel(panel.transform, "SFX", yPos);
            Slider sfxSlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // Delete Data Button
            var deleteTuple = CreateLegacyButton(panel.transform, "데이터 삭제", 200, 50, new Color32(180, 40, 40, 255));
            
            // Custom button color behavior for Delete Button
            UnityEngine.UI.ColorBlock delCb = deleteTuple.btn.colors;
            delCb.normalColor = new Color32(180, 40, 40, 255);       // Red normal
            delCb.highlightedColor = new Color32(180, 40, 40, 255);  // No hover reaction
            delCb.selectedColor = new Color32(180, 40, 40, 255);     // No focus reaction
            delCb.pressedColor = new Color32(120, 10, 10, 255);      // Deep red when pressed
            deleteTuple.btn.colors = delCb;
            
            // Remove hover script to ensure absolutely zero hover reaction
            Component hoverScript = deleteTuple.btn.GetComponent("LobbyButtonHover");
            if (hoverScript != null) UnityEngine.Object.Destroy(hoverScript);

            RectTransform deleteRt = deleteTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(deleteRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            deleteRt.anchoredPosition = new Vector2(-120, 40);

            // Close Button
            var closeTuple = CreateLegacyButton(panel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(120, 40);

            // Attach SettingsUI
            SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();
            settingsUiRef = settingsUi;
            bgBtn.onClick.AddListener(() => settingsUi.Hide());
            if (globalMgrRef != null) globalMgrRef.Initialize(settingsRoot);
            UIHelper.SetField(settingsUi, "settingsPanel", settingsRoot);
            UIHelper.SetField(settingsUi, "titleTextLabel", titleText);
            UIHelper.SetField(settingsUi, "textSpeedSlider", textSpeedSlider);
            UIHelper.SetField(settingsUi, "textSpeedLabel", textSpeedLabel);
            UIHelper.SetField(settingsUi, "previewTextLabel", previewText);
            UIHelper.SetField(settingsUi, "bgmVolumeSlider", bgmSlider);
            UIHelper.SetField(settingsUi, "bgmVolumeLabel", bgmLabel);
            UIHelper.SetField(settingsUi, "sfxVolumeSlider", sfxSlider);
            UIHelper.SetField(settingsUi, "sfxVolumeLabel", sfxLabel);
            UIHelper.SetField(settingsUi, "closeButtonText", closeTuple.text);
            UIHelper.SetField(settingsUi, "closeButton", closeTuple.btn);

            settingsRoot.SetActive(false);

            // Wire lobby settings button
            if (settingsButtonRef != null)
            {
                settingsButtonRef.onClick.AddListener(() => settingsUi.Show());
            }
        }

        private void CreateLanguageUI()
        {
            GameObject langRoot = UIHelper.CreateUIObject("LanguageRoot", mainCanvas.transform);
            UIHelper.StretchFull(langRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay (now a button to close)
            GameObject langBgBtnObj = UIHelper.CreateUIObject("BackgroundButton", langRoot.transform);
            UIHelper.StretchFull(langBgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(langBgBtnObj, new Color(0, 0, 0, 0.7f));
            UnityEngine.UI.Button langBgBtn = langBgBtnObj.AddComponent<UnityEngine.UI.Button>();
            langBgBtn.transition = UnityEngine.UI.Selectable.Transition.None;

            // Language panel
            GameObject panel = UIHelper.CreatePanel("LanguagePanel", langRoot.transform, HalloweenTheme.PanelBackground);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(500, 500);

            // Title
            GameObject titleObj = UIHelper.CreateUIObject("Title", panel.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleRt.anchoredPosition = new Vector2(0, -30);
            titleRt.sizeDelta = new Vector2(400, 40);
            UIHelper.AddText(titleObj, "\uc5b8\uc5b4 \uc124\uc815", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);

            // Buttons Container
            GameObject langContainer = UIHelper.CreateUIObject("LanguageContainer", panel.transform);
            RectTransform langRt = langContainer.GetComponent<RectTransform>();
            UIHelper.SetAnchors(langRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            langRt.anchoredPosition = new Vector2(0, -90);
            langRt.sizeDelta = new Vector2(300, 300);
            VerticalLayoutGroup vlg = langContainer.AddComponent<VerticalLayoutGroup>();
            vlg.childControlWidth = false;
            vlg.childControlHeight = false;
            vlg.childForceExpandWidth = false;
            vlg.childForceExpandHeight = false;
            vlg.childAlignment = TextAnchor.UpperCenter;
            vlg.spacing = 15;
            
            string[] langNames = { "한국어", "English", "日本語", "简体中文", "繁體中文" };
            Button[] langBtns = new Button[langNames.Length];
            for (int i = 0; i < langNames.Length; i++)
            {
                var btnTuple = CreateLegacyButton(langContainer.transform, langNames[i], 300, 45, HalloweenTheme.ButtonNormal);
                langBtns[i] = btnTuple.btn;
                
                // Disable color tint to preserve our manual coloring logic in LanguageUI
                btnTuple.btn.transition = Selectable.Transition.None;
            }

            // Close Button
            var closeTuple = CreateLegacyButton(panel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 40);

            // Attach LanguageUI
            LanguageUI langUi = langRoot.AddComponent<LanguageUI>();
            langBgBtn.onClick.AddListener(() => langUi.Hide());
            UIHelper.SetField(langUi, "panelRoot", langRoot);
            UIHelper.SetField(langUi, "languageButtons", langBtns);
            UIHelper.SetField(langUi, "closeButton", closeTuple.btn);
            UIHelper.SetField(langUi, "titleText", titleObj.GetComponent<TextMeshProUGUI>());
            UIHelper.SetField(langUi, "closeText", closeTuple.text);

            langRoot.SetActive(false);

            // Wire lobby language button
            if (langButtonRef != null)
            {
                langButtonRef.onClick.AddListener(() => langUi.Show());
            }
        }
        
        private (Button btn, Text text) CreateLegacyButton(Transform parent, string label, float width, float height, Color32 btnBg)
        {
            GameObject btnObj = UIHelper.CreateUIObject("Button_" + label, parent);
            RectTransform rt = btnObj.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(width, height);

            // Invisible hit box
            Image hitImg = UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));

            // Border (drawn behind)
            GameObject borderObj = UIHelper.CreateUIObject("Border", btnObj.transform);
            UIHelper.StretchFull(borderObj.GetComponent<RectTransform>());
            Image borderImg = UIHelper.AddImage(borderObj, HalloweenTheme.PanelBorder);
            borderImg.raycastTarget = false;

            // Background (drawn on top, shrunk to reveal border)
            GameObject bgObj = UIHelper.CreateUIObject("Background", btnObj.transform);
            RectTransform bgRt = bgObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(bgRt);
            bgRt.offsetMin = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);
            bgRt.offsetMax = new Vector2(-HalloweenTheme.PanelBorderWidth, -HalloweenTheme.PanelBorderWidth);
            Image bgImg = UIHelper.AddImage(bgObj, btnBg);
            bgImg.raycastTarget = false;

            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            btn.colors = HalloweenTheme.GetButtonColors();
            btn.targetGraphic = bgImg; // Only tint the inner background!

            GameObject textObj = UIHelper.CreateUIObject("Text", btnObj.transform);
            UIHelper.StretchFull(textObj.GetComponent<RectTransform>());
            
            Text legacyText = textObj.AddComponent<Text>();
            legacyText.text = label;
            legacyText.alignment = TextAnchor.MiddleCenter;
            legacyText.alignByGeometry = true;
            legacyText.verticalOverflow = VerticalWrapMode.Overflow;
            legacyText.fontSize = 20;
            legacyText.color = HalloweenTheme.ButtonText;
            
            // Assign standard OS font to prevent Chinese characters from breaking
            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo",
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans",
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC",
                "Arial Unicode MS", "sans-serif"
            };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, 20);
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");

            return (btn, legacyText);
        }

        private Text CreateLegacyText(GameObject obj, string text, Color color, int fontSize, TextAnchor alignment)
        {
            Text legacyText = obj.AddComponent<Text>();
            legacyText.text = text;
            legacyText.alignment = alignment;
            legacyText.fontSize = fontSize;
            legacyText.alignByGeometry = true;
            legacyText.verticalOverflow = VerticalWrapMode.Overflow;
            legacyText.color = color;

            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo", // Korean
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans", // Japanese
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", // Simplified Chinese
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", // Traditional Chinese
                "Arial Unicode MS", "sans-serif" // Fallbacks
            };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, fontSize);
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");

            return legacyText;
        }
        
        private Text CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(400, 25);
            return CreateLegacyText(obj, text, HalloweenTheme.TextPrimary, 18, TextAnchor.UpperLeft);
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
            
            // The actual panel that gets toggled
            GameObject backlogPanel = UIHelper.CreateUIObject("BacklogPanel", backlogRoot.transform);
            UIHelper.StretchFull(backlogPanel.GetComponent<RectTransform>());

            // Semi-transparent overlay
            UIHelper.AddImage(backlogPanel, new Color(0, 0, 0, 0.8f));

            // Scroll area
            GameObject scrollObj = UIHelper.CreateUIObject("ScrollView", backlogPanel.transform);
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
            GameObject titleObj = UIHelper.CreateUIObject("BacklogTitle", backlogPanel.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleRt.anchoredPosition = new Vector2(0, -25);
            titleRt.sizeDelta = new Vector2(400, 40);
            UIHelper.AddText(titleObj, "\uc5b8\uc5b4 \uc124\uc815", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);

            // Close button
            var closeTuple = CreateLegacyButton(backlogPanel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 30);

            // Attach BacklogUI
            backlogUiRef = backlogRoot.AddComponent<BacklogUI>();
            UIHelper.SetField(backlogUiRef, "backlogPanel", backlogPanel);
            UIHelper.SetField(backlogUiRef, "contentContainer", content.transform);
            UIHelper.SetField(backlogUiRef, "backlogEntryPrefab", entryPrefab);
            UIHelper.SetField(backlogUiRef, "closeButton", closeTuple.btn);
            UIHelper.SetField(backlogUiRef, "scrollRect", scrollRect);

            backlogPanel.SetActive(false);
        }

        private void CreateExtraUI()
        {
            // Root panel (fullscreen overlay, starts hidden)
            GameObject extraRoot = UIHelper.CreateUIObject("ExtraPanel", mainCanvas.transform);
            UIHelper.StretchFull(extraRoot.GetComponent<RectTransform>());
            extraRoot.SetActive(false);

            // Dark background (click to close)
            GameObject extraBgBtnObj = UIHelper.CreateUIObject("BackgroundButton", extraRoot.transform);
            UIHelper.StretchFull(extraBgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(extraBgBtnObj, new Color32(15, 8, 25, 200));
            UnityEngine.UI.Button extraBgBtn = extraBgBtnObj.AddComponent<UnityEngine.UI.Button>();
            extraBgBtn.transition = UnityEngine.UI.Selectable.Transition.None;

            // ===== Back shadow box (simulates folder stack depth) =====
            GameObject shadowBox = UIHelper.CreateUIObject("ShadowBox", extraRoot.transform);
            RectTransform shadowRt = shadowBox.GetComponent<RectTransform>();
            UIHelper.SetAnchors(shadowRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
            // Shadow box encompassing the entire diagonal stack (lowered and tightened)
            shadowRt.offsetMin = new Vector2(160, 0);
            shadowRt.offsetMax = new Vector2(-100, -170);
            Image shadowImg = UIHelper.AddImage(shadowBox, new Color32(80, 60, 40, 255));
            shadowImg.sprite = UIHelper.CreateRoundedRectSprite(10, 4, new Color32(80, 60, 40, 255), new Color32(60, 45, 25, 255));
            shadowImg.type = Image.Type.Sliced;

            // ===== Create 6 Folder objects =====
            string[] charNames = { "\uc138\uc774\uce74", "\uce74\uc2a4\ubbf8", "\ub9ac\ub098", "\ub9ac\ub9ac\uc2a4", "\ubbf8\ub098", "\ud558\ub8e8\uce74" };
            int folderCount = charNames.Length;

            // Folder colors
            Color32 folderBorder = new Color32(90, 65, 35, 255);
            Color32 folderBodyDefault = new Color32(210, 185, 140, 255);

            ExtraUI extraUi = extraRoot.AddComponent<ExtraUI>();
            extraBgBtn.onClick.AddListener(() => extraUi.Hide());
            UIHelper.SetField(extraUi, "extraPanel", extraRoot);
            UIHelper.SetField(extraUi, "globalSettingsButton", globalSettingsBtnObj);
            UIHelper.SetField(extraUi, "lobbySettingsButton", lobbySettingsBtnObj);

            for (int ci = 0; ci < folderCount; ci++)
            {
                // ===== Folder Root =====
                GameObject folder = UIHelper.CreateUIObject("Folder_" + charNames[ci], extraRoot.transform);
                // Insert right after the background and shadow box!
                folder.transform.SetSiblingIndex(2);
                
                RectTransform folderRt = folder.GetComponent<RectTransform>();
                UIHelper.SetAnchors(folderRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
                
                // Diagonal staircase: Shift UP by 8px and RIGHT by 8px (very tight overlap)
                // Base Y is lowered further to 10 and -220
                float xShift = ci * 8f;
                float yShift = ci * 8f;
                folderRt.offsetMin = new Vector2(150 + xShift, 10 + yShift);
                folderRt.offsetMax = new Vector2(-150 + xShift, -220 + yShift);

                // ===== Body (main content area) =====
                // Create body FIRST so it renders behind the tab
                GameObject bodyObj = UIHelper.CreateUIObject("Body", folder.transform);
                RectTransform bodyRt = bodyObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(bodyRt);

                Image bodyImg = UIHelper.AddImage(bodyObj, folderBodyDefault);
                // Body has square top corners so it perfectly aligns with the tabs!
                bodyImg.sprite = UIHelper.CreateCustomRoundedRectSprite(10, 4, Color.white, folderBorder, false, false, true, true);
                bodyImg.type = Image.Type.Sliced;

                // ===== Tab (upper protruding part of the folder) =====
                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                // Add extra width to tabs so they physically overlap each other!
                float tabRight = UnityEngine.Mathf.Min(1f, tabFraction * (ci + 1) + 0.03f);

                // TabContainer
                GameObject tabContainerObj = UIHelper.CreateUIObject("TabContainer", folder.transform);
                RectTransform tabContainerRt = tabContainerObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabContainerRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                
                // Determine horizontal offsets for flush edges on first and last tabs
                float leftOffset = (ci == 0) ? 0f : 3f;
                float rightOffset = (ci == folderCount - 1) ? 0f : -3f;
                
                // Sit flush with the body vertically
                tabContainerRt.anchoredPosition = new Vector2(0, 55);
                tabContainerRt.offsetMin = new Vector2(leftOffset, 0);
                tabContainerRt.offsetMax = new Vector2(rightOffset, 55);
                
                // Add invisible image to container to receive clicks
                UIHelper.AddImage(tabContainerObj, new Color(0, 0, 0, 0));

                // The actual Tab Image
                GameObject tabObj = UIHelper.CreateUIObject("Tab", tabContainerObj.transform);
                RectTransform tabRt = tabObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(tabRt);

                Image tabImg = UIHelper.AddImage(tabObj, folderBodyDefault);
                // Tab has square bottom corners to seamlessly connect to the Body!
                tabImg.sprite = UIHelper.CreateCustomRoundedRectSprite(8, 4, Color.white, folderBorder, true, true, false, false);
                tabImg.type = Image.Type.Sliced;

                // ===== Seam Hider =====
                // A solid block of color that covers the Tab's bottom horizontal border AND the Body's top horizontal border.
                GameObject seamObj = UIHelper.CreateUIObject("Seam", tabContainerObj.transform);
                RectTransform seamRt = seamObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(seamRt, new Vector2(0, 0), new Vector2(1, 0), new Vector2(0.5f, 0.5f));
                // Inset by 4px on both sides so we DO NOT cover the straight vertical borders!
                seamRt.offsetMin = new Vector2(4, -6);
                seamRt.offsetMax = new Vector2(-4, 6);
                
                Image seamImg = UIHelper.AddImage(seamObj, folderBodyDefault);

                // Tab text - Make it a child of TabContainer so it perfectly centers in the visible area!
                GameObject tabTextObj = UIHelper.CreateUIObject("Text", tabContainerObj.transform);
                RectTransform tabTextRt = tabTextObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(tabTextRt);
                // Shift text down slightly to the dead center (removed previous +5 upward bias)
                tabTextRt.offsetMin = new Vector2(0, 0);
                tabTextRt.offsetMax = new Vector2(0, 0);
                TextMeshProUGUI tabText = UIHelper.AddText(tabTextObj, charNames[ci], new Color32(60, 40, 20, 255), 18, TextAlignmentOptions.Center);
                tabText.fontStyle = FontStyles.Bold;

                // Tab click handler goes on the Container
                Button tabBtn = tabContainerObj.AddComponent<Button>();
                tabBtn.transition = Selectable.Transition.None;
                int capturedIndex = ci;
                tabBtn.onClick.AddListener(() => { extraUi.SelectCharacter(capturedIndex); });

                // ===== Portrait (left side) =====
                GameObject portraitObj = UIHelper.CreateUIObject("Portrait", bodyObj.transform);
                RectTransform portraitRt = portraitObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(portraitRt, new Vector2(0, 0), new Vector2(0.32f, 1), new Vector2(0.5f, 0.5f));
                portraitRt.offsetMin = new Vector2(30, 60);
                portraitRt.offsetMax = new Vector2(-20, -100);
                Image portraitImg = UIHelper.AddImage(portraitObj, new Color(1, 1, 1, 0));
                portraitImg.preserveAspect = true;

                // ===== Info panel (right side with scroll) =====
                GameObject infoPanelObj = UIHelper.CreateUIObject("Scroll", bodyObj.transform);
                RectTransform infoPanelRt = infoPanelObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(infoPanelRt, new Vector2(0.32f, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
                infoPanelRt.offsetMin = new Vector2(5, 10);
                infoPanelRt.offsetMax = new Vector2(-15, -10);

                ScrollRect scrollRect = infoPanelObj.AddComponent<ScrollRect>();
                scrollRect.horizontal = false;
                scrollRect.vertical = true;
                scrollRect.movementType = ScrollRect.MovementType.Clamped;
                UIHelper.AddImage(infoPanelObj, new Color(0, 0, 0, 0));

                // Viewport
                GameObject viewportObj = UIHelper.CreateUIObject("Viewport", infoPanelObj.transform);
                UIHelper.StretchFull(viewportObj.GetComponent<RectTransform>());
                viewportObj.AddComponent<RectMask2D>();

                // Content
                GameObject contentObj = UIHelper.CreateUIObject("Content", viewportObj.transform);
                RectTransform contentRt = contentObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(contentRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0, 1));
                contentRt.sizeDelta = new Vector2(0, 0);
                ContentSizeFitter fitter = contentObj.AddComponent<ContentSizeFitter>();
                fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

                scrollRect.viewport = viewportObj.GetComponent<RectTransform>();
                scrollRect.content = contentRt;

                // Name text
                GameObject nameObj = UIHelper.CreateUIObject("NameText", contentObj.transform);
                RectTransform nameRt = nameObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(nameRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0, 1));
                nameRt.sizeDelta = new Vector2(0, 50);
                TextMeshProUGUI nameText = UIHelper.AddText(nameObj, "", new Color32(60, 40, 20, 255), 28, TextAlignmentOptions.Left);
                nameText.fontStyle = FontStyles.Bold;
                nameText.margin = new Vector4(20, 20, 20, 0);

                // Profile text
                GameObject profileObj = UIHelper.CreateUIObject("ProfileText", contentObj.transform);
                RectTransform profileRt = profileObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(profileRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0, 1));
                profileRt.sizeDelta = new Vector2(0, 0);
                TextMeshProUGUI profileText = UIHelper.AddText(profileObj, "", new Color32(50, 40, 30, 255), 18, TextAlignmentOptions.TopLeft);
                profileText.textWrappingMode = TextWrappingModes.Normal;
                profileText.margin = new Vector4(20, 10, 20, 40);
                profileText.lineSpacing = 8f;

                // Layout
                VerticalLayoutGroup vlg = contentObj.AddComponent<VerticalLayoutGroup>();
                vlg.childForceExpandWidth = true;
                vlg.childForceExpandHeight = false;
                vlg.childControlWidth = true;
                vlg.childControlHeight = true;
                vlg.padding = new RectOffset(0, 0, 10, 20);

                LayoutElement profileLE = profileObj.AddComponent<LayoutElement>();
                profileLE.flexibleWidth = 1;
                LayoutElement nameLE = nameObj.AddComponent<LayoutElement>();
                nameLE.minHeight = 50;
                nameLE.flexibleWidth = 1;

                // Register folder with ExtraUI
                extraUi.RegisterFolder(folder, bodyImg, tabImg, tabText);
            }

            // ===== Header =====
            GameObject headerObj = UIHelper.CreateUIObject("Header", extraRoot.transform);
            RectTransform headerRt = headerObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(headerRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            headerRt.anchoredPosition = new Vector2(0, -20);
            headerRt.sizeDelta = new Vector2(0, 60);
            // Raycast blocker for header area
            UIHelper.AddImage(headerObj, new Color(0, 0, 0, 0));

            GameObject titleObj = UIHelper.CreateUIObject("Title", headerObj.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            titleRt.sizeDelta = new Vector2(400, 50);
            UIHelper.AddText(titleObj, "\uce90\ub9ad\ud130 \uc124\uc815\uc9d1", new Color32(210, 185, 140, 255), 30, TextAlignmentOptions.Center);

            // ===== Close Button =====
            GameObject closeBtnObj = UIHelper.CreateUIObject("CloseBtn", headerObj.transform);
            RectTransform closeRt = closeBtnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(1, 0.5f), new Vector2(1, 0.5f), new Vector2(1, 0.5f));
            closeRt.anchoredPosition = new Vector2(-40, 0);
            closeRt.sizeDelta = new Vector2(40, 40);
            Image closeBtnImg = UIHelper.AddImage(closeBtnObj, Color.white);
            closeBtnImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, new Color32(180, 50, 50, 255), new Color32(255, 120, 120, 255));
            closeBtnImg.type = Image.Type.Sliced;
            Button closeBtn = closeBtnObj.AddComponent<Button>();

            GameObject closeTextObj = UIHelper.CreateUIObject("Text", closeBtnObj.transform);
            RectTransform textRt = closeTextObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(textRt);
            textRt.offsetMin = new Vector2(0, 2);
            textRt.offsetMax = new Vector2(0, 2);
            UIHelper.AddText(closeTextObj, "X", Color.white, 24, TextAlignmentOptions.Center);


            UIHelper.SetField(extraUi, "closeButton", closeBtn);
            extraUiRef = extraUi;
        }

                private void CreateGlobalUI()
        {
            GameObject globalRoot = UIHelper.CreateUIObject("GlobalUI", mainCanvas.transform);
            UIHelper.StretchFull(globalRoot.GetComponent<RectTransform>());

            var globalMgr = globalRoot.AddComponent<GlobalUIManager>();
            globalMgrRef = globalMgr;

            // Settings Button (Top Right)
            GameObject btnObj = UIHelper.CreateUIObject("GlobalSettingsBtn", globalRoot.transform);
            globalSettingsBtnObj = btnObj;
            RectTransform btnRt = btnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(btnRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            btnRt.anchoredPosition = new Vector2(-20, -20);
            btnRt.sizeDelta = new Vector2(60, 60);

            // Button styling (Invisible hit box)
            Image btnImg = UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));
            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = Color.white;
            cb.highlightedColor = new Color32(200, 200, 200, 255); // Slightly gray on hover
            cb.pressedColor = new Color32(150, 150, 150, 255);     // Darker gray on click
            cb.selectedColor = Color.white;
            cb.colorMultiplier = 1f;
            cb.fadeDuration = 0.15f;
            btn.colors = cb;
            
            btn.onClick.AddListener(() => globalMgr.ToggleSettings());

            // Gear Icon
            GameObject iconObj = UIHelper.CreateUIObject("Icon", btnObj.transform);
            UIHelper.StretchFull(iconObj.GetComponent<RectTransform>());
            Text iconText = iconObj.AddComponent<Text>();
            iconText.text = "⚙"; // Gear emoji
            iconText.alignment = TextAnchor.MiddleCenter;
            iconText.alignByGeometry = true;
            iconText.fontSize = 40;
            iconText.color = Color.white;
            
            // Add black outline to the gear text
            UnityEngine.UI.Outline textOutline = iconObj.AddComponent<UnityEngine.UI.Outline>();
            textOutline.effectColor = new Color(0, 0, 0, 1);
            textOutline.effectDistance = new Vector2(2, -2);
            
            // Link text as target graphic so the gear itself reacts to hover/click!
            btn.targetGraphic = iconText;
            
            // Assign font
            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo",
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans",
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC",
                "Arial Unicode MS", "sans-serif"
            };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, 40);
            if (rawFont != null) iconText.font = rawFont;
            else iconText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
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
