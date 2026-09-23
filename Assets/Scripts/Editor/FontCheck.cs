using UnityEngine;
public class FontCheck : MonoBehaviour {
    void Start() {
        Font arial = Resources.GetBuiltinResource<Font>("Arial.ttf");
        Debug.Log("Arial exists: " + (arial != null));
    }
}
