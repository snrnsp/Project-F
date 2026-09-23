using UnityEngine;

namespace HalloweenVN.Core
{
    public enum GameLanguage
    {
        Korean,
        English,
        Japanese,
        ChineseSimplified,
        ChineseTraditional
    }

    public static class SettingsData
    {
        public static float TextSpeed { get; set; } = 0.03f;
        public static float BGMVolume { get; set; } = 0.8f;
        public static float SFXVolume { get; set; } = 1.0f;
        public static bool IsFullScreen { get; set; } = true;
        public static float AutoPlayDelay { get; set; } = 2.0f;
        public static int PerformanceMode { get; set; } = 1; // 0: Power Saving, 1: High Quality
        public static GameLanguage Language { get; set; } = GameLanguage.Korean;

        private const string Prefix = "HalloweenVN_";

        static SettingsData()
        {
            Load();
            ApplyPerformanceMode();
        }

        public static void Load()
        {
            TextSpeed = PlayerPrefs.GetFloat(Prefix + "TextSpeed", 0.03f);
            BGMVolume = PlayerPrefs.GetFloat(Prefix + "BGMVolume", 0.8f);
            SFXVolume = PlayerPrefs.GetFloat(Prefix + "SFXVolume", 1.0f);
            IsFullScreen = PlayerPrefs.GetInt(Prefix + "IsFullScreen", 1) == 1;
            AutoPlayDelay = PlayerPrefs.GetFloat(Prefix + "AutoPlayDelay", 2.0f);
            PerformanceMode = PlayerPrefs.GetInt(Prefix + "PerformanceMode", 1);
            Language = (GameLanguage)PlayerPrefs.GetInt(Prefix + "Language", 0);
        }

        public static void Save()
        {
            PlayerPrefs.SetFloat(Prefix + "TextSpeed", Mathf.Clamp(TextSpeed, 0.01f, 0.1f));
            PlayerPrefs.SetFloat(Prefix + "BGMVolume", Mathf.Clamp01(BGMVolume));
            PlayerPrefs.SetFloat(Prefix + "SFXVolume", Mathf.Clamp01(SFXVolume));
            PlayerPrefs.SetInt(Prefix + "IsFullScreen", IsFullScreen ? 1 : 0);
            PlayerPrefs.SetFloat(Prefix + "AutoPlayDelay", Mathf.Clamp(AutoPlayDelay, 1.0f, 5.0f));
            PlayerPrefs.SetInt(Prefix + "PerformanceMode", PerformanceMode);
            PlayerPrefs.SetInt(Prefix + "Language", (int)Language);
            PlayerPrefs.Save();
            ApplyPerformanceMode();
        }

        public static void ApplyPerformanceMode()
        {
            if (PerformanceMode == 0) // Power Saving
            {
                Application.targetFrameRate = 30;
                QualitySettings.vSyncCount = 0;
            }
            else // High Quality
            {
                Application.targetFrameRate = 60;
                QualitySettings.vSyncCount = 1;
            }
        }

        public static void ResetToDefaults()
        {
            TextSpeed = 0.03f;
            BGMVolume = 0.8f;
            SFXVolume = 1.0f;
            IsFullScreen = true;
            AutoPlayDelay = 2.0f;
            PerformanceMode = 1;
            Save();
        }
    }
}
