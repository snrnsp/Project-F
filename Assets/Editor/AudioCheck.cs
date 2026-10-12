using UnityEngine;
using UnityEditor;
public class AudioCheck {
    public static void Check() {
        AudioClip clip = AssetDatabase.LoadAssetAtPath<AudioClip>("Assets/Resources/Audio/SFX/sfx_ui_click.mp3");
        if (clip != null) {
            Debug.Log($"Clip length: {clip.length}, samples: {clip.samples}");
        }
    }
}
