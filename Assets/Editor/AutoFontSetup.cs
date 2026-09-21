#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;
using TMPro;

namespace HalloweenVN.Editor
{
    [InitializeOnLoad]
    public class AutoFontSetup
    {
        static AutoFontSetup()
        {
            EditorApplication.delayCall += SetupFont;
        }

        [MenuItem("Tools/Setup Korean Font (한글 폰트 설정)")]
        public static void SetupFont()
        {
            string fontPath = "Assets/Resources/Fonts/MalgunGothic.ttf";
            string assetPath = "Assets/Resources/Fonts/MalgunGothic SDF.asset";

            Font font = AssetDatabase.LoadAssetAtPath<Font>(fontPath);
            if (font == null)
            {
                Debug.LogError("❌ [AutoFontSetup] MalgunGothic.ttf 폰트를 찾을 수 없습니다. 경로: " + fontPath);
                return;
            }

            TMP_FontAsset existingAsset = AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(assetPath);
            if (existingAsset == null)
            {
                TMP_FontAsset fontAsset = TMP_FontAsset.CreateFontAsset(font);
                fontAsset.atlasPopulationMode = AtlasPopulationMode.Dynamic;
                
                AssetDatabase.CreateAsset(fontAsset, assetPath);
                AssetDatabase.SaveAssets();
                Debug.Log("✅ [AutoFontSetup] 맑은 고딕(MalgunGothic) TMP 폰트 에셋이 성공적으로 생성되었습니다!");
            }
            else
            {
                Debug.Log("✅ [AutoFontSetup] 한글 폰트 에셋이 이미 존재합니다.");
            }
        }
    }
}
#endif
