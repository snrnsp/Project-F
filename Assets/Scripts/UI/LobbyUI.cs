﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using HalloweenVN.Core;
using HalloweenVN.Dialogue;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Manages the lobby (title) screen UI.
    /// </summary>
    public class LobbyUI : MonoBehaviour
    {
        [SerializeField] private GameObject lobbyPanel;
        [SerializeField] private TextMeshProUGUI titleText;
        [SerializeField] private TextMeshProUGUI subtitleText;
        [SerializeField] private Button newGameButton;
        [SerializeField] private Button continueButton;

        // Added for translation
        [SerializeField] private Text newGameText;
        [SerializeField] private Text continueText;
        [SerializeField] private Text extraText;
        [SerializeField] private Text settingsText;
        [SerializeField] private Text versionText;
        [SerializeField] private Text lobbyTitleText;
        private bool isStartingGame = false;

        private void OnEnable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
            }
            UpdateContinueButton();
            UpdateLanguage();
        }

        public void UpdateLanguage()
        {
            if (newGameText == null) return;

            GameLanguage lang = SettingsData.Language;

            // Korean (Default)
            if (lang == GameLanguage.Korean)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "오블리비언\n<size=22>OBLIVION</size>";
                newGameText.text = "새 게임";
                extraText.text = "캐릭터";
                settingsText.text = "환경 설정";
                if (versionText != null) versionText.text = "버전 1.0.2";
            }
            // English
            else if (lang == GameLanguage.English)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "OBLIVION";
                newGameText.text = "New Game";
                extraText.text = "Character";
                settingsText.text = "Settings";
                if (versionText != null) versionText.text = "Ver 1.0.2";
            }
            // Japanese
            else if (lang == GameLanguage.Japanese)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "オブリビオン\n<size=22>OBLIVION</size>";
                newGameText.text = "初めから";
                extraText.text = "キャラクター";
                settingsText.text = "設定";
                if (versionText != null) versionText.text = "バージョン 1.0.2";
            }
            // Simplified Chinese
            else if (lang == GameLanguage.ChineseSimplified)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "遗忘\n<size=22>OBLIVION</size>";
                newGameText.text = "新游戏";
                extraText.text = "角色";
                settingsText.text = "设置";
                if (versionText != null) versionText.text = "版本 1.0.2";
            }
            // Traditional Chinese
            else if (lang == GameLanguage.ChineseTraditional)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "遺忘\n<size=22>OBLIVION</size>";
                newGameText.text = "新遊戲";
                extraText.text = "額外內容";
                settingsText.text = "設定";
                if (versionText != null) versionText.text = "版本 1.0.2";
            }
        }

        private void Start()
        {
            if (newGameButton != null)
            {
                newGameButton.onClick.AddListener(OnNewGameClicked);
            }
            if (continueButton != null)
            {
                continueButton.onClick.AddListener(OnContinueClicked);
            }
            UpdateContinueButton();
        }

        private void OnDisable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
            }
        }

        private void OnDestroy()
        {
            if (newGameButton != null)
            {
                newGameButton.onClick.RemoveListener(OnNewGameClicked);
            }
            if (continueButton != null)
            {
                continueButton.onClick.RemoveListener(OnContinueClicked);
            }
        }

        private Sprite CreateRoundedRectSprite(int radius, int borderSize, Color32 bgColor, Color32 borderColor)
        {
            int size = radius * 2 + borderSize * 2 + 4; // Add a bit of padding for safe slicing
            int centerStart = radius + borderSize;
            int centerEnd = centerStart + 3;
            
            Texture2D tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.wrapMode = TextureWrapMode.Clamp;
            Color32 clear = new Color32(0, 0, 0, 0);
            
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    float dx = Mathf.Max(0, Mathf.Max(centerStart - x, x - centerEnd));
                    float dy = Mathf.Max(0, Mathf.Max(centerStart - y, y - centerEnd));
                    float dist = Mathf.Sqrt(dx * dx + dy * dy);
                    
                    if (dist > radius + borderSize) tex.SetPixel(x, y, clear);
                    else if (dist > radius) tex.SetPixel(x, y, borderColor);
                    else tex.SetPixel(x, y, bgColor);
                }
            }
            tex.Apply();
            return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100, 0, SpriteMeshType.FullRect, new Vector4(centerStart, centerStart, centerStart, centerStart));
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            if (lobbyPanel == null) return;

            if (phase == GamePhase.Lobby)
            {
                lobbyPanel.SetActive(true);
                UpdateContinueButton();
                StopAllCoroutines();
                StartCoroutine(SlideLobby(true));
            }
            else
            {
                StopAllCoroutines();
                StartCoroutine(SlideLobby(false));
            }
        }

        private System.Collections.IEnumerator SlideLobby(bool show)
        {
            RectTransform rt = lobbyPanel.GetComponent<RectTransform>();
            float duration = 0.5f;
            float time = 0f;
            
            // X offset: 0 for show, -canvasWidth for hide (sliding left, resolution-independent)
            Vector2 startPos = rt.anchoredPosition;
            float canvasWidth = rt.rect.width > 0 ? rt.rect.width : 1920f;
            Vector2 targetPos = show ? Vector2.zero : new Vector2(-canvasWidth, 0);

            while (time < duration)
            {
                time += Time.deltaTime;
                float t = Mathf.SmoothStep(0, 1, time / duration);
                rt.anchoredPosition = Vector2.Lerp(startPos, targetPos, t);
                yield return null;
            }
            rt.anchoredPosition = targetPos;

            if (!show)
            {
                lobbyPanel.SetActive(false);
            }
        }

        /// <summary>
        /// Shows or hides the continue button based on save data availability.
        /// </summary>
        private void UpdateContinueButton()
        {
            if (continueButton != null)
            {
                // 사용자가 로드 버튼이 유독 연하게 보이는 것을 원치 않으므로 시각적 통일성을 위해 항상 활성화 상태 유지
                continueButton.interactable = true;
                
                CanvasGroup cg = continueButton.GetComponent<CanvasGroup>();
                if (cg != null) cg.alpha = 1f;
            }
        }

        private void OnNewGameClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            ShowPreAlphaWarning();
        }

        private void ShowPreAlphaWarning()
        {
            GameObject overlay = new GameObject("PreAlphaOverlay");
            overlay.transform.SetParent(lobbyPanel.transform.parent, false);
            RectTransform overlayRt = overlay.AddComponent<RectTransform>();
            overlayRt.anchorMin = Vector2.zero;
            overlayRt.anchorMax = Vector2.one;
            overlayRt.offsetMin = Vector2.zero;
            overlayRt.offsetMax = Vector2.zero;
            Image overlayImg = overlay.AddComponent<Image>();
            overlayImg.color = new Color(0, 0, 0, 0.85f);
            
            Button overlayBtn = overlay.AddComponent<Button>();
            overlayBtn.transition = Selectable.Transition.None;
            overlayBtn.onClick.AddListener(() => {
                Destroy(overlay);
            });

            GameObject panel = new GameObject("WarningPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.anchorMin = new Vector2(0.5f, 0.5f);
            panelRt.anchorMax = new Vector2(0.5f, 0.5f);
            panelRt.sizeDelta = new Vector2(820, 450);
            Image panelImg = panel.AddComponent<Image>();
            panelImg.type = Image.Type.Sliced;
            panelImg.sprite = CreateRoundedRectSprite(16, 2, new Color32(25, 20, 35, 255), new Color32(100, 180, 255, 255));
            
            Button panelDummyBtn = panel.AddComponent<Button>();
            panelDummyBtn.transition = Selectable.Transition.None;

            float titleY = -60f;

            GameObject iconObj = new GameObject("PreAlphaTitle");
            iconObj.transform.SetParent(panel.transform, false);
            RectTransform iconRt = iconObj.AddComponent<RectTransform>();
            iconRt.anchorMin = new Vector2(0.5f, 1f);
            iconRt.anchorMax = new Vector2(0.5f, 1f);
            iconRt.anchoredPosition = new Vector2(0, titleY);
            iconRt.sizeDelta = new Vector2(500, 45);
            TextMeshProUGUI iconText = Theme.UIHelper.AddText(iconObj, "Pre-Alpha 안내", new Color32(150, 200, 255, 255), 30, TextAlignmentOptions.Center);
            iconText.fontStyle = FontStyles.Bold;

            GameObject msgObj = new GameObject("WarningMessage");
            msgObj.transform.SetParent(panel.transform, false);
            RectTransform msgRt = msgObj.AddComponent<RectTransform>();
            msgRt.anchorMin = new Vector2(0.5f, 1f);
            msgRt.anchorMax = new Vector2(0.5f, 1f);
            msgRt.anchoredPosition = new Vector2(0, -180);
            msgRt.sizeDelta = new Vector2(720, 200);
            
            string preAlphaMsg = "현재 오블리비언은 '<color=#80C0FF>프리 알파</color>(소프트웨어나 게임 개발 과정에서 정식 알파 테스트 이전의 초기 제작 및 설계 단계)'에 있습니다!\n\n게임의 품질이 낮을 수 있는 점 양해 바랍니다!";
            
            TextMeshProUGUI msgText = Theme.UIHelper.AddText(msgObj, preAlphaMsg, new Color32(230, 230, 230, 255), 24, TextAlignmentOptions.Center);
            msgText.lineSpacing = 15f;

            GameObject btnObj = new GameObject("OkButton");
            btnObj.transform.SetParent(panel.transform, false);
            RectTransform btnRt = btnObj.AddComponent<RectTransform>();
            btnRt.anchorMin = new Vector2(0.5f, 0f);
            btnRt.anchorMax = new Vector2(0.5f, 0f);
            btnRt.anchoredPosition = new Vector2(0, 70);
            btnRt.sizeDelta = new Vector2(240, 60);
            Image btnImg = btnObj.AddComponent<Image>();
            btnImg.type = Image.Type.Sliced;
            btnImg.sprite = CreateRoundedRectSprite(8, 0, new Color32(50, 100, 160, 255), new Color32(0, 0, 0, 0));
            
            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            var cb = btn.colors;
            cb.normalColor = Color.white;
            cb.highlightedColor = new Color(0.8f, 0.9f, 1f);
            cb.pressedColor = new Color(0.6f, 0.8f, 1f);
            cb.selectedColor = Color.white;
            btn.colors = cb;

            GameObject btnTextObj = new GameObject("Text");
            btnTextObj.transform.SetParent(btnObj.transform, false);
            RectTransform btnTextRt = btnTextObj.AddComponent<RectTransform>();
            btnTextRt.anchorMin = Vector2.zero;
            btnTextRt.anchorMax = Vector2.one;
            btnTextRt.offsetMin = Vector2.zero;
            btnTextRt.offsetMax = Vector2.zero;
            TextMeshProUGUI btnText = Theme.UIHelper.AddText(btnTextObj, "확인", new Color32(255, 255, 255, 255), 28, TextAlignmentOptions.Center);
            btnText.fontStyle = FontStyles.Bold;

            btn.onClick.AddListener(() =>
            {
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                Destroy(overlay);
                ShowPhotosensitivityWarning();
            });
        }
void ShowPhotosensitivityWarning()
        {
            // Create overlay
            GameObject overlay = new GameObject("WarningOverlay");
            overlay.transform.SetParent(lobbyPanel.transform.parent, false);
            RectTransform overlayRt = overlay.AddComponent<RectTransform>();
            overlayRt.anchorMin = Vector2.zero;
            overlayRt.anchorMax = Vector2.one;
            overlayRt.offsetMin = Vector2.zero;
            overlayRt.offsetMax = Vector2.zero;
            Image overlayImg = overlay.AddComponent<Image>();
            overlayImg.color = new Color(0, 0, 0, 0.85f);
            
            // Add button to overlay to cancel/close the warning popup
            Button overlayBtn = overlay.AddComponent<Button>();
            overlayBtn.transition = Selectable.Transition.None;
            overlayBtn.onClick.AddListener(() => {
                Destroy(overlay);
            });

            // Warning panel
            GameObject panel = new GameObject("WarningPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.anchorMin = new Vector2(0.5f, 0.5f);
            panelRt.anchorMax = new Vector2(0.5f, 0.5f);
            panelRt.sizeDelta = new Vector2(820, 500);
            Image panelImg = panel.AddComponent<Image>();
            panelImg.type = Image.Type.Sliced;
            panelImg.sprite = CreateRoundedRectSprite(16, 2, new Color32(25, 20, 35, 255), new Color32(255, 180, 50, 255));
            
            // Add a dummy button to the panel to absorb clicks so they don't bubble up to the overlay button
            Button panelDummyBtn = panel.AddComponent<Button>();
            panelDummyBtn.transition = Selectable.Transition.None;

            // --- Warning triangle icon (solid triangle with "!" cutout) ---
            float triW = 52f;
            float triH = 48f;
            float titleY = -75f;

            // Generate triangle texture with "!" negative space
            int texSize = 64;
            Texture2D triTex = new Texture2D(texSize, texSize, TextureFormat.RGBA32, false);
            triTex.wrapMode = TextureWrapMode.Clamp;
            Color clear = new Color(0, 0, 0, 0);
            Color fill = Color.white;
            float cx = texSize * 0.5f;
            // "!" cutout dimensions (in texture pixels)
            float barHalfW = 2.5f;
            float barTop = texSize * 0.72f;   // bar starts high
            float barBot = texSize * 0.32f;    // bar ends here
            float dotTop = texSize * 0.24f;    // dot top
            float dotBot = texSize * 0.15f;    // dot bottom
            float dotHalfW = 2.5f;

            for (int y = 0; y < texSize; y++)
            {
                for (int x = 0; x < texSize; x++)
                {
                    // Triangle: apex up, wide at bottom
                    float progress = (float)y / texSize;
                    float halfW = (1f - progress) * texSize * 0.5f;
                    bool inTriangle = (x >= cx - halfW && x <= cx + halfW);

                    if (!inTriangle)
                    {
                        triTex.SetPixel(x, y, clear);
                        continue;
                    }

                    // Check if pixel is inside "!" cutout
                    bool inBar = (x >= cx - barHalfW && x <= cx + barHalfW && y >= barBot && y <= barTop);
                    bool inDot = (x >= cx - dotHalfW && x <= cx + dotHalfW && y >= dotBot && y <= dotTop);

                    triTex.SetPixel(x, y, (inBar || inDot) ? clear : fill);
                }
            }
            triTex.Apply();
            Sprite triSprite = Sprite.Create(triTex, new Rect(0, 0, texSize, texSize), new Vector2(0.5f, 0.5f));

            // Warning triangle
            GameObject triObj = new GameObject("WarningTriangle");
            triObj.transform.SetParent(panel.transform, false);
            RectTransform triRt = triObj.AddComponent<RectTransform>();
            triRt.anchorMin = new Vector2(0.5f, 1f);
            triRt.anchorMax = new Vector2(0.5f, 1f);
            triRt.anchoredPosition = new Vector2(-170, titleY);
            triRt.sizeDelta = new Vector2(triW, triH);
            Image triImg = triObj.AddComponent<Image>();
            triImg.sprite = triSprite;
            triImg.color = new Color32(255, 180, 50, 255);
            triImg.raycastTarget = false;

            // Title text (to the right of the triangle)
            GameObject iconObj = new GameObject("WarningTitle");
            iconObj.transform.SetParent(panel.transform, false);
            RectTransform iconRt = iconObj.AddComponent<RectTransform>();
            iconRt.anchorMin = new Vector2(0.5f, 1f);
            iconRt.anchorMax = new Vector2(0.5f, 1f);
            iconRt.anchoredPosition = new Vector2(15, titleY);
            iconRt.sizeDelta = new Vector2(500, 45);
            TextMeshProUGUI iconText = Theme.UIHelper.AddText(iconObj, "광과민성 발작 경고", new Color32(255, 180, 80, 255), 30, TextAlignmentOptions.Center);
            iconText.fontStyle = FontStyles.Bold;

            // Warning message — use color tags for stronger emphasis
            string warn = "<color=#FFD080>";
            string warnEnd = "</color>";
            GameObject msgObj = new GameObject("WarningMessage");
            msgObj.transform.SetParent(panel.transform, false);
            RectTransform msgRt = msgObj.AddComponent<RectTransform>();
            msgRt.anchorMin = new Vector2(0, 0.13f);
            msgRt.anchorMax = new Vector2(1, 0.82f);
            msgRt.offsetMin = new Vector2(45, 0);
            msgRt.offsetMax = new Vector2(-45, 0);
            TextMeshProUGUI msgText = Theme.UIHelper.AddText(msgObj,
                "극소수의 사람들은 비디오 게임에 등장하는 " +
                $"<b>{warn}번쩍이는 빛{warnEnd}</b>이나 " +
                $"<b>{warn}특정 패턴{warnEnd}</b>과 같은 시각적 이미지에 노출될 때 " +
                $"<b>{warn}광과민성 발작{warnEnd}</b>을 일으킬 수 있습니다. " +
                "과거에 발작 병력이 없었더라도 게임을 하는 동안 " +
                "이러한 증상을 유발할 수 있는 미확인 상태일 수 있습니다. " +
                $"게임 중 <b>{warn}현기증{warnEnd}</b>, <b>{warn}시력 이상{warnEnd}</b>, " +
                $"<b>{warn}눈이나 얼굴의 경련{warnEnd}</b>, " +
                $"<b>{warn}팔다리의 떨림{warnEnd}</b>, <b>{warn}방향 감각 상실{warnEnd}</b>, " +
                $"<b>{warn}혼란{warnEnd}</b>, " +
                $"또는 <b>{warn}일시적인 의식 상실{warnEnd}</b> 등의 증상을 겪는다면 " +
                $"<b>{warn}즉시 게임을 중단{warnEnd}</b>하고 의사와 상담하십시오.",
                new Color32(200, 195, 210, 255), 20, TextAlignmentOptions.Center);
            msgText.textWrappingMode = TextWrappingModes.Normal;
            msgText.lineSpacing = 8f;
            msgText.richText = true;

            // OK button
            GameObject btnObj = new GameObject("ConfirmButton");
            btnObj.transform.SetParent(panel.transform, false);
            RectTransform btnRt = btnObj.AddComponent<RectTransform>();
            btnRt.anchorMin = new Vector2(0.5f, 0f);
            btnRt.anchorMax = new Vector2(0.5f, 0f);
            btnRt.anchoredPosition = new Vector2(0, 70);
            btnRt.sizeDelta = new Vector2(200, 50);
            // Invisible hitbox
            Image hitImg = Theme.UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));

            // Border
            GameObject borderObj = new GameObject("Border");
            borderObj.transform.SetParent(btnObj.transform, false);
            RectTransform borderRt = borderObj.AddComponent<RectTransform>();
            borderRt.anchorMin = Vector2.zero;
            borderRt.anchorMax = Vector2.one;
            borderRt.offsetMin = Vector2.zero;
            borderRt.offsetMax = Vector2.zero;
            Image borderImg = Theme.UIHelper.AddImage(borderObj, new Color32(255, 150, 40, 255)); // Orange border
            borderImg.raycastTarget = false;

            // Background
            GameObject bgObj = new GameObject("Background");
            bgObj.transform.SetParent(btnObj.transform, false);
            RectTransform bgRt = bgObj.AddComponent<RectTransform>();
            bgRt.anchorMin = Vector2.zero;
            bgRt.anchorMax = Vector2.one;
            bgRt.offsetMin = new Vector2(6, 6);
            bgRt.offsetMax = new Vector2(-6, -6);
            Image bgImg = Theme.UIHelper.AddImage(bgObj, new Color32(80, 50, 120, 255));
            bgImg.raycastTarget = false;

            Button btn = btnObj.AddComponent<Button>();
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = Color.white;
            cb.highlightedColor = new Color32(200, 200, 200, 255);
            cb.pressedColor = new Color32(150, 150, 150, 255);
            btn.colors = cb;
            btn.targetGraphic = bgImg;

            GameObject btnTextObj = new GameObject("ButtonText");
            btnTextObj.transform.SetParent(btnObj.transform, false);
            RectTransform btnTextRt = btnTextObj.AddComponent<RectTransform>();
            btnTextRt.anchorMin = Vector2.zero;
            btnTextRt.anchorMax = Vector2.one;
            btnTextRt.offsetMin = Vector2.zero;
            btnTextRt.offsetMax = Vector2.zero;
            TextMeshProUGUI btnText = Theme.UIHelper.AddText(btnTextObj, "확인", new Color32(255, 255, 255, 255), 28, TextAlignmentOptions.Center);
            btnText.fontStyle = FontStyles.Bold;

            btn.onClick.AddListener(() =>
            {
                if (isStartingGame) return;
                isStartingGame = true;
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                
                // We do NOT set interactable = false here because it causes the button to permanently stay gray (disabled color)
                // during the long 2.2s fade out. The isStartingGame flag prevents double clicks instead.
                StartNewGame(overlay);
            });
        }

        private void StartNewGame(GameObject popupOverlay)
        {
            Theme.ScreenTransition transition = FindFirstObjectByType<Theme.ScreenTransition>();
            if (transition != null)
            {
                // Run the coroutine on the transition object so it survives LobbyUI deactivation
                transition.StartCoroutine(DelayedNewGameRoutine(transition, popupOverlay));
            }
            else
            {
                if (popupOverlay != null) Destroy(popupOverlay);
                
                if (GameManager.Instance != null) GameManager.Instance.ChangePhase(GamePhase.Dialogue);
                if (DialogueManager.Instance != null) DialogueManager.Instance.StartDialogue("ch0_origin");
            }
        }

        private IEnumerator DelayedNewGameRoutine(Theme.ScreenTransition transition, GameObject popupOverlay)
        {
            float fadeTime = 1.7f; // 0.5s faster than previous 2.2f
            float waitTime = 2.0f; // 2 seconds wait on black screen

            transition.autoTransitionOnPhaseChange = false;
            
            bool fadeOutDone = false;
            transition.FadeOut(fadeTime, () => fadeOutDone = true);
            
            // Wait for fade out to complete
            yield return new WaitUntil(() => fadeOutDone);
            
            // Screen is completely black here
            if (popupOverlay != null) Destroy(popupOverlay);
            if (GameManager.Instance != null) GameManager.Instance.ChangePhase(GamePhase.Dialogue);
            
            // Wait 2 seconds in darkness
            yield return new WaitForSeconds(waitTime);
            
            // Start the story and fade back in using the same fadeTime
            if (DialogueManager.Instance != null) DialogueManager.Instance.StartDialogue("ch0_origin");
            
            transition.FadeIn(fadeTime, () => {
                transition.autoTransitionOnPhaseChange = true;
            });
        }

        private void OnContinueClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            SaveData data = SaveManager.Load(0);
            if (data != null && GameManager.Instance != null)
            {
                if (System.Enum.TryParse(data.currentPhase, out GamePhase phase))
                {
                    GameManager.Instance.ChangePhase(phase);
                }
                if (!string.IsNullOrEmpty(data.currentDialogueId) && DialogueManager.Instance != null)
                {
                    DialogueManager.Instance.StartDialogue(data.currentDialogueId);
                }
            }
        }
    }
}
