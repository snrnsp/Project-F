﻿using UnityEngine;
using UnityEngine.UI;

namespace HalloweenVN.UI.Theme
{
    public static class HalloweenTheme
    {
        // Main palette
        public static readonly Color BackgroundDark = new Color32(13, 10, 20, 255);        // near-black purple
        public static readonly Color PanelBackground = new Color32(30, 15, 45, 255);       // dark purple, semi-transparent
        public static readonly Color PanelBorder = new Color32(180, 100, 20, 255);         // warm amber/orange
        public static readonly Color AccentOrange = new Color32(255, 140, 0, 255);         // bright orange
        public static readonly Color AccentRed = new Color32(180, 30, 30, 255);            // blood red
        public static readonly Color TextPrimary = new Color32(240, 230, 211, 255);        // warm cream
        public static readonly Color TextSpeaker = new Color32(255, 160, 50, 255);         // orange-gold
        public static readonly Color TextAccent = new Color32(255, 100, 50, 255);          // orange-red
        
        // Buttons
        public static readonly Color ButtonNormal = new Color32(50, 25, 70, 255);          // dark purple
        public static readonly Color ButtonHighlight = new Color32(80, 40, 110, 255);      // brighter purple
        public static readonly Color ButtonPressed = new Color32(120, 60, 20, 255);        // dark orange
        public static readonly Color ButtonDisabled = new Color32(40, 40, 40, 255);        // gray
        public static readonly Color ButtonText = new Color32(255, 180, 80, 255);          // warm gold
        
        // Evidence / Deduction
        public static readonly Color SlotEmpty = new Color32(35, 30, 50, 255);             // dark purple-gray
        public static readonly Color SlotFilled = new Color32(50, 80, 50, 255);            // muted green
        public static readonly Color SlotHighlight = new Color32(180, 100, 20, 255);       // amber highlight
        public static readonly Color InventoryBg = new Color32(20, 12, 30, 255);           // very dark
        
        // Transition
        public static readonly Color TransitionColor = new Color32(0, 0, 0, 255);          // pure black
        
        // Sizes
        public const float DialoguePanelHeight = 250f;
        public const float SpeakerFontSize = 32f;
        public const float DialogueFontSize = 26f;
        public const float ChoiceFontSize = 24f;
        public const float ButtonFontSize = 22f;
        public const float HeaderFontSize = 36f;
        public const float BodyFontSize = 20f;
        public const float PanelBorderWidth = 6f;
        public const float PanelCornerRadius = 8f;
        public const float ButtonHeight = 50f;
        public const float ChoiceButtonHeight = 55f;
        public const float EvidenceSlotWidth = 280f;
        public const float EvidenceSlotHeight = 80f;
        public const float EvidenceItemSize = 90f;
        public const float Padding = 15f;
        public const float Spacing = 10f;
        
        /// <summary>
        /// Creates a ColorBlock for Halloween-themed buttons.
        /// </summary>
        public static ColorBlock GetButtonColors()
        {
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = ButtonNormal;
            cb.highlightedColor = ButtonHighlight;
            cb.pressedColor = ButtonPressed;
            cb.disabledColor = ButtonDisabled;
            cb.colorMultiplier = 1f;
            cb.fadeDuration = 0.15f;
            return cb;
        }
    }
}
