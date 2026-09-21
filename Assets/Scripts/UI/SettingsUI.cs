using UnityEngine;
using UnityEngine.UI;
using TMPro;
using HalloweenVN.Core;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Settings panel UI with text speed, volume, and fullscreen controls.
    /// </summary>
    public class SettingsUI : MonoBehaviour
    {
        [SerializeField] private GameObject settingsPanel;
        [SerializeField] private Slider textSpeedSlider;
        [SerializeField] private TextMeshProUGUI textSpeedLabel;
        [SerializeField] private Slider bgmVolumeSlider;
        [SerializeField] private TextMeshProUGUI bgmVolumeLabel;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private TextMeshProUGUI sfxVolumeLabel;
        [SerializeField] private Toggle fullscreenToggle;
        [SerializeField] private Button closeButton;
        
        [SerializeField] private TextMeshProUGUI previewTextLabel;
        private Coroutine typingCoroutine;
        private string previewMessage = "텍스트 속도가 이 정도로 출력됩니다. 눈으로 확인해 보세요!";

        private void OnEnable()
        {
            if (textSpeedSlider != null)
            {
                textSpeedSlider.minValue = 0f;
                textSpeedSlider.maxValue = 100f;
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
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(true);
                // Refresh slider positions from current settings
                if (textSpeedSlider != null) textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                if (bgmVolumeSlider != null) bgmVolumeSlider.value = SettingsData.BGMVolume;
                if (sfxVolumeSlider != null) sfxVolumeSlider.value = SettingsData.SFXVolume;
                if (fullscreenToggle != null) fullscreenToggle.isOn = SettingsData.IsFullScreen;
                PlayPreviewText();
            }
        }

        public void Hide()
        {
            SettingsData.Save();
            if (settingsPanel != null) settingsPanel.SetActive(false);
        }

        private void OnTextSpeedChanged(float value)
        {
            SettingsData.TextSpeed = SliderToSpeed(value);
            UpdateLabels();
            SettingsData.Save();
            PlayPreviewText();
        }
        
        private void PlayPreviewText()
        {
            if (previewTextLabel == null) return;
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            typingCoroutine = StartCoroutine(TypePreviewCoroutine());
        }
        
        private System.Collections.IEnumerator TypePreviewCoroutine()
        {
            previewTextLabel.text = previewMessage;
            
            // Wait one frame so TMPro calculates textInfo.characterCount
            yield return null;
            
            while (true)
            {
                int totalChars = previewTextLabel.textInfo.characterCount;
                previewTextLabel.maxVisibleCharacters = 0;
                
                for (int i = 0; i <= totalChars; i++)
                {
                    previewTextLabel.maxVisibleCharacters = i;
                    yield return new WaitForSeconds(SettingsData.TextSpeed);
                }
                
                yield return new WaitForSeconds(0.5f);
            }
        }

        private void OnBGMVolumeChanged(float value)
        {
            SettingsData.BGMVolume = value;
            UpdateLabels();
            SettingsData.Save();
        }

        private void OnSFXVolumeChanged(float value)
        {
            SettingsData.SFXVolume = value;
            UpdateLabels();
            SettingsData.Save();
        }

        private void OnFullscreenChanged(bool value)
        {
            SettingsData.IsFullScreen = value;
            Screen.fullScreen = value;
            SettingsData.Save();
        }

        private void UpdateLabels()
        {
            if (textSpeedLabel != null) textSpeedLabel.text = $"텍스트 속도: {Mathf.RoundToInt(SpeedToSlider(SettingsData.TextSpeed))}";
            if (bgmVolumeLabel != null) bgmVolumeLabel.text = $"BGM: {Mathf.RoundToInt(SettingsData.BGMVolume * 100)}%" ;
            if (sfxVolumeLabel != null) sfxVolumeLabel.text = $"SFX: {Mathf.RoundToInt(SettingsData.SFXVolume * 100)}%";
        }

        private float SliderToSpeed(float sliderVal)
        {
            return Mathf.Lerp(0.1f, 0.01f, sliderVal / 100f);
        }

        private float SpeedToSlider(float delay)
        {
            float t = Mathf.InverseLerp(0.1f, 0.01f, delay);
            return Mathf.Lerp(0f, 100f, t);
        }
    }
}