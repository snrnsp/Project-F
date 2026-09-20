using UnityEngine;
using HalloweenVN.UI.Theme;

namespace HalloweenVN.Core
{
    /// <summary>
    /// Automatically bootstraps the entire Halloween VN system on game start.
    /// No manual GameObject setup required — just press Play.
    /// </summary>
    public static class GameBootstrap
    {
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
        static void AutoSetup()
        {
            // Prevent duplicate setup
            if (Object.FindFirstObjectByType<HalloweenUIBuilder>() != null)
                return;

            GameObject bootstrapObj = new GameObject("[HalloweenVN]");
            bootstrapObj.AddComponent<HalloweenUIBuilder>();
            Object.DontDestroyOnLoad(bootstrapObj);

            Debug.Log("🎃 Halloween VN — Auto-initialized!");
        }
    }
}
