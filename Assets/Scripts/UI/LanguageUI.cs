﻿using UnityEngine;
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
        [SerializeField] private TextMeshProUGUI titleText;
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

        private void UpdateLanguageButtonsUI()
        {
            if (titleText != null)
            {
                if (SettingsData.Language == GameLanguage.English) titleText.text = "Language Settings";
                else if (SettingsData.Language == GameLanguage.Japanese) titleText.text = "言語設定";
                else if (SettingsData.Language == GameLanguage.ChineseSimplified) titleText.text = "语言设置";
                else if (SettingsData.Language == GameLanguage.ChineseTraditional) titleText.text = "語言設定";
                else titleText.text = "언어 설정";
            }
            if (closeText != null)
            {
                if (SettingsData.Language == GameLanguage.English) closeText.text = "Close";
                else if (SettingsData.Language == GameLanguage.Japanese) closeText.text = "閉じる";
                else if (SettingsData.Language == GameLanguage.ChineseSimplified) closeText.text = "关闭";
                else if (SettingsData.Language == GameLanguage.ChineseTraditional) closeText.text = "關閉";
                else closeText.text = "닫기";
            }

            if (languageButtons == null) return;
            
            for (int i = 0; i < languageButtons.Length; i++)
            {
                if (languageButtons[i] == null) continue;
                
                Image img = languageButtons[i].GetComponent<Image>();
                TextMeshProUGUI txt = languageButtons[i].GetComponentInChildren<TextMeshProUGUI>();
                Text legacyTxt = languageButtons[i].GetComponentInChildren<Text>();
                
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
                    if (legacyTxt != null) legacyTxt.color = new Color32(180, 180, 180, 255);
                }
            }
        }
    }
}

