import os
import codecs

settings_code = '''using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using HalloweenVN.Core;

namespace HalloweenVN.UI
{
    public class SettingsUI : MonoBehaviour
    {
        [SerializeField] private GameObject settingsPanel;
        [SerializeField] private Slider textSpeedSlider;
        [SerializeField] private Text textSpeedLabel;
        [SerializeField] private Slider bgmVolumeSlider;
        [SerializeField] private Text bgmVolumeLabel;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Text sfxVolumeLabel;
        [SerializeField] private Toggle fullscreenToggle;
        [SerializeField] private Button closeButton;
        
        [SerializeField] private Text previewTextLabel;
        [SerializeField] private Text titleTextLabel;
        [SerializeField] private Text closeButtonText;
        private Coroutine typingCoroutine;
        private string previewMessage = "''' + "\\uD14D\\uC2A4\\uD2B8 \\uC18D\\uB3C4\\uAC00 \\uC774 \\uC815\\uB3C4\\uB85C \\uCD9C\\uB825\\uB429\\uB2C8\\uB2E4. \\uB208\\uC73C\\uB85C \\uD655\\uC778\\uD574 \\uBCF4\\uC138\\uC694!" + '''";

        private void OnEnable()
        {
            if (textSpeedSlider != null)
            {
                textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                textSpeedSlider.onValueChanged.AddListener(OnTextSpeedChanged);
            }
            if (bgmVolumeSlider != null)
            {
                bgmVolumeSlider.value = SettingsData.BGMVolume;
                bgmVolumeSlider.onValueChanged.AddListener(OnBGMVolumeChanged);
            }
            if (sfxVolumeSlider != null)
            {
                sfxVolumeSlider.value = SettingsData.SFXVolume;
                sfxVolumeSlider.onValueChanged.AddListener(OnSFXVolumeChanged);
            }
            if (fullscreenToggle != null)
            {
                fullscreenToggle.isOn = SettingsData.IsFullScreen;
                fullscreenToggle.onValueChanged.AddListener(OnFullscreenChanged);
            }
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }

            UpdateLabels();
            UpdateLanguage();
        }

        public void UpdateLanguage()
        {
            GameLanguage lang = SettingsData.Language;

            if (lang == GameLanguage.Korean)
            {
                if (titleTextLabel != null) titleTextLabel.text = "''' + "\\uC124\\uC815" + '''";
                if (textSpeedLabel != null) textSpeedLabel.text = "''' + "\\uD14D\\uC2A4\\uD2B8 \\uC18D\\uB3C4" + '''";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "''' + "\\uB2EB\\uAE30" + '''";
                previewMessage = "''' + "\\uD14D\\uC2A4\\uD2B8 \\uC18D\\uB3C4\\uAC00 \\uC774 \\uC815\\uB3C4\\uB85C \\uCD9C\\uB825\\uB429\\uB2C8\\uB2E4. \\uB208\\uC73C\\uB85C \\uD655\\uC778\\uD574 \\uBCF4\\uC138\\uC694!" + '''";
            }
            else if (lang == GameLanguage.English)
            {
                if (titleTextLabel != null) titleTextLabel.text = "Settings";
                if (textSpeedLabel != null) textSpeedLabel.text = "Text Speed";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "Close";
                previewMessage = "This is a text speed test. Please check it carefully!";
            }
            else if (lang == GameLanguage.Japanese)
            {
                if (titleTextLabel != null) titleTextLabel.text = "''' + "\\u8A2D\\u5B9A" + '''";
                if (textSpeedLabel != null) textSpeedLabel.text = "''' + "\\u30C6\\u30AD\\u30B9\\u30C8\\u901F\\u5EA6" + '''";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "''' + "\\u9589\\u3058\\u308B" + '''";
                previewMessage = "''' + "\\u30C6\\u30AD\\u30B9\\u30C8\\u901F\\u5EA6\\u306E\\u30C6\\u30B9\\u30C8\\u3067\\u3059\\u3002\\u3054\\u78BA\\u8A8D\\u304F\\u3060\\u3055\\u3044\\u3002" + '''";
            }
            else if (lang == GameLanguage.ChineseSimplified)
            {
                if (titleTextLabel != null) titleTextLabel.text = "''' + "\\u8BBE\\u7F6E" + '''";
                if (textSpeedLabel != null) textSpeedLabel.text = "''' + "\\u6587\\u672C\\u901F\\u5EA6" + '''";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "''' + "\\u80CC\\u666F\\u97F3\\u4E50" + '''";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "''' + "\\u97F3\\u6548" + '''";
                if (closeButtonText != null) closeButtonText.text = "''' + "\\u5173\\u95ED" + '''";
                previewMessage = "''' + "\\u8FD9\\u662F\\u6587\\u672C\\u901F\\u5EA6\\u6D4B\\u8BD5\\u3002\\u8BF7\\u4ED4\\u7EC6\\u68C0\\u67E5\\uFF01" + '''";
            }
            else if (lang == GameLanguage.ChineseTraditional)
            {
                if (titleTextLabel != null) titleTextLabel.text = "''' + "\\u8A2D\\u5B9A" + '''";
                if (textSpeedLabel != null) textSpeedLabel.text = "''' + "\\u6587\\u672C\\u901F\\u5EA6" + '''";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "''' + "\\u80CC\\u666F\\u97F3\\u6A02" + '''";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "''' + "\\u97F3\\u6548" + '''";
                if (closeButtonText != null) closeButtonText.text = "''' + "\\u95DC\\u9589" + '''";
                previewMessage = "''' + "\\u9019\\u662F\\u6587\\u672C\\u901F\\u5EA6\\u6E2C\\u8A66\\u3002\\u8ACB\\u4ED4\\u7D30\\u6AA2\\u67E5\\u3002" + '''";
            }
            
            PlayPreviewText();
        }

        private void OnDisable()
        {
            if (textSpeedSlider != null) textSpeedSlider.onValueChanged.RemoveListener(OnTextSpeedChanged);
            if (bgmVolumeSlider != null) bgmVolumeSlider.onValueChanged.RemoveListener(OnBGMVolumeChanged);
            if (sfxVolumeSlider != null) sfxVolumeSlider.onValueChanged.RemoveListener(OnSFXVolumeChanged);
            if (fullscreenToggle != null) fullscreenToggle.onValueChanged.RemoveListener(OnFullscreenChanged);
            if (closeButton != null) closeButton.onClick.RemoveListener(Hide);
        }

        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(true);
                if (textSpeedSlider != null) textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                if (bgmVolumeSlider != null) bgmVolumeSlider.value = SettingsData.BGMVolume;
                if (sfxVolumeSlider != null) sfxVolumeSlider.value = SettingsData.SFXVolume;
                if (fullscreenToggle != null) fullscreenToggle.isOn = SettingsData.IsFullScreen;
                
                UpdateLabels();
                PlayPreviewText();
            }
        }

        public void Hide()
        {
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(false);
            }
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
                typingCoroutine = null;
            }
        }

        private void PlayPreviewText()
        {
            if (previewTextLabel == null) return;
            
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
            }
            
            if (gameObject.activeInHierarchy)
            {
                typingCoroutine = StartCoroutine(TypePreviewCoroutine());
            }
        }
        
        private System.Collections.IEnumerator TypePreviewCoroutine()
        {
            int totalChars = previewMessage.Length;
            
            while (true)
            {
                previewTextLabel.text = "";
                
                for (int i = 0; i <= totalChars; i++)
                {
                    previewTextLabel.text = previewMessage.Substring(0, i);
                    yield return new WaitForSeconds(SettingsData.TextSpeed);
                }
                
                yield return new WaitForSeconds(2f);
            }
        }

        private void OnTextSpeedChanged(float val)
        {
            SettingsData.TextSpeed = SliderToSpeed(val);
            UpdateLabels();
            PlayPreviewText();
        }

        private void OnBGMVolumeChanged(float val)
        {
            SettingsData.BGMVolume = val;
            UpdateLabels();
        }

        private void OnSFXVolumeChanged(float val)
        {
            SettingsData.SFXVolume = val;
            UpdateLabels();
        }

        private void OnFullscreenChanged(bool val)
        {
            SettingsData.IsFullScreen = val;
            Screen.fullScreen = val;
        }

        private void UpdateLabels()
        {
        }

        private float SpeedToSlider(float speed)
        {
            float t = Mathf.InverseLerp(0.1f, 0.01f, speed);
            return Mathf.Lerp(0f, 100f, t);
        }

        private float SliderToSpeed(float sliderVal)
        {
            float t = Mathf.InverseLerp(0f, 100f, sliderVal);
            return Mathf.Lerp(0.1f, 0.01f, t);
        }
    }
}'''

with codecs.open("c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs", "w", encoding="utf-8-sig") as f:
    f.write(settings_code)
print("SettingsUI generated")
