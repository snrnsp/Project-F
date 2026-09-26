using UnityEngine;
using System.IO;

namespace HalloweenVN.Data
{
    /// <summary>
    /// Utility class for loading game data from various sources.
    /// </summary>
    public static class DataLoader
    {
        /// <summary>
        /// Loads and deserializes a JSON file from Resources.
        /// </summary>
        public static T LoadFromResources<T>(string path)
        {
            TextAsset textAsset = Resources.Load<TextAsset>(path);
            if (textAsset != null)
            {
                string json = textAsset.text;
                if (json.Length > 0 && json[0] == '\uFEFF') json = json.Substring(1);
                return JsonUtility.FromJson<T>(json);
            }
            Debug.LogError($"DataLoader: Failed to load file from Resources at path: {path}");
            return default;
        }

#if !UNITY_WEBGL
        /// <summary>
        /// Loads and deserializes a JSON file from StreamingAssets.
        /// </summary>
        public static T LoadFromStreamingAssets<T>(string fileName)
        {
            string path = Path.Combine(Application.streamingAssetsPath, fileName);
            if (File.Exists(path))
            {
                string json = File.ReadAllText(path);
                return JsonUtility.FromJson<T>(json);
            }
            Debug.LogError($"DataLoader: Failed to load file from StreamingAssets at path: {path}");
            return default;
        }
#endif

        /// <summary>
        /// Convenience method to load a DialogueContainer.
        /// </summary>
        public static DialogueContainer LoadDialogue(string dialogueId)
        {
            return LoadFromResources<DialogueContainer>($"Data/Dialogues/{dialogueId}");
        }

        /// <summary>
        /// Convenience method to load an EvidenceDatabase.
        /// </summary>
        public static EvidenceDatabase LoadEvidenceDatabase(string dbName)
        {
            return LoadFromResources<EvidenceDatabase>($"Data/Evidence/{dbName}");
        }

        /// <summary>
        /// Convenience method to load a CaseContainer.
        /// </summary>
        public static CaseContainer LoadCase(string caseId)
        {
            return LoadFromResources<CaseContainer>($"Data/Cases/{caseId}");
        }
    }
}
