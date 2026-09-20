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
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
            }
            else
            {
                Destroy(gameObject);
            }
        }
        
        /// <summary>
        /// Changes the current game phase and notifies listeners.
        /// </summary>
        /// <param name="newPhase">The new game phase.</param>
        public void ChangePhase(GamePhase newPhase)
        {
            CurrentPhase = newPhase;
            OnPhaseChanged?.Invoke(CurrentPhase);
        }
    }
}
