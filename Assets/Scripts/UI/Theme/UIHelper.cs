﻿﻿﻿﻿using TMPro;
using UnityEngine;
using UnityEngine.UI;
using System.Reflection;

namespace HalloweenVN.UI.Theme
{
    public static class UIHelper
    {
        /// <summary>
        /// Creates a basic RectTransform GameObject parented to `parent`
        /// </summary>
        public static GameObject CreateUIObject(string name, Transform parent)
        {
            GameObject obj = new GameObject(name);
            obj.transform.SetParent(parent, false);
            obj.AddComponent<RectTransform>();
            return obj;
        }

        /// <summary>
        /// Creates an Image component with given color, optional sprite
        /// </summary>
                public static Sprite CreateCustomRoundedRectSprite(int radius, int borderSize, Color32 bgColor, Color32 borderColor, bool tl, bool tr, bool bl, bool br)
        {
            int size = radius * 2 + borderSize * 2 + 4;
            int centerStart = radius + borderSize;
            int centerEnd = size - centerStart - 1;
            
            Texture2D tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.wrapMode = TextureWrapMode.Clamp;
            Color32 clear = new Color32(0, 0, 0, 0);
            
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    float dx = Mathf.Max(0, Mathf.Max(centerStart - x, x - centerEnd));
                    float dy = Mathf.Max(0, Mathf.Max(centerStart - y, y - centerEnd));
                    
                    bool isCorner = (dx > 0 && dy > 0);
                    bool shouldRound = true;

                    if (isCorner) {
                        if (x < centerStart && y < centerStart) shouldRound = bl;
                        else if (x > centerEnd && y < centerStart) shouldRound = br;
                        else if (x < centerStart && y > centerEnd) shouldRound = tl;
                        else if (x > centerEnd && y > centerEnd) shouldRound = tr;
                    }

                    float dist = 0;
                    if (isCorner && shouldRound) {
                        dist = Mathf.Sqrt(dx * dx + dy * dy);
                    } else {
                        // For straight edges OR square corners, use Chebyshev distance
                        dist = Mathf.Max(dx, dy);
                    }
                    
                    if (dist > radius + borderSize) tex.SetPixel(x, y, clear);
                    else if (dist > radius) tex.SetPixel(x, y, borderColor);
                    else tex.SetPixel(x, y, bgColor);
                }
            }
            tex.Apply();
            return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100, 0, SpriteMeshType.FullRect, new Vector4(centerStart, centerStart, centerStart, centerStart));
        }

        public static Sprite CreateRoundedRectSprite(int radius, int borderSize, Color32 bgColor, Color32 borderColor)
        {
            int size = radius * 2 + borderSize * 2 + 4; // Add a bit of padding for safe slicing
            int centerStart = radius + borderSize;
            int centerEnd = centerStart + 3;
            
            Texture2D tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.wrapMode = TextureWrapMode.Clamp;
            Color32 clear = new Color32(0, 0, 0, 0);
            
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    float dx = Mathf.Max(0, Mathf.Max(centerStart - x, x - centerEnd));
                    float dy = Mathf.Max(0, Mathf.Max(centerStart - y, y - centerEnd));
                    float dist = Mathf.Sqrt(dx * dx + dy * dy);
                    
                    if (dist > radius + borderSize) tex.SetPixel(x, y, clear);
                    else if (dist > radius) tex.SetPixel(x, y, borderColor);
                    else tex.SetPixel(x, y, bgColor);
                }
            }
            tex.Apply();
            return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100, 0, SpriteMeshType.FullRect, new Vector4(centerStart, centerStart, centerStart, centerStart));
        }

        public static Image AddImage(GameObject obj, Color color, Sprite sprite = null)
        {
            Image img = obj.AddComponent<Image>();
            img.color = color;
            if (sprite != null)
            {
                img.sprite = sprite;
            }
            return img;
        }

        private static TMP_FontAsset cachedKoreanFont;
        private static TMP_FontAsset dynamicFallbackFont;

        /// <summary>
        /// Creates a TextMeshProUGUI with given text, color, fontSize, alignment
        /// </summary>
        public static TextMeshProUGUI AddText(GameObject obj, string text, Color color, float fontSize, TextAlignmentOptions alignment = TextAlignmentOptions.Left)
        {
            TextMeshProUGUI tmp = obj.AddComponent<TextMeshProUGUI>();
            tmp.text = text;
            tmp.color = color;
            tmp.fontSize = fontSize;
            tmp.alignment = alignment;

            // Load or create Korean Font at runtime
            if (cachedKoreanFont == null)
            {
                // Try to load pre-made asset first
                cachedKoreanFont = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
                
                // If not found, create dynamic font asset from TTF at runtime
                if (cachedKoreanFont == null)
                {
                    Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
                    if (rawFont != null)
                    {
                        cachedKoreanFont = TMP_FontAsset.CreateFontAsset(rawFont);
                        cachedKoreanFont.name = "MalgunGothic Runtime SDF";
                    }
                }
            }

            if (cachedKoreanFont != null)
            {
                tmp.font = cachedKoreanFont;
            }

            return tmp;
        }

        /// <summary>
        /// Creates a fully styled Button with TMP text child
        /// </summary>
        public static (Button btn, TextMeshProUGUI btnText) CreateButton(Transform parent, string label, float width, float height)
        {
            GameObject btnObj = CreateUIObject("Button_" + label, parent);
            RectTransform rt = btnObj.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(width, height);

            Image img = AddImage(btnObj, HalloweenTheme.ButtonNormal);
            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            btn.colors = HalloweenTheme.GetButtonColors();
            btn.targetGraphic = img;

            GameObject textObj = CreateUIObject("Text", btnObj.transform);
            StretchFull(textObj.GetComponent<RectTransform>());
            TextMeshProUGUI tmp = AddText(textObj, label, HalloweenTheme.ButtonText, HalloweenTheme.ButtonFontSize, TextAlignmentOptions.Center);
            
            return (btn, tmp);
        }

        /// <summary>
        /// Creates a panel with background image and optional border outline
        /// </summary>
        public static GameObject CreatePanel(string name, Transform parent, Color bgColor)
        {
            GameObject panel = CreateUIObject(name, parent);
            AddImage(panel, bgColor);
            Outline outline = panel.AddComponent<Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);
            return panel;
        }

        /// <summary>
        /// Creates a scroll view with vertical layout
        /// </summary>
        public static (ScrollRect scrollRect, Transform content) CreateScrollView(string name, Transform parent, float width, float height)
        {
            GameObject scrollObj = CreateUIObject(name, parent);
            RectTransform scrollRt = scrollObj.GetComponent<RectTransform>();
            scrollRt.sizeDelta = new Vector2(width, height);
            ScrollRect scrollRect = scrollObj.AddComponent<ScrollRect>();
            scrollRect.horizontal = false;
            scrollRect.vertical = true;
            scrollRect.scrollSensitivity = 20f;
            AddImage(scrollObj, new Color(0,0,0,0)); // Invisible background to catch scroll events

            GameObject viewport = CreateUIObject("Viewport", scrollObj.transform);
            StretchFull(viewport.GetComponent<RectTransform>());
            viewport.AddComponent<Image>().color = new Color(0,0,0,0);
            viewport.AddComponent<Mask>().showMaskGraphic = false;

            GameObject content = CreateUIObject("Content", viewport.transform);
            RectTransform contentRt = content.GetComponent<RectTransform>();
            SetAnchors(contentRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            contentRt.sizeDelta = new Vector2(0, 0);

            VerticalLayoutGroup vlg = content.AddComponent<VerticalLayoutGroup>();
            vlg.childControlHeight = false;
            vlg.childControlWidth = true;
            vlg.childForceExpandHeight = false;
            vlg.childForceExpandWidth = true;
            vlg.spacing = HalloweenTheme.Spacing;

            ContentSizeFitter csf = content.AddComponent<ContentSizeFitter>();
            csf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            scrollRect.viewport = viewport.GetComponent<RectTransform>();
            scrollRect.content = contentRt;

            return (scrollRect, content.transform);
        }

        /// <summary>
        /// Configures RectTransform anchoring shortcuts
        /// </summary>
        public static void SetAnchors(RectTransform rt, Vector2 anchorMin, Vector2 anchorMax, Vector2 pivot)
        {
            rt.anchorMin = anchorMin;
            rt.anchorMax = anchorMax;
            rt.pivot = pivot;
        }

        /// <summary>
        /// Stretch to fill parent
        /// </summary>
        public static void StretchFull(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
        }

        /// <summary>
        /// Anchor to bottom, given height
        /// </summary>
        public static void SetBottom(RectTransform rt, float height)
        {
            rt.anchorMin = new Vector2(0, 0);
            rt.anchorMax = new Vector2(1, 0);
            rt.pivot = new Vector2(0.5f, 0);
            rt.offsetMin = new Vector2(0, 0);
            rt.offsetMax = new Vector2(0, height);
        }

        /// <summary>
        /// Reflection-based field setting for private SerializeFields
        /// </summary>
        public static void SetField(Component comp, string fieldName, object value)
        {
            if (comp == null) return;
            var field = comp.GetType().GetField(fieldName, BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Public);
            if (field != null) 
            {
                field.SetValue(comp, value);
            }
            else 
            {
                Debug.LogWarning($"Field '{fieldName}' not found on {comp.GetType().Name}");
            }
        }
    }
}
