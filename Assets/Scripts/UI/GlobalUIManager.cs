﻿using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;

namespace HalloweenVN.UI
{
    public class GlobalUIManager : MonoBehaviour
    {
        [SerializeField] private GameObject settingsUI;

        public void Initialize(GameObject settingsUiObj)
        {
            this.settingsUI = settingsUiObj;
        }

        void Update()
        {
            if (Keyboard.current != null && Keyboard.current.escapeKey.wasPressedThisFrame)
            {
                // 1. If Settings is open, close it.
                var settings = UnityEngine.Object.FindFirstObjectByType<SettingsUI>(UnityEngine.FindObjectsInactive.Exclude);
                if (settings != null && settings.gameObject.activeInHierarchy)
                {
                    settings.Hide();
                    return;
                }

                // 2. If Backlog is open, close it.
                var backlog = UnityEngine.Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include);
                if (backlog != null && backlog.IsOpen)
                {
                    backlog.HideBacklog();
                    return;
                }

                // 3. If Extra is open, close it.
                var extra = UnityEngine.Object.FindFirstObjectByType<ExtraUI>(UnityEngine.FindObjectsInactive.Exclude);
                if (extra != null && extra.gameObject.activeInHierarchy)
                {
                    extra.Hide();
                    return;
                }

                // 4. Otherwise, open settings
                if (settingsUI != null && !settingsUI.activeSelf)
                {
                    settingsUI.SetActive(true);
                    
                    // Also attempt to call Show() if it has one
                    var settingsComp = settingsUI.GetComponent<SettingsUI>();
                    if (settingsComp != null) settingsComp.Show();
                }
            }
        }

        public void ToggleSettings()
        {
            if (settingsUI != null)
            {
                bool willBeActive = !settingsUI.activeSelf;
                settingsUI.SetActive(willBeActive);
                
                if (willBeActive)
                {
                    var comp = settingsUI.GetComponent<SettingsUI>();
                    if (comp != null) comp.Show();
                }
                else
                {
                    var comp = settingsUI.GetComponent<SettingsUI>();
                    if (comp != null) comp.Hide();
                }
            }
        }
    }
}
