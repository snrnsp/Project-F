using UnityEngine;
using UnityEditor;
public class SpriteCheck2 {
    [InitializeOnLoadMethod]
    static void Check() {
        Sprite[] sprites = Resources.LoadAll<Sprite>("Characters/리리스/기본");
        Debug.Log("###LILITH_SPRITES### " + (sprites != null ? sprites.Length.ToString() : "0"));
        Texture2D tex = Resources.Load<Texture2D>("Characters/리리스/기본");
        Debug.Log("###LILITH_TEX### " + (tex != null ? "found" : "null"));
    }
}
