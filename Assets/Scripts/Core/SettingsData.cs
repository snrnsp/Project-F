using UnityEngine;
using UnityEngine.InputSystem;

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
        public enum SkipKeyOption { Ctrl, Shift, Space, Off, Custom }
        public static SkipKeyOption SkipKey = SkipKeyOption.Ctrl;
        public static bool UseHandwritingFont { get; set; } = true;
        public static int PerformanceMode { get; set; } = 1; // 0: Power Saving, 1: High Quality
        public static GameLanguage Language { get; set; } = GameLanguage.Korean;
        public static bool EnableFlashingEffects { get; set; } = true;

        // Customizable Key Bindings
        public static Key AdvanceKey { get; set; } = Key.Space;
        public static Key SkipKeyBinding { get; set; } = Key.LeftCtrl;
        public static Key AutoPlayKey { get; set; } = Key.A;
        public static Key BacklogKey { get; set; } = Key.L;
        public static Key HideUiKey { get; set; } = Key.H;

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
            SkipKey = (SkipKeyOption)PlayerPrefs.GetInt(Prefix + "SkipKey", 0);
            UseHandwritingFont = PlayerPrefs.GetInt(Prefix + "UseHandwritingFont", 1) == 1;
            PerformanceMode = PlayerPrefs.GetInt(Prefix + "PerformanceMode", 1);
            Language = (GameLanguage)PlayerPrefs.GetInt(Prefix + "Language", 0);
            EnableFlashingEffects = PlayerPrefs.GetInt(Prefix + "EnableFlashingEffects", 1) == 1;

            AdvanceKey = (Key)PlayerPrefs.GetInt(Prefix + "Key_Advance", (int)Key.Space);
            int defaultSkipKey = SkipKey == SkipKeyOption.Shift ? (int)Key.LeftShift
                               : SkipKey == SkipKeyOption.Space ? (int)Key.Space
                               : (int)Key.LeftCtrl;
            SkipKeyBinding = (Key)PlayerPrefs.GetInt(Prefix + "Key_Skip", defaultSkipKey);
            SyncSkipKeyOptionFromBinding();
            AutoPlayKey = (Key)PlayerPrefs.GetInt(Prefix + "Key_Auto", (int)Key.A);
            BacklogKey = (Key)PlayerPrefs.GetInt(Prefix + "Key_Backlog", (int)Key.L);
            HideUiKey = (Key)PlayerPrefs.GetInt(Prefix + "Key_HideUi", (int)Key.H);
        }

        public static void SyncSkipKeyOptionFromBinding()
        {
            if (SkipKeyBinding == Key.LeftCtrl || SkipKeyBinding == Key.RightCtrl)
                SkipKey = SkipKeyOption.Ctrl;
            else if (SkipKeyBinding == Key.LeftShift || SkipKeyBinding == Key.RightShift)
                SkipKey = SkipKeyOption.Shift;
            else if (SkipKeyBinding == Key.Space)
                SkipKey = SkipKeyOption.Space;
            else if (SkipKeyBinding == Key.None)
                SkipKey = SkipKeyOption.Off;
            else
                SkipKey = SkipKeyOption.Custom;
        }

        public static void SetSkipKeyFromOption(SkipKeyOption option)
        {
            SkipKey = option;
            if (option == SkipKeyOption.Ctrl) SkipKeyBinding = Key.LeftCtrl;
            else if (option == SkipKeyOption.Shift) SkipKeyBinding = Key.LeftShift;
            else if (option == SkipKeyOption.Space) SkipKeyBinding = Key.Space;
        }

        public static void Save()
        {
            SyncSkipKeyOptionFromBinding();
            PlayerPrefs.SetFloat(Prefix + "TextSpeed", Mathf.Clamp(TextSpeed, 0.001f, 0.1f));
            PlayerPrefs.SetFloat(Prefix + "BGMVolume", Mathf.Clamp01(BGMVolume));
            PlayerPrefs.SetFloat(Prefix + "SFXVolume", Mathf.Clamp01(SFXVolume));
            PlayerPrefs.SetInt(Prefix + "IsFullScreen", IsFullScreen ? 1 : 0);
            PlayerPrefs.SetFloat(Prefix + "AutoPlayDelay", Mathf.Clamp(AutoPlayDelay, 0.1f, 5.0f));
            PlayerPrefs.SetInt(Prefix + "SkipKey", (int)SkipKey);
            PlayerPrefs.SetInt(Prefix + "UseHandwritingFont", UseHandwritingFont ? 1 : 0);
            PlayerPrefs.SetInt(Prefix + "PerformanceMode", PerformanceMode);
            PlayerPrefs.SetInt(Prefix + "Language", (int)Language);
            PlayerPrefs.SetInt(Prefix + "EnableFlashingEffects", EnableFlashingEffects ? 1 : 0);

            PlayerPrefs.SetInt(Prefix + "Key_Advance", (int)AdvanceKey);
            PlayerPrefs.SetInt(Prefix + "Key_Skip", (int)SkipKeyBinding);
            PlayerPrefs.SetInt(Prefix + "Key_Auto", (int)AutoPlayKey);
            PlayerPrefs.SetInt(Prefix + "Key_Backlog", (int)BacklogKey);
            PlayerPrefs.SetInt(Prefix + "Key_HideUi", (int)HideUiKey);
            PlayerPrefs.Save();
            ApplyPerformanceMode();
        }

        public static bool IsKeyPressed(Key boundKey)
        {
            var kb = Keyboard.current;
            if (kb == null || boundKey == Key.None) return false;
            if (boundKey == Key.LeftCtrl || boundKey == Key.RightCtrl)
                return kb.leftCtrlKey.isPressed || kb.rightCtrlKey.isPressed;
            if (boundKey == Key.LeftShift || boundKey == Key.RightShift)
                return kb.leftShiftKey.isPressed || kb.rightShiftKey.isPressed;
            if (boundKey == Key.LeftAlt || boundKey == Key.RightAlt)
                return kb.leftAltKey.isPressed || kb.rightAltKey.isPressed;
            if (boundKey == Key.Enter || boundKey == Key.NumpadEnter)
                return kb.enterKey.isPressed || kb.numpadEnterKey.isPressed;
            var ctrl = kb[boundKey];
            return ctrl != null && ctrl.isPressed;
        }

        public static bool WasKeyPressedThisFrame(Key boundKey)
        {
            var kb = Keyboard.current;
            if (kb == null || boundKey == Key.None) return false;
            if (boundKey == Key.LeftCtrl || boundKey == Key.RightCtrl)
                return kb.leftCtrlKey.wasPressedThisFrame || kb.rightCtrlKey.wasPressedThisFrame;
            if (boundKey == Key.LeftShift || boundKey == Key.RightShift)
                return kb.leftShiftKey.wasPressedThisFrame || kb.rightShiftKey.wasPressedThisFrame;
            if (boundKey == Key.LeftAlt || boundKey == Key.RightAlt)
                return kb.leftAltKey.wasPressedThisFrame || kb.rightAltKey.wasPressedThisFrame;
            if (boundKey == Key.Enter || boundKey == Key.NumpadEnter)
                return kb.enterKey.wasPressedThisFrame || kb.numpadEnterKey.wasPressedThisFrame;
            var ctrl = kb[boundKey];
            return ctrl != null && ctrl.wasPressedThisFrame;
        }

        public static bool IsSkipKeyPressed() => IsKeyPressed(SkipKeyBinding);

        public static bool WasAdvanceKeyPressedThisFrame()
        {
            if (WasKeyPressedThisFrame(AdvanceKey)) return true;
            // Also keep Enter working for advancing dialogue unless Enter is bound to another action
            if (AdvanceKey != Key.Enter && SkipKeyBinding != Key.Enter && AutoPlayKey != Key.Enter && BacklogKey != Key.Enter && HideUiKey != Key.Enter)
            {
                if (WasKeyPressedThisFrame(Key.Enter)) return true;
            }
            return false;
        }

        public static bool WasAutoKeyPressedThisFrame() => WasKeyPressedThisFrame(AutoPlayKey);

        public static bool WasBacklogKeyPressedThisFrame()
        {
            if (WasKeyPressedThisFrame(BacklogKey)) return true;
            if (BacklogKey != Key.PageUp && AdvanceKey != Key.PageUp && SkipKeyBinding != Key.PageUp && AutoPlayKey != Key.PageUp && HideUiKey != Key.PageUp)
            {
                if (WasKeyPressedThisFrame(Key.PageUp)) return true;
            }
            return false;
        }

        public static bool WasHideUiKeyPressedThisFrame() => WasKeyPressedThisFrame(HideUiKey);

        public static Key NormalizeKey(Key rawKey)
        {
            if (rawKey == Key.RightCtrl) return Key.LeftCtrl;
            if (rawKey == Key.RightShift) return Key.LeftShift;
            if (rawKey == Key.RightAlt) return Key.LeftAlt;
            if (rawKey == Key.NumpadEnter) return Key.Enter;
            return rawKey;
        }

        public static string GetKeyDisplayName(Key key)
        {
            switch (key)
            {
                case Key.None: return "-";
                case Key.LeftCtrl:
                case Key.RightCtrl: return "Ctrl";
                case Key.LeftShift:
                case Key.RightShift: return "Shift";
                case Key.LeftAlt:
                case Key.RightAlt: return "Alt";
                case Key.Space: return "Space";
                case Key.Enter:
                case Key.NumpadEnter: return "Enter";
                case Key.Tab: return "Tab";
                case Key.Backquote: return "`";
                case Key.Minus: return "-";
                case Key.Equals: return "=";
                case Key.LeftBracket: return "[";
                case Key.RightBracket: return "]";
                case Key.Backslash: return "\\";
                case Key.Semicolon: return ";";
                case Key.Quote: return "'";
                case Key.Comma: return ",";
                case Key.Period: return ".";
                case Key.Slash: return "/";
                case Key.UpArrow: return "↑";
                case Key.DownArrow: return "↓";
                case Key.LeftArrow: return "←";
                case Key.RightArrow: return "→";
                case Key.Digit0: return "0";
                case Key.Digit1: return "1";
                case Key.Digit2: return "2";
                case Key.Digit3: return "3";
                case Key.Digit4: return "4";
                case Key.Digit5: return "5";
                case Key.Digit6: return "6";
                case Key.Digit7: return "7";
                case Key.Digit8: return "8";
                case Key.Digit9: return "9";
                default: return key.ToString();
            }
        }

        public static void ApplyPerformanceMode()
        {
#if UNITY_WEBGL && !UNITY_EDITOR
            // WebGL: let the browser's requestAnimationFrame handle frame pacing
            QualitySettings.vSyncCount = 0;
            Application.targetFrameRate = (PerformanceMode == 0) ? 30 : -1;
#else
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
#endif
        }

        public static void ResetKeyBindings()
        {
            AdvanceKey = Key.Space;
            SkipKeyBinding = Key.LeftCtrl;
            SkipKey = SkipKeyOption.Ctrl;
            AutoPlayKey = Key.A;
            BacklogKey = Key.L;
            HideUiKey = Key.H;
            Save();
        }

        public static void ResetToDefaults()
        {
            TextSpeed = 0.03f;
            BGMVolume = 0.8f;
            SFXVolume = 1.0f;
            IsFullScreen = true;
            AutoPlayDelay = 2.0f;
            SkipKey = SkipKeyOption.Ctrl;
            UseHandwritingFont = true;
            PerformanceMode = 1;
            EnableFlashingEffects = true;
            ResetKeyBindings();
        }
    }
}

