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
            UpdateLanguageButtonsUI();
            
            LobbyUI lobby = Object.FindAnyObjectByType<LobbyUI>();
            if (lobby != null) lobby.UpdateLanguage();
            
            SettingsUI settings = Object.FindAnyObjectByType<SettingsUI>(FindObjectsInactive.Include);
            if (settings != null) settings.UpdateLanguage();

            DialogueUI dialogue = Object.FindAnyObjectByType<DialogueUI>(FindObjectsInactive.Include);
            if (dialogue != null) dialogue.UpdateLanguage();
            
            Debug.Log($"Language set to {lang}");
        }

        
        private static System.Collections.Generic.Dictionary<string, Font> _legacyFontCache = new System.Collections.Generic.Dictionary<string, Font>();
        private Font GetLegacyFont(string name) {
            if (string.IsNullOrEmpty(name)) return null;
            if (_legacyFontCache.ContainsKey(name)) return _legacyFontCache[name];
            Font rawFont = Resources.Load<Font>("Fonts/" + name);
            if (rawFont != null) _legacyFontCache[name] = rawFont;
            return rawFont;
        }

        private void UpdateLanguageButtonsUI()
        {
            if (titleText != null)
            {
                string fontName = FontHelper.GetFontNameForLanguage(SettingsData.Language);
                if (fontName != null) {
                    var f = FontHelper.GetFont(fontName);
                    if (f != null) titleText.font = f;
                }
                if (SettingsData.Language == GameLanguage.Korean) titleText.fontSize = 32;
                else titleText.fontSize = 28;
                
                if (SettingsData.Language == GameLanguage.English) titleText.text = "Language Settings";
                else if (SettingsData.Language == GameLanguage.Japanese) titleText.text = "\u8A00\u8A9E\u8A2D\u5B9A";
                else if (SettingsData.Language == GameLanguage.ChineseSimplified) titleText.text = "\u8BED\u8A00\u8BBE\u7F6E";
                else if (SettingsData.Language == GameLanguage.ChineseTraditional) titleText.text = "\u8A9E\u8A00\u8A2D\u5B9A";
                else titleText.text = "\uC5B8\uC5B4 \uC124\uC815";
            }
            if (closeText != null)
            {
                if (SettingsData.Language == GameLanguage.English) closeText.text = "Close";
                else if (SettingsData.Language == GameLanguage.Japanese) closeText.text = "\u9589\u3058\u308B";
                else if (SettingsData.Language == GameLanguage.ChineseSimplified) closeText.text = "\u5173\u95ED";
                else if (SettingsData.Language == GameLanguage.ChineseTraditional) closeText.text = "\u95DC\u9589";
                else closeText.text = "\uB2EB\uAE30";
            }

            if (languageButtons == null) return;
            
            for (int i = 0; i < languageButtons.Length; i++)
            {
                if (languageButtons[i] == null) continue;
                
                Image img = languageButtons[i].GetComponent<Image>();
                TextMeshProUGUI txt = languageButtons[i].GetComponentInChildren<TextMeshProUGUI>();
                Text legacyTxt = languageButtons[i].GetComponentInChildren<Text>();
                
                if (legacyTxt != null) {
                    string btnFontName = FontHelper.GetFontNameForLanguage((GameLanguage)i);
                    Font f = FontHelper.GetFont(btnFontName);
                    if (f != null) legacyTxt.font = f;
                    
                    if ((GameLanguage)i == GameLanguage.Korean) legacyTxt.fontSize = 33;
                    else legacyTxt.fontSize = 28;
                }
                
                if ((int)SettingsData.Language == i)
                {
                    if (img != null) img.color = new Color32(230, 100, 20, 255); // Orange
                    if (txt != null) txt.color = Color.white;
                    if (legacyTxt != null) legacyTxt.color = Color.white;
                }
                else
                {
                    if (img != null) img.color = new Color32(40, 25, 60, 255); // Dark Purple
                    if (txt != null) txt.color = new Color32(180, 180, 180, 255); // Grey
                    if (legacyTxt != null) legacyTxt.color = new Color32(180, 180, 180, 255); // Grey
                }
            }
        }
    }
}