using UnityEditor;
using UnityEngine;
public class WebGLFix : MonoBehaviour {
    [MenuItem("Tools/Fix WebGL")]
    public static void Fix() {
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Disabled;
        PlayerSettings.WebGL.decompressionFallback = true;
        Debug.Log("WebGL Settings Fixed");
    }
}
