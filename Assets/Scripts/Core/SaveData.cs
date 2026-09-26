using System.Collections.Generic;
using UnityEngine;
using System;

namespace HalloweenVN.Core
{
    [System.Serializable]
    public class SerializableKeyValue
    {
        public string key;
        public bool value;
    }

    [System.Serializable]
    public class SaveData
    {
        public int saveSlot;
        public string currentPhase;
        public string currentDialogueId;
        public int currentNodeIndex;
        public List<string> collectedEvidenceIds;
        public string currentCaseId;
        public int chapterIndex;
        public List<SerializableKeyValue> gameFlagsList;
        public string saveTimestamp;

        /// <summary>
        /// Sets a game flag value.
        /// </summary>
        public void SetFlag(string key, bool value)
        {
            if (gameFlagsList == null)
            {
                gameFlagsList = new List<SerializableKeyValue>();
            }

            foreach (var kvp in gameFlagsList)
            {
                if (kvp.key == key)
                {
                    kvp.value = value;
                    return;
                }
            }
            gameFlagsList.Add(new SerializableKeyValue { key = key, value = value });
        }

        /// <summary>
        /// Gets a game flag value. Returns false if not found.
        /// </summary>
        public bool GetFlag(string key)
        {
            if (gameFlagsList != null)
            {
                foreach (var kvp in gameFlagsList)
                {
                    if (kvp.key == key)
                    {
                        return kvp.value;
                    }
                }
            }
            return false;
        }

        /// <summary>
        /// Checks if a game flag exists.
        /// </summary>
        public bool HasFlag(string key)
        {
            if (gameFlagsList != null)
            {
                foreach (var kvp in gameFlagsList)
                {
                    if (kvp.key == key)
                    {
                        return true;
                    }
                }
            }
            return false;
        }
    }

    /// <summary>
    /// WebGL-compatible save manager using PlayerPrefs.
    /// Works on all platforms including WebGL (browser).
    /// </summary>
    public static class SaveManager
    {
        private static string GetKey(int slot) => $"HalloweenVN_Save_{slot}";

        /// <summary>
        /// Saves the given data to the specified slot via PlayerPrefs.
        /// </summary>
        public static void Save(SaveData data, int slot)
        {
            string json = JsonUtility.ToJson(data, true);
            PlayerPrefs.SetString(GetKey(slot), json);
            PlayerPrefs.Save();
        }

        /// <summary>
        /// Loads save data from the specified slot.
        /// </summary>
        public static SaveData Load(int slot)
        {
            string key = GetKey(slot);
            if (PlayerPrefs.HasKey(key))
            {
                string json = PlayerPrefs.GetString(key);
                return JsonUtility.FromJson<SaveData>(json);
            }
            return null;
        }

        /// <summary>
        /// Checks if a save file exists for the given slot.
        /// </summary>
        public static bool HasSave(int slot)
        {
            return PlayerPrefs.HasKey(GetKey(slot));
        }

        /// <summary>
        /// Deletes the save file for the given slot.
        /// </summary>
        public static void Delete(int slot)
        {
            string key = GetKey(slot);
            if (PlayerPrefs.HasKey(key))
            {
                PlayerPrefs.DeleteKey(key);
                PlayerPrefs.Save();
            }
        }

        /// <summary>
        /// Creates a SaveData object from the current game state.
        /// </summary>
        public static SaveData CreateFromCurrentState(int slot)
        {
            SaveData data = new SaveData();
            data.saveSlot = slot;
            
            if (GameManager.Instance != null)
            {
                data.currentPhase = GameManager.Instance.CurrentPhase.ToString();
            }
            
            data.saveTimestamp = DateTime.UtcNow.ToString("o");
            
            return data;
        }
    }
}
