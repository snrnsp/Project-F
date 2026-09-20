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

        private void OnEnable()
        {
            if (textSpeedSlider != null)
            {
                textSpeedSlider.minValue = 0.01f;
                textSpeedSlider.maxValue = 0.1f;
                textSpeedSlider.value = SettingsData.TextSpeed;
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
                if (textSpeedSlider != null) textSpeedSlider.value = SettingsData.TextSpeed;
                if (bgmVolumeSlider != null) bgmVolumeSlider.value = SettingsData.BGMVolume;
                if (sfxVolumeSlider != null) sfxVolumeSlider.value = SettingsData.SFXVolume;
                if (fullscreenToggle != null) fullscreenToggle.isOn = SettingsData.IsFullScreen;
            }
        }

        public void Hide()
        {
            SettingsData.Save();
            if (settingsPanel != null) settingsPanel.SetActive(false);
        }

        private void OnTextSpeedChanged(float value)
        {
            SettingsData.TextSpeed = value;
            UpdateLabels();
        }

        private void OnBGMVolumeChanged(float value)
        {
            SettingsData.BGMVolume = value;
            UpdateLabels();
        }

        private void OnSFXVolumeChanged(float value)
        {
            SettingsData.SFXVolume = value;
            UpdateLabels();
        }

        private void OnFullscreenChanged(bool value)
        {
            SettingsData.IsFullScreen = value;
            Screen.fullScreen = value;
        }

        private void UpdateLabels()
        {
            // Lower value = faster typing, so invert for display
            if (textSpeedLabel != null) textSpeedLabel.text = $"텍스트 속도: {Mathf.RoundToInt((0.11f - SettingsData.TextSpeed) * 1000)}";
            if (bgmVolumeLabel != null) bgmVolumeLabel.text = $"BGM: {Mathf.RoundToInt(SettingsData.BGMVolume * 100)}%";
            if (sfxVolumeLabel != null) sfxVolumeLabel.text = $"SFX: {Mathf.RoundToInt(SettingsData.SFXVolume * 100)}%";
        }
    }
}
