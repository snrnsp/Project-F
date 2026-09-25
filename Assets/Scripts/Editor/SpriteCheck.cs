using UnityEngine;
public class SpriteCheck : MonoBehaviour {
    void Start() {
        Sprite[] sprites = Resources.LoadAll<Sprite>("Characters/리리스/기본");
        Debug.Log("Lilith sprites count: " + (sprites != null ? sprites.Length : 0));
        Texture2D tex = Resources.Load<Texture2D>("Characters/리리스/기본");
        Debug.Log("Lilith texture: " + (tex != null ? "found" : "null"));
    }
}
