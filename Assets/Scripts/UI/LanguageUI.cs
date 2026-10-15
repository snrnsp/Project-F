using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TMPro;
using HalloweenVN.Core;

namespace HalloweenVN.UI
{
    public class LanguageUI : MonoBehaviour
    {
        [SerializeField] private GameObject panelRoot;
        [SerializeField] private Button[] languageButtons;
        [SerializeField] private Button closeButton;
        [SerializeField] private Text titleText;
        [SerializeField] private Text closeText;

        private void OnEnable()
        {
            if (closeButton != null)
                closeButton.onClick.AddListener(Hide);

            if (languageButtons != null)
            {
                for (int i = 0; i < languageButtons.Length; i++)
                {
                    int index = i;
                    if (languageButtons[i] != null)
                    {
                        languageButtons[i].onClick.AddListener(() => SetLanguage((GameLanguage)index));
                    }
                }
            }

            UpdateLanguageButtonsUI();
        }

        private void OnDisable()
        {
            if (closeButton != null)
                closeButton.onClick.RemoveListener(Hide);

            if (languageButtons != null)
            {
                for (int i = 0; i < languageButtons.Length; i++)
                {
                    if (languageButtons[i] != null) 
                        languageButtons[i].onClick.RemoveAllListeners();
                }
            }
        }

        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
if (panelRoot != null)
            {
                panelRoot.SetActive(true);
                UpdateLanguageButtonsUI();
            }
        }

        public void Hide()
        {
            SettingsData.Save();
            if (panelRoot != null)
                panelRoot.SetActive(false);
        }

        private void SetLanguage(GameLanguage lang)
        {
            SettingsData.Language = lang;
            SettingsData.Save();

            LobbyUI lobby = Object.FindAnyObjectByType<LobbyUI>();
            if (lobby != null) lobby.UpdateLanguage();

            SettingsUI settings = Object.FindAnyObjectByType<SettingsUI>(FindObjectsInactive.Include);
            if (settings != null) settings.UpdateLanguage();

            DialogueUI dialogue = Object.FindAnyObjectByType<DialogueUI>(FindObjectsInactive.Include);
            if (dialogue != null) dialogue.UpdateLanguage();
            var extra = UnityEngine.Object.FindAnyObjectByType<ExtraUI>(UnityEngine.FindObjectsInactive.Include);
            if (extra != null) extra.UpdateLanguage();

            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(lang);
            var tmpFont = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            if (tmpFont != null)
            {
                var allTmp = Object.FindObjectsByType<TMPro.TextMeshProUGUI>(FindObjectsInactive.Include, FindObjectsSortMode.None);
                foreach (var tmp in allTmp)
                {
                    if (tmp != null)
                    {
                        tmp.font = tmpFont;
                    }
                }
            }

            var legacyFont = FontHelper.GetFont(fontName);
            if (legacyFont != null)
            {
                var allLegacy = Object.FindObjectsByType<UnityEngine.UI.Text>(FindObjectsInactive.Include, FindObjectsSortMode.None);
                foreach (var txt in allLegacy)
                {
                    if (txt != null)
                    {
                        txt.font = legacyFont;
                    }
                }
            }

            // Re-apply per-button fonts AFTER global refresh (so they don't get overwritten)
            UpdateLanguageButtonsUI();

            Debug.Log($"Language set to {lang}");
        }

        private Font GetLegacyFont(string name) => FontHelper.GetFont(name);

        private void UpdateLanguageButtonsUI()
        {
            if (titleText != null)
            {
                string fontName = FontHelper.GetFontNameForLanguage(SettingsData.Language);
                if (fontName != null) {
                    var f = FontHelper.GetFont(fontName);
                    if (f != null) titleText.font = f;
                }
                bool isGothic = !SettingsData.UseHandwritingFont;
                
                if (SettingsData.Language == GameLanguage.Korean) titleText.fontSize = isGothic ? 24 : 32;
                else titleText.fontSize = isGothic ? 22 : 28;
                
                titleText.text = Loc.Get("ui.language.title", "언어 설정");
            }
            if (closeText != null)
            {
                bool isGothic = !SettingsData.UseHandwritingFont;
                closeText.fontSize = isGothic ? 22 : 28;

                closeText.text = Loc.Get("ui.language.close", "닫기");
            }

            if (languageButtons == null) return;
            
            for (int i = 0; i < languageButtons.Length; i++)
            {
                if (languageButtons[i] == null) continue;
                
                Image img = languageButtons[i].targetGraphic as Image;
                TextMeshProUGUI txt = languageButtons[i].GetComponentInChildren<TextMeshProUGUI>();
                Text legacyTxt = languageButtons[i].GetComponentInChildren<Text>();
                
                if (legacyTxt != null) {
                    string btnFontName = FontHelper.GetFontNameForLanguage((GameLanguage)i);
                    Font f = FontHelper.GetFont(btnFontName);
                    if (f != null) legacyTxt.font = f;
                    
                    bool isGothic = !SettingsData.UseHandwritingFont;
                    if ((GameLanguage)i == GameLanguage.Korean) legacyTxt.fontSize = isGothic ? 24 : 33;
                    else legacyTxt.fontSize = isGothic ? 22 : 28;
                }
                
                if (txt != null) {
                    string btnFontName = FontHelper.GetFontNameForLanguage((GameLanguage)i);
                    var tmpBtnFont = FontHelper.GetTMPFont(btnFontName);
                    if (tmpBtnFont != null) txt.font = tmpBtnFont;
                    
                    bool isGothic = !SettingsData.UseHandwritingFont;
                    if ((GameLanguage)i == GameLanguage.Korean) txt.fontSize = isGothic ? 24 : 33;
                    else txt.fontSize = isGothic ? 22 : 28;
                }
                
                bool isSelected = ((int)SettingsData.Language == i);
                if (img != null) img.color = Color.white;

                languageButtons[i].transition = Selectable.Transition.ColorTint;
                ColorBlock cb = languageButtons[i].colors;
                if (isSelected)
                {
                    cb.normalColor = new Color32(225, 95, 20, 255);
                    cb.highlightedColor = new Color32(250, 125, 45, 255);
                    cb.pressedColor = new Color32(180, 70, 15, 255);
                    cb.selectedColor = cb.normalColor;
                }
                else
                {
                    cb.normalColor = new Color32(42, 26, 64, 255);
                    cb.highlightedColor = new Color32(82, 50, 120, 255);
                    cb.pressedColor = new Color32(120, 60, 25, 255);
                    cb.selectedColor = cb.normalColor;
                }
                cb.fadeDuration = 0.08f;
                languageButtons[i].colors = cb;

                Transform borderTr = languageButtons[i].transform.Find("Border");
                if (borderTr != null)
                {
                    Image borderImg = borderTr.GetComponent<Image>();
                    if (borderImg != null)
                    {
                        borderImg.color = isSelected
                            ? HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange
                            : (Color)new Color32(115, 75, 150, 255);
                    }
                }

                Color txtCol = isSelected ? Color.white : (Color)new Color32(215, 205, 225, 255);
                if (txt != null) txt.color = txtCol;
                if (legacyTxt != null) legacyTxt.color = txtCol;
            }
        }
    }
}