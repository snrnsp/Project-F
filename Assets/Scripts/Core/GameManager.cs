using UnityEngine;
using System;

namespace HalloweenVN.Core
{
    /// <summary>
    /// Manages the core game state and phase transitions.
    /// </summary>
    public class GameManager : MonoBehaviour
    {
        public static GameManager Instance { get; private set; }
        
        public GamePhase CurrentPhase { get; private set; } = GamePhase.Lobby;
        
        public event Action<GamePhase> OnPhaseChanged;
        
        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);

            // Create ScreenEffects Manager
            GameObject fx = new GameObject("ScreenEffects");
            fx.AddComponent<HalloweenVN.Effects.ScreenEffects>();
            DontDestroyOnLoad(fx);
        }
        
        /// <summary>
        /// Changes the current game phase and notifies listeners.
        /// </summary>
        /// <param name="newPhase">The new game phase.</param>
        public void ChangePhase(GamePhase newPhase)
        {
            CurrentPhase = newPhase;
            OnPhaseChanged?.Invoke(CurrentPhase);
            
            if (CurrentPhase != GamePhase.Lobby)
            {
                SaveManager.Save(SaveManager.CreateFromCurrentState(0), 0);
            }
        }
        
        private void OnApplicationQuit()
        {
            if (CurrentPhase != GamePhase.Lobby)
            {
                SaveManager.Save(SaveManager.CreateFromCurrentState(0), 0);
            }
        }

        private void OnApplicationPause(bool pauseStatus)
        {
            if (pauseStatus && CurrentPhase != GamePhase.Lobby)
            {
                SaveManager.Save(SaveManager.CreateFromCurrentState(0), 0);
            }
        }
    }
}
