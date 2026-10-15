using UnityEngine;
using UnityEngine.UI;

namespace HalloweenVN.UI
{
    /// <summary>Keeps untranslated labels readable with bundled fonts on WebGL.</summary>
    [RequireComponent(typeof(Text))]
    public sealed class LegacyTextFontFallback : MonoBehaviour
    {
        private Text label;
        private Font preferredFont;
        private Font appliedFont;
        private string previousText;
        private bool isRefreshing;

        private void OnEnable()
        {
            label = GetComponent<Text>();
            previousText = null;
            if (label != null)
            {
                label.RegisterDirtyLayoutCallback(Refresh);
            }
            Refresh();
        }

        private void OnDisable()
        {
            if (label != null)
            {
                label.UnregisterDirtyLayoutCallback(Refresh);
            }
        }

        public void Refresh()
        {
            if (isRefreshing) return;
            if (label == null) label = GetComponent<Text>();
            if (label == null) return;

            if (label.font != appliedFont) preferredFont = label.font;
            else if (previousText == label.text) return;

            isRefreshing = true;
            try
            {
                previousText = label.text;
                appliedFont = preferredFont;
                if (preferredFont != null && !Supports(preferredFont, label.text))
                {
                    Font fallback = FontHelper.GetFont("MalgunGothic");
                    if (fallback != null && Supports(fallback, label.text)) appliedFont = fallback;
                }
                if (appliedFont != null && label.font != appliedFont) label.font = appliedFont;
            }
            finally
            {
                isRefreshing = false;
            }
        }

        private static bool Supports(Font font, string text)
        {
            if (string.IsNullOrEmpty(text)) return true;
            foreach (char character in text)
                if (!char.IsWhiteSpace(character) && !char.IsControl(character) && !font.HasCharacter(character))
                    return false;
            return true;
        }
    }
}
