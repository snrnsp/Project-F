using UnityEditor;
using UnityEngine;
using HalloweenVN.UI.Theme;

public class HalloweenVNSetup : MonoBehaviour
{
    [MenuItem("Halloween VN/Setup Scene (원클릭 설정)")]
    static void SetupScene()
    {
        // Check if already exists
        if (Object.FindFirstObjectByType<HalloweenUIBuilder>() != null)
        {
            Debug.Log("HalloweenUIBuilder already exists in scene!");
            EditorUtility.DisplayDialog("Setup", "HalloweenUIBuilder가 이미 씬에 존재합니다!", "OK");
            return;
        }

        GameObject builderObj = new GameObject("HalloweenVN_Builder");
        builderObj.AddComponent<HalloweenUIBuilder>();
        Selection.activeGameObject = builderObj;

        Debug.Log("✅ HalloweenUIBuilder added to scene! Press Play to start.");
        EditorUtility.DisplayDialog("Setup Complete", 
            "HalloweenUIBuilder가 씬에 추가되었습니다!\n\nPlay 버튼을 눌러 시작하세요.", "OK");
    }
}
