import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/Dialogue/DialogueManager.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''        public void RewindTo\(string targetDialogueId, DialogueNode targetNode, System\.Collections\.Generic\.List<HalloweenVN\.UI\.BacklogUI\.BacklogEntry> rewindHistory\)\r?\n\s*\{\r?\n.*?DisplayNode\(currentNode\.id\);\r?\n\s*\}'''

replacement = r'''        public void RewindTo(string targetDialogueId, DialogueNode targetNode, System.Collections.Generic.List<HalloweenVN.UI.BacklogUI.BacklogEntry> rewindHistory)
        {
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            
            // 1. Load Dialogue Container
            if (!dialogueCache.TryGetValue(targetDialogueId, out currentDialogue))
            {
                currentDialogue = HalloweenVN.Data.DataLoader.LoadDialogue(targetDialogueId);
                if (currentDialogue != null)
                {
                    dialogueCache[targetDialogueId] = currentDialogue;
                }
            }
            if (currentDialogue == null) return;
            BuildNodeLookup();
            
            // 2. Clear current visual state
            var ui = UnityEngine.Object.FindAnyObjectByType<HalloweenVN.UI.DialogueUI>();
            if (ui != null)
            {
                ui.ClearAll();
            }
            
            string bgm = null;
            if (ui != null && currentDialogue.nodes != null)
            {
                // To restore state, we simulate the visual/audio progression up to the target node
                // This ensures all non-text nodes (which aren't in rewindHistory) are properly applied.
                foreach (var n in currentDialogue.nodes)
                {
                    if (n.id > targetNode.id) break;
                    
                    ui.UpdateVisualsOnly(n, true);
                    
                    if (!string.IsNullOrEmpty(n.command))
                    {
                        if (n.command.StartsWith("AUDIO:PLAY_BGM:")) bgm = n.command.Substring("AUDIO:PLAY_BGM:".Length);
                        else if (n.command == "AUDIO:STOP_BGM") bgm = null;
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

            // 4. Resume from target node
            currentNode = targetNode;
            IsPlaying = true;
            
            // Display it
            DisplayNode(currentNode.id);
        }'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed RewindTo in DialogueManager!")
else:
    print("Failed to match RewindTo!")
