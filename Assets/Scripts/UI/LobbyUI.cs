using System.Collections;
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

        private void OnEnable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
            }
            UpdateContinueButton();
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
            
            // X offset: 0 for show, -1920 for hide (sliding left)
            Vector2 startPos = rt.anchoredPosition;
            Vector2 targetPos = show ? Vector2.zero : new Vector2(-1920, 0);

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
                continueButton.interactable = SaveManager.HasSave(0);
            }
        }

        private void OnNewGameClicked()
        {
            ShowPhotosensitivityWarning();
        }

        private void ShowPhotosensitivityWarning()
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

            // Warning panel
            GameObject panel = new GameObject("WarningPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.anchorMin = new Vector2(0.5f, 0.5f);
            panelRt.anchorMax = new Vector2(0.5f, 0.5f);
            panelRt.sizeDelta = new Vector2(820, 500);
            Image panelImg = panel.AddComponent<Image>();
            panelImg.color = new Color32(25, 20, 35, 255);

            // --- Warning triangle icon (solid triangle with "!" cutout) ---
            float triW = 52f;
            float triH = 48f;
            float titleY = -52f;

            // Generate triangle texture with "!" negative space
            int texSize = 64;
            Texture2D triTex = new Texture2D(texSize, texSize, TextureFormat.RGBA32, false);
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
            TextMeshProUGUI iconText = iconObj.AddComponent<TextMeshProUGUI>();
            iconText.text = "광과민성 발작 경고";
            iconText.fontSize = 30;
            iconText.fontStyle = FontStyles.Bold;
            iconText.color = new Color32(255, 180, 80, 255);
            iconText.alignment = TextAlignmentOptions.Center;
            if (titleText != null && titleText.font != null) iconText.font = titleText.font;

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
            TextMeshProUGUI msgText = msgObj.AddComponent<TextMeshProUGUI>();
            msgText.text = "극소수의 사람들은 비디오 게임에 등장하는 " +
                           $"<b>{warn}번쩍이는 빛{warnEnd}</b>이나 " +
                           $"<b>{warn}특정 패턴{warnEnd}</b>과 같은 시각적 이미지에 노출될 때 " +
                           $"<b>{warn}광과민성 발작{warnEnd}</b>을 일으킬 수 있습니다. " +
                           "과거에 발작 병력이 없었더라도, 게임을 하는 동안 " +
                           "이러한 증상을 유발할 수 있는 미확인 상태일 수 있습니다.\n\n" +
                           $"게임 중 <b>{warn}현기증{warnEnd}</b>, <b>{warn}시력 이상{warnEnd}</b>, " +
                           $"<b>{warn}눈이나 얼굴의 경련{warnEnd}</b>, " +
                           $"<b>{warn}팔다리의 떨림{warnEnd}</b>, <b>{warn}방향 감각 상실{warnEnd}</b>, " +
                           $"<b>{warn}혼란{warnEnd}</b>, " +
                           $"또는 <b>{warn}일시적인 의식 상실{warnEnd}</b> 등의 증상을 겪는다면 " +
                           $"<b>{warn}즉시 게임을 중단{warnEnd}</b>하고 의사와 상담하십시오.";
            msgText.fontSize = 20;
            msgText.color = new Color32(200, 195, 210, 255);
            msgText.alignment = TextAlignmentOptions.Center;
            msgText.enableWordWrapping = true;
            msgText.lineSpacing = 8f;
            if (titleText != null && titleText.font != null) msgText.font = titleText.font;

            // OK button
            GameObject btnObj = new GameObject("ConfirmButton");
            btnObj.transform.SetParent(panel.transform, false);
            RectTransform btnRt = btnObj.AddComponent<RectTransform>();
            btnRt.anchorMin = new Vector2(0.5f, 0f);
            btnRt.anchorMax = new Vector2(0.5f, 0f);
            btnRt.anchoredPosition = new Vector2(0, 45);
            btnRt.sizeDelta = new Vector2(200, 50);
            Image btnImg = btnObj.AddComponent<Image>();
            btnImg.color = new Color32(80, 50, 120, 255);
            Button btn = btnObj.AddComponent<Button>();
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = new Color32(80, 50, 120, 255);
            cb.highlightedColor = new Color32(110, 70, 160, 255);
            cb.pressedColor = new Color32(150, 100, 50, 255);
            btn.colors = cb;
            btn.targetGraphic = btnImg;

            GameObject btnTextObj = new GameObject("ButtonText");
            btnTextObj.transform.SetParent(btnObj.transform, false);
            RectTransform btnTextRt = btnTextObj.AddComponent<RectTransform>();
            btnTextRt.anchorMin = Vector2.zero;
            btnTextRt.anchorMax = Vector2.one;
            btnTextRt.offsetMin = Vector2.zero;
            btnTextRt.offsetMax = Vector2.zero;
            TextMeshProUGUI btnText = btnTextObj.AddComponent<TextMeshProUGUI>();
            btnText.text = "확인";
            btnText.fontSize = 24;
            btnText.fontStyle = FontStyles.Bold;
            btnText.color = new Color32(255, 255, 255, 255);
            btnText.alignment = TextAlignmentOptions.Center;
            if (titleText != null && titleText.font != null) btnText.font = titleText.font;

            btn.onClick.AddListener(() =>
            {
                btn.interactable = false; // Prevent double-clicks during fade
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
                if (DialogueManager.Instance != null) DialogueManager.Instance.StartDialogue("ch0_opening");
            }
        }

        private IEnumerator DelayedNewGameRoutine(Theme.ScreenTransition transition, GameObject popupOverlay)
        {
            float fadeTime = 2.2f; // 0.3s faster than previous 2.5f
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
            if (DialogueManager.Instance != null) DialogueManager.Instance.StartDialogue("ch0_opening");
            
            transition.FadeIn(fadeTime, () => {
                transition.autoTransitionOnPhaseChange = true;
            });
        }

        private void OnContinueClicked()
        {
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
