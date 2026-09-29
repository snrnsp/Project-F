using UnityEngine;
using UnityEditor;
using TMPro;

public class FontScaleChanger {
    [MenuItem("Tools/Change Font Scale")]
    public static void ChangeScale() {
        TMP_FontAsset jpFont = Resources.Load<TMP_FontAsset>("Fonts/ZenKurenaido-Regular SDF");
        if (jpFont != null) {
            Debug.Log($"JP Font found! Scale: {jpFont.faceInfo.scale}");
            var info = jpFont.faceInfo;
            info.scale = 0.75f;
            jpFont.faceInfo = info;
            EditorUtility.SetDirty(jpFont);
        } else {
            Debug.Log("JP Font not found.");
        }
        
        TMP_FontAsset cnFont = Resources.Load<TMP_FontAsset>("Fonts/MaShanZheng-Regular SDF");
        if (cnFont != null) {
            Debug.Log($"CN Font found! Scale: {cnFont.faceInfo.scale}");
            var info = cnFont.faceInfo;
            info.scale = 0.8f;
            cnFont.faceInfo = info;
            EditorUtility.SetDirty(cnFont);
        } else {
            Debug.Log("CN Font not found.");
        }
        
        AssetDatabase.SaveAssets();
    }
}
