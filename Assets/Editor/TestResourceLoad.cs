#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

namespace HalloweenVN.Editor
{
    public class TestResourceLoad
    {
        [MenuItem("Tools/Test Resource Load")]
        public static void TestLoad()
        {
            Sprite sprite = Resources.Load<Sprite>("Characters/카스미/기본");
            if (sprite != null)
            {
                Debug.Log($"SUCCESS: Loaded {sprite.name}");
            }
            else
            {
                Debug.LogError("FAILED: Sprite is null!");
                
                // Let's see what is there
                Object[] all = Resources.LoadAll("Characters/카스미/기본");
                Debug.Log($"Found {all.Length} objects with that path.");
                foreach (var obj in all)
                {
                    Debug.Log($" - Type: {obj.GetType().Name}, Name: {obj.name}");
                }
            }
        }
    }
}
#endif
