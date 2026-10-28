using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using HalloweenVN.Core;
using HalloweenVN.Data;

namespace HalloweenVN.Dialogue
{
    public class DialogueManager : MonoBehaviour
    {
        public static DialogueManager Instance { get; private set; }

        public event Action OnDialogueStarted;
        public event Action OnDialogueEnded;
        public event Action<DialogueNode> OnNodeDisplayed;
        public event Action<List<DialogueChoice>> OnChoicesDisplayed;

        public bool IsPlaying { get; private set; }
        public bool IsTransitioningChapter { get; private set; }

        private static Dictionary<string, DialogueContainer> dialogueCache = new Dictionary<string, DialogueContainer>();
        private Dictionary<int, DialogueNode> nodeLookup = new Dictionary<int, DialogueNode>();

        private DialogueContainer currentDialogue;
        public DialogueContainer CurrentDialogue => currentDialogue;
        public string CurrentDialogueId => currentDialogue?.dialogueId;
        private DialogueNode currentNode;
        public DialogueNode CurrentNode => currentNode;
        private string pendingCommand;
        private bool isTyping;
        private Coroutine typingCoroutine;
        private int transitionGeneration;

        private void Awake()
        {
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
                dialogueCache.Clear(); // Added to ensure hot-reloading JSON changes works properly
            }
            else
            {
                Destroy(gameObject);
            }
        }

        private void OnEnable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
            }
        }

        private void OnDisable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
            }
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            // Dialogues could still be played during Investigation or other phases,
            // so we don't necessarily disable completely, but we can hook in phase logic if needed.
        }

        /// <summary>
        /// Starts a dialogue loaded from the specified ID.
        /// </summary>
        /// <param name="dialogueId">The ID of the dialogue to load.</param>
        public void StartDialogue(string dialogueId)
        {
            Debug.Log($"[DialogueManager] StartDialogue called with id: {dialogueId}");
            if (!dialogueCache.TryGetValue(dialogueId, out DialogueContainer container))
            {
                container = DataLoader.LoadDialogue(dialogueId);
                if (container != null)
                {
                    dialogueCache[dialogueId] = container;
                }
            }

            if (container != null)
            {
                Debug.Log($"[DialogueManager] Loaded dialogue '{dialogueId}' with {container.nodes?.Count ?? 0} nodes");
                StartDialogue(container);
            }
            else
            {
                Debug.LogError($"Dialogue with ID {dialogueId} not found.");
            }
        }

        /// <summary>
        /// Starts a dialogue using the provided container.
        /// </summary>
        /// <param name="container">The dialogue container.</param>
        private void BuildNodeLookup()
        {
            nodeLookup.Clear();
            if (currentDialogue != null && currentDialogue.nodes != null)
            {
                foreach (var node in currentDialogue.nodes)
                {
                    nodeLookup[node.id] = node;
                }
            }
        }

        public void StartDialogue(DialogueContainer container)
        {
            HalloweenVN.Effects.ScreenEffects.Instance?.StopShake();
            currentDialogue = container;
            BuildNodeLookup();
            IsPlaying = true;
            OnDialogueStarted?.Invoke();
            
            if (currentDialogue != null && !string.IsNullOrEmpty(currentDialogue.initialBgm))
            {
                HalloweenVN.Core.AudioManager.Instance?.PlayBGM(currentDialogue.initialBgm);
            }
            
            if (currentDialogue != null && currentDialogue.nodes != null && currentDialogue.nodes.Count > 0)
            {
                DisplayNode(currentDialogue.nodes[0].id);
            }
            else
            {
                EndDialogue();
            }
        }

        /// <summary>
        /// Displays a specific dialogue node by ID.
        /// </summary>
        /// <param name="nodeId">The node ID to display.</param>
        
        private static readonly string[] StoryChapterOrder = {
            "ch0_origin",
            "ch0_gathering",
            "ch0_opening",
            "ch1_morning",
            "ch1_night",
            "ch1_investigation_talk",
            "ch1_result_perfect",
            "ch1_resolution",
            "ch1_epilogue"
        };

        private static string GetDefaultChapterBgm(string dialogueId)
        {
            switch (dialogueId)
            {
                case "ch0_origin":
                case "ch0_gathering":
                case "ch0_opening":
                    return "bgm_office_night";
                case "ch1_morning":
                    return "bgm_office_day";
                case "ch1_night":
                case "ch1_investigation_talk":
                case "ch1_result_perfect":
                case "ch1_result_fail":
                case "ch1_resolution":
                    return "bgm_investigation";
                default:
                    return null;
            }
        }

        private DialogueContainer GetOrLoadContainer(string dialogueId)
        {
            if (string.IsNullOrEmpty(dialogueId)) return null;
            if (!dialogueCache.TryGetValue(dialogueId, out DialogueContainer container))
            {
                container = HalloweenVN.Data.DataLoader.LoadDialogue(dialogueId);
                if (container != null)
                {
                    dialogueCache[dialogueId] = container;
                }
            }
            return container;
        }

        public void RewindTo(string targetDialogueId, DialogueNode targetNode, System.Collections.Generic.List<HalloweenVN.UI.BacklogUI.BacklogEntry> rewindHistory)
        {
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            transitionGeneration++;
            IsTransitioningChapter = false;
            pendingCommand = null;
            
            // 1. Load Dialogue Container
            currentDialogue = GetOrLoadContainer(targetDialogueId);
            if (currentDialogue == null) return;
            BuildNodeLookup();
            
            // 2. Clear current visual state
            var ui = UnityEngine.Object.FindAnyObjectByType<HalloweenVN.UI.DialogueUI>();
            if (ui != null)
            {
                ui.ClearAll();
                ui.StartPreloadCurrentChapter();
            }
            
            string initialChapterBgm = !string.IsNullOrEmpty(currentDialogue.initialBgm)
                ? currentDialogue.initialBgm
                : GetDefaultChapterBgm(targetDialogueId);
            bool bgmFoundInCurrent = !string.IsNullOrEmpty(currentDialogue.initialBgm);
            string bgm = initialChapterBgm;
            bool shouldShakeContinuously = false;
            if (currentDialogue.nodes != null)
            {
                // Simulate the visual/audio progression up to the target node.
                // Visuals for strictly prior nodes (n.id < targetNode.id) reconstruct background and narrator-return state;
                // targetNode visuals are applied cleanly once by DisplayNode(currentNode.id).
                foreach (var n in currentDialogue.nodes)
                {
                    if (n.id > targetNode.id) break;
                    
                    if (n.id < targetNode.id && ui != null)
                    {
                        ui.UpdateVisualsOnly(n, true);
                    }
                    if (TryGetBgmCommand(n.command, out string nodeBgm))
                    {
                        bgm = nodeBgm;
                        bgmFoundInCurrent = true;
                    }
                    if (n.id < targetNode.id && TryGetShakeLoopCommand(n.command, out bool shakeLoop))
                    {
                        shouldShakeContinuously = shakeLoop;
                    }
                }
            }
            
            // If BGM wasn't explicitly changed in the current chapter's nodes up to this point,
            // check the cross-chapter backlog history to see what was playing before.
            if (!bgmFoundInCurrent && rewindHistory != null)
            {
                for (int i = rewindHistory.Count - 1; i >= 0; i--)
                {
                    var n = rewindHistory[i].node;
                    if (n != null && TryGetBgmCommand(n.command, out string historyBgm))
                    {
                        bgm = historyBgm;
                        bgmFoundInCurrent = true;
                        break;
                    }
                }
            }
            
            // 3.5 Restore the BGM that was playing at the target point and silence leftover SFX
            var audio = HalloweenVN.Core.AudioManager.Instance;
            if (audio != null)
            {
                audio.StopAllSFX();
                if (string.IsNullOrEmpty(bgm)) audio.StopBGM(0.5f);
                else audio.PlayBGM(bgm);
            }

            var fx = HalloweenVN.Effects.ScreenEffects.Instance;
            if (fx != null)
            {
                fx.ClearOverlays();
                if (shouldShakeContinuously) fx.StartContinuousShake(10f);
                else fx.StopShake();
            }

            // 4. Resume from target node
            currentNode = FindNode(targetNode.id) ?? targetNode;
            IsPlaying = true;
            
            // Display it
            DisplayNode(currentNode.id);
        }

        public void ResumeDialogue(string dialogueId, int nodeId, bool hasAudioState = false, string savedBgm = null)
        {
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            transitionGeneration++;
            IsTransitioningChapter = false;
            pendingCommand = null;
            
            currentDialogue = GetOrLoadContainer(dialogueId);
            if (currentDialogue == null) return;
            BuildNodeLookup();
            
            var ui = UnityEngine.Object.FindAnyObjectByType<HalloweenVN.UI.DialogueUI>();
            if (ui != null)
            {
                ui.ClearAll();
                ui.StartPreloadCurrentChapter();
            }

            string defaultBgm = !string.IsNullOrEmpty(currentDialogue.initialBgm)
                ? currentDialogue.initialBgm
                : GetDefaultChapterBgm(dialogueId);
            string bgm = hasAudioState ? savedBgm : defaultBgm;
            bool shouldShakeContinuously = false;
            HalloweenVN.UI.BacklogUI.ClearHistory();

            // Reconstruct preceding linear chapters into Backlog so players continuing from a save
            // still have their recent cross-chapter log history available.
            int chapIdx = System.Array.IndexOf(StoryChapterOrder, dialogueId);
            for (int c = 0; c < chapIdx; c++)
            {
                DialogueContainer prevContainer = GetOrLoadContainer(StoryChapterOrder[c]);
                if (prevContainer?.nodes == null) continue;
                foreach (var prevNode in prevContainer.nodes)
                {
                    HalloweenVN.UI.BacklogUI.RecordNodeSilently(StoryChapterOrder[c], prevNode);
                }
            }

            if (currentDialogue.nodes != null)
            {
                // To restore state, we simulate the visual/audio progression up to the target node
                foreach (var n in currentDialogue.nodes)
                {
                    if (n.id > nodeId) break;
                    
                    if (n.id < nodeId && ui != null)
                    {
                        ui.UpdateVisualsOnly(n, true);
                    }
                    if (TryGetBgmCommand(n.command, out string nodeBgm)) bgm = nodeBgm;
                    if (n.id < nodeId)
                    {
                        if (TryGetShakeLoopCommand(n.command, out bool shakeLoop))
                        {
                            shouldShakeContinuously = shakeLoop;
                        }
                        HalloweenVN.UI.BacklogUI.RecordNodeSilently(dialogueId, n);
                    }
                }
            }
            
            var audio = HalloweenVN.Core.AudioManager.Instance;
            if (audio != null)
            {
                audio.StopAllSFX();
                if (!string.IsNullOrEmpty(bgm)) audio.PlayBGM(bgm);
                else audio.StopBGM();
            }

            var fx = HalloweenVN.Effects.ScreenEffects.Instance;
            if (fx != null)
            {
                fx.ClearOverlays();
                if (shouldShakeContinuously) fx.StartContinuousShake(10f);
                else fx.StopShake();
            }

            currentNode = FindNode(nodeId);
            if (currentNode == null && currentDialogue.nodes.Count > 0) currentNode = currentDialogue.nodes[0];
            
            IsPlaying = true;
            if (currentNode != null) DisplayNode(currentNode.id);
        }

        /// <summary>
        /// After a backlog rewind the music must match the target point
        /// (e.g. rewinding from the ending piano back into the climax).
        /// Finds the last BGM command before the target node; falls back to the dialogue's first node.
        /// </summary>
        private void RestoreAudioForRewind(System.Collections.Generic.List<HalloweenVN.UI.BacklogUI.BacklogEntry> rewindHistory)
        {
            var audio = HalloweenVN.Core.AudioManager.Instance;
            if (audio == null) return;
            audio.StopAllSFX();

            string bgm = null;
            bool found = false;
            if (rewindHistory != null)
            {
                for (int i = rewindHistory.Count - 1; i >= 0 && !found; i--)
                {
                    var n = rewindHistory[i].node;
                    if (n != null) found = TryGetBgmCommand(n.command, out bgm);
                }
            }
            if (!found && currentDialogue != null && currentDialogue.nodes != null && currentDialogue.nodes.Count > 0)
            {
                found = TryGetBgmCommand(currentDialogue.nodes[0].command, out bgm);
            }
            if (!found) return;

            if (string.IsNullOrEmpty(bgm)) audio.StopBGM(0.5f);
            else audio.PlayBGM(bgm);
        }

        /// <summary>Returns true if the command string contains a BGM change. bgm is null for STOP_BGM.</summary>
        private static bool TryGetBgmCommand(string command, out string bgm)
        {
            bgm = null;
            if (string.IsNullOrEmpty(command)) return false;
            bool found = false;
            foreach (string raw in command.Split(';'))
            {
                string cmd = raw.Trim();
                if (cmd.StartsWith("AUDIO:PLAY_BGM:")) { bgm = cmd.Substring("AUDIO:PLAY_BGM:".Length); found = true; }
                else if (cmd == "AUDIO:STOP_BGM") { bgm = null; found = true; }
            }
            return found;
        }

        private static bool TryGetShakeLoopCommand(string command, out bool shakeLoop)
        {
            shakeLoop = false;
            if (string.IsNullOrEmpty(command)) return false;
            bool found = false;
            foreach (string raw in command.Split(';'))
            {
                string cmd = raw.Trim();
                if (cmd == "EFFECT:SHAKE_START" || cmd == "EFFECT:SHAKE_LOOP") { shakeLoop = true; found = true; }
                else if (cmd == "EFFECT:SHAKE_STOP") { shakeLoop = false; found = true; }
            }
            return found;
        }

        public void DisplayNode(int nodeId)
        {
            currentNode = FindNode(nodeId);
            if (currentNode == null)
            {
                EndDialogue();
                return;
            }

            pendingCommand = null;

            if (!string.IsNullOrEmpty(currentNode.command))
            {
                // A node may carry several commands separated by ';'
                // (e.g. "AUDIO:PLAY_BGM:bgm_climax;EFFECT:SHAKE").
                string flowCommand = null;
                foreach (string raw in currentNode.command.Split(';'))
                {
                    string cmd = raw.Trim();
                    if (cmd.Length == 0) continue;
                    if (cmd.StartsWith("EFFECT:") || cmd.StartsWith("AUDIO:"))
                    {
                        // Effects and Audio trigger immediately with the text
                        ExecuteCommand(cmd);
                    }
                    else
                    {
                        flowCommand = cmd;
                    }
                }

                if (flowCommand != null)
                {
                    // Flow commands (CHANGE_PHASE, etc.) are deferred if there's text
                    bool hasText = !string.IsNullOrEmpty(currentNode.text);
                    if (hasText)
                    {
                        pendingCommand = flowCommand;
                    }
                    else
                    {
                        ExecuteCommand(flowCommand);
                        return;
                    }
                }
                else if (string.IsNullOrWhiteSpace(currentNode.text) &&
                         (currentNode.choices == null || currentNode.choices.Count == 0) &&
                         currentNode.nextNodeId != -1)
                {
                    // Effect/audio-only node with no text: advance immediately so an empty narrator screen is not shown
                    DisplayNode(currentNode.nextNodeId);
                    return;
                }
            }
            
            if (currentNode.nextNodeId == -1 && string.IsNullOrEmpty(currentNode.command) && (currentNode.choices == null || currentNode.choices.Count == 0))
            {
                // This indicates the end, but we still display the node text first.
                // AdvanceDialogue will handle the termination.
            }

            OnNodeDisplayed?.Invoke(currentNode);
            
            // Auto Save
            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase != GamePhase.Lobby)
            {
                SaveManager.Save(SaveManager.CreateFromCurrentState(0), 0);
            }

            if (currentNode.choices != null && currentNode.choices.Count > 0)
            {
                OnChoicesDisplayed?.Invoke(currentNode.choices);
            }
        }

        /// <summary>
        /// Executes a dialogue command (CHANGE_PHASE, START_DIALOGUE, END).
        /// </summary>
        private void ExecuteCommand(string command)
        {
            if (command.StartsWith("AUDIO:"))
            {
                if (HalloweenVN.Core.AudioManager.Instance == null) return;
                string audioCmd = command.Substring("AUDIO:".Length);
                if (audioCmd.StartsWith("PLAY_BGM:"))
                {
                    HalloweenVN.Core.AudioManager.Instance.PlayBGM(audioCmd.Substring("PLAY_BGM:".Length));
                }
                else if (audioCmd == "STOP_BGM")
                {
                    HalloweenVN.Core.AudioManager.Instance.StopBGM();
                }
                else if (audioCmd.StartsWith("PLAY_SFX_FADEOUT:"))
                {
                    string[] parts = audioCmd.Substring("PLAY_SFX_FADEOUT:".Length).Split(',');
                    if (parts.Length == 3)
                    {
                        HalloweenVN.Core.AudioManager.Instance.PlaySFX(parts[0], float.Parse(parts[1], System.Globalization.CultureInfo.InvariantCulture), float.Parse(parts[2], System.Globalization.CultureInfo.InvariantCulture));
                    }
                }
                else if (audioCmd.StartsWith("PLAY_SFX:"))
                {
                    HalloweenVN.Core.AudioManager.Instance.PlaySFX(audioCmd.Substring("PLAY_SFX:".Length));
                }
            }
            else if (command.StartsWith("EFFECT:"))
            {
                string effectType = command.Substring("EFFECT:".Length);
                var fx = HalloweenVN.Effects.ScreenEffects.Instance;
                if (fx != null)
                {
                    switch (effectType)
                    {
                        case "SHAKE": fx.ShakeCamera(0.5f, 10f); break;
                        case "SHAKE_SHORT":
                        case "SHAKE_LIGHT": fx.ShakeCamera(0.25f, 6f); break;
                        case "SHAKE_HEAVY": fx.ShakeCamera(0.65f, 14f); break;
                        case "SHAKE_START":
                        case "SHAKE_LOOP": fx.StartContinuousShake(10f); break;
                        case "SHAKE_STOP": fx.StopShake(0.8f); break;
                        case "FLASH": fx.FlashScreen(Color.white); break;
                        case "FLASH_RED": fx.FlashScreen(Color.red); break;
                        case "FADE_TO_BLACK": fx.FadeToBlack(); break;
                        case "FADE_FROM_BLACK": fx.FadeFromBlack(); break;
                    }
                }
            }
            else if (command.StartsWith("CHANGE_PHASE:"))
            {
                string phaseString = command.Substring("CHANGE_PHASE:".Length);
                if (Enum.TryParse(phaseString, out GamePhase phase))
                {
                    EndDialogue();
                    GameManager.Instance.ChangePhase(phase);
                }
            }
            else if (command.StartsWith("START_DIALOGUE:"))
            {
                string nextDialogueId = command.Substring("START_DIALOGUE:".Length);
                StartCoroutine(TransitionToNextDialogue(nextDialogueId));
            }
            else if (command == "END")
            {
                EndDialogue();
                var fx = HalloweenVN.Effects.ScreenEffects.Instance;
                if (fx != null) fx.FadeFromBlack(1f); // 남아있는 검은 화면 페이드 제거
                
                if (GameManager.Instance != null)
                {
                    GameManager.Instance.ChangePhase(GamePhase.Lobby);
                }
            }
        }

        private IEnumerator TransitionToNextDialogue(string nextDialogueId)
        {
            int generation = transitionGeneration;
            var fx = HalloweenVN.Effects.ScreenEffects.Instance;
            if (fx != null)
            {
                IsPlaying = false; // Prevent clicks during fade out
                
                // Fade to black
                yield return fx.FadeToBlack(1f);
                if (generation != transitionGeneration) yield break;
                
                // Wait 1 second in darkness, skipping if Ctrl is pressed
                float waitElapsed = 0f;
                while (waitElapsed < 1f)
                {
                    if (generation != transitionGeneration) yield break;
                    bool isFastForwarding = HalloweenVN.Core.SettingsData.IsSkipKeyPressed();
                    
                    waitElapsed += Time.unscaledDeltaTime * (isFastForwarding ? 10f : 1f);
                    yield return null;
                }
                
                if (generation != transitionGeneration) yield break;
                // Change the scene behind the black screen
                IsTransitioningChapter = true;
                EndDialogue();
                StartDialogue(nextDialogueId);
                IsTransitioningChapter = false;
                
                // Fade from black
                yield return fx.FadeFromBlack(1f);
            }
            else
            {
                IsTransitioningChapter = true;
                EndDialogue();
                StartDialogue(nextDialogueId);
                IsTransitioningChapter = false;
            }
        }

        /// <summary>
        /// Advances the dialogue to the next node, or ends it if there are no more nodes.
        /// </summary>
        public void AdvanceDialogue()
        {
            if (currentNode == null || !IsPlaying) return;

            if (currentNode.choices != null && currentNode.choices.Count > 0)
            {
                return;
            }

            // If there's a pending command (text was shown, now execute)
            if (!string.IsNullOrEmpty(pendingCommand))
            {
                string cmd = pendingCommand;
                pendingCommand = null;
                ExecuteCommand(cmd);
                return;
            }

            if (currentNode.nextNodeId != -1)
            {
                DisplayNode(currentNode.nextNodeId);
            }
            else
            {
                EndDialogue();
            }
        }

        /// <summary>
        /// Selects a dialogue choice and proceeds to its target node.
        /// </summary>
        /// <param name="choiceIndex">The index of the choice selected.</param>
        public void SelectChoice(int choiceIndex)
        {
            if (currentNode != null && currentNode.choices != null && choiceIndex >= 0 && choiceIndex < currentNode.choices.Count)
            {
                int nextId = currentNode.choices[choiceIndex].nextNodeId;
                if (nextId != -1)
                {
                    DisplayNode(nextId);
                }
                else
                {
                    EndDialogue();
                }
            }
        }

        /// <summary>
        /// Ends the current dialogue.
        /// </summary>
        public void EndDialogue()
        {
            HalloweenVN.Effects.ScreenEffects.Instance?.StopShake();
            transitionGeneration++;
            pendingCommand = null;
            IsPlaying = false;
            currentDialogue = null;
            currentNode = null;
            OnDialogueEnded?.Invoke();
        }

        private DialogueNode FindNode(int nodeId)
        {
            if (nodeLookup.TryGetValue(nodeId, out DialogueNode node))
            {
                return node;
            }
            return null;
        }
    }
}
