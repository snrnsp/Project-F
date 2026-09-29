using UnityEngine;
using TMPro;

public class TestFaceInfo : MonoBehaviour {
    void Start() {
        TMP_FontAsset font = TMP_FontAsset.CreateFontAsset(Resources.Load<Font>("Fonts/ZenKurenaido-Regular"));
        var info = font.faceInfo;
        Debug.Log(info.scale);
    }
}
