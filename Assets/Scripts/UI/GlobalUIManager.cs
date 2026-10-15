using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;

namespace HalloweenVN.UI
{
    public class GlobalUIManager : MonoBehaviour
    {
        [SerializeField] private GameObject settingsUI;

        private LanguageUI _cachedLangUi;
        private SettingsUI _cachedSettingsUi;
        private BacklogUI _cachedBacklogUi;
        private ExtraUI _cachedExtraUi;
        private LobbyUI _cachedLobbyUi;
        private DialogueUI _cachedDialogueUi;

        public void Initialize(GameObject settingsUiObj)
        {
            this.settingsUI = settingsUiObj;
            if (settingsUiObj != null) _cachedSettingsUi = settingsUiObj.GetComponent<SettingsUI>();
        }

        void Update()
        {
            bool escPressed = Keyboard.current != null && Keyboard.current.escapeKey.wasPressedThisFrame;
            bool rightClickPressed = Mouse.current != null && Mouse.current.rightButton.wasPressedThisFrame;

            if (!escPressed && !rightClickPressed) return;

            // 0. If LanguageUI is open, close it.
            if (_cachedLangUi == null) _cachedLangUi = UnityEngine.Object.FindFirstObjectByType<LanguageUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedLangUi != null && _cachedLangUi.gameObject.activeInHierarchy)
            {
                _cachedLangUi.Hide();
                return;
            }

            // 1. If Settings is open, close any open sub-panel first, then close Settings.
            if (_cachedSettingsUi == null) _cachedSettingsUi = UnityEngine.Object.FindFirstObjectByType<SettingsUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedSettingsUi != null && _cachedSettingsUi.gameObject.activeInHierarchy)
            {
                if (_cachedSettingsUi.TryCloseSubPanels()) return;
                _cachedSettingsUi.Hide();
                return;
            }

            // 2. If Backlog is open, dismiss rewind confirmation popup first, then close Backlog.
            if (_cachedBacklogUi == null) _cachedBacklogUi = UnityEngine.Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedBacklogUi != null && _cachedBacklogUi.IsOpen)
            {
                if (_cachedBacklogUi.HasActivePopup)
                {
                    _cachedBacklogUi.DismissActivePopup();
                    return;
                }
                _cachedBacklogUi.HideBacklog();
                return;
            }

            // 3. If Extra is open, close it.
            if (_cachedExtraUi == null) _cachedExtraUi = UnityEngine.Object.FindFirstObjectByType<ExtraUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedExtraUi != null && _cachedExtraUi.gameObject.activeInHierarchy)
            {
                _cachedExtraUi.Hide();
                return;
            }

            // 4. If Lobby has an active warning popup, close it.
            if (_cachedLobbyUi == null) _cachedLobbyUi = UnityEngine.Object.FindFirstObjectByType<LobbyUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedLobbyUi != null && _cachedLobbyUi.gameObject.activeInHierarchy && _cachedLobbyUi.TryCloseActivePopup())
            {
                return;
            }

            // 5. Only ESC opens Settings (Right-Click during dialogue is reserved for hiding/restoring the dialogue UI).
            if (escPressed)
            {
                if (_cachedDialogueUi == null) _cachedDialogueUi = UnityEngine.Object.FindFirstObjectByType<DialogueUI>(UnityEngine.FindObjectsInactive.Include);
                if (_cachedDialogueUi != null && _cachedDialogueUi.gameObject.activeInHierarchy && _cachedDialogueUi.IsUiHidden)
                {
                    _cachedDialogueUi.RestoreHiddenUI();
                    return;
                }

                if (settingsUI != null && !settingsUI.activeSelf)
                {
                    settingsUI.SetActive(true);
                    if (_cachedSettingsUi == null) _cachedSettingsUi = settingsUI.GetComponent<SettingsUI>();
                    if (_cachedSettingsUi != null) _cachedSettingsUi.Show();
                }
            }
        }

        public void ToggleSettings()
        {
            if (settingsUI != null)
            {
                bool willBeActive = !settingsUI.activeSelf;
                settingsUI.SetActive(willBeActive);
                if (_cachedSettingsUi == null) _cachedSettingsUi = settingsUI.GetComponent<SettingsUI>();

                if (willBeActive)
                {
                    if (_cachedSettingsUi != null) _cachedSettingsUi.Show();
                }
                else
                {
                    if (_cachedSettingsUi != null) _cachedSettingsUi.Hide();
                }
            }
        }
    }
}
