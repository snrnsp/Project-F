using UnityEngine;
public class FontCheck : MonoBehaviour {
    void Start() {
        Font f = Resources.Load<Font>("Fonts/MalgunGothic");
        f.RequestCharactersInTexture("語言設定");
        bool b1 = f.HasCharacter('語');
        bool b2 = f.HasCharacter('設');
        bool b3 = f.HasCharacter('言');
        bool b4 = f.HasCharacter('定');
        Debug.Log($"MalgunGothic has: 語={b1} 設={b2} 言={b3} 定={b4}");
    }
}