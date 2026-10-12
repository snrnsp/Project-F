import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/Dialogue/DialogueManager.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''            string bgm = null;\r?\n\s*if \(ui != null && currentDialogue\.nodes != null\)\r?\n\s*\{\r?\n\s*// To restore state, we simulate the visual/audio progression up to the target node\r?\n\s*// This ensures all non-text nodes \(which aren't in rewindHistory\) are properly applied\.\r?\n\s*foreach \(var n in currentDialogue\.nodes\)\r?\n\s*\{\r?\n\s*if \(n\.id > targetNode\.id\) break;\r?\n\s*ui\.UpdateVisualsOnly\(n, true\);\r?\n\s*if \(!string\.IsNullOrEmpty\(n\.command\)\)\r?\n\s*\{\r?\n\s*if \(n\.command\.StartsWith\("AUDIO:PLAY_BGM:"\)\) bgm = n\.command\.Substring\("AUDIO:PLAY_BGM:"\.Length\);\r?\n\s*else if \(n\.command == "AUDIO:STOP_BGM"\) bgm = null;\r?\n\s*\}\r?\n\s*\}\r?\n\s*\}\r?\n\s*// 3\.5 Restore the BGM that was playing at the target point and silence leftover SFX\r?\n\s*var audio = HalloweenVN\.Core\.AudioManager\.Instance;\r?\n\s*if \(audio != null\)\r?\n\s*\{\r?\n\s*audio\.StopAllSFX\(\);\r?\n\s*if \(string\.IsNullOrEmpty\(bgm\)\) audio\.StopBGM\(0\.5f\);\r?\n\s*else audio\.PlayBGM\(bgm\);\r?\n\s*\}'''

replacement = r'''            bool bgmFoundInCurrent = false;
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
                        if (n.command.StartsWith("AUDIO:PLAY_BGM:"))
                        {
                            bgm = n.command.Substring("AUDIO:PLAY_BGM:".Length);
                            bgmFoundInCurrent = true;
                        }
                        else if (n.command == "AUDIO:STOP_BGM")
                        {
                            bgm = null;
                            bgmFoundInCurrent = true;
                        }
                    }
                }
            }
            
            // If BGM wasn't changed in the current chapter's nodes up to this point,
            // we must check the cross-chapter backlog history to see what was playing before.
            if (!bgmFoundInCurrent && rewindHistory != null)
            {
                for (int i = rewindHistory.Count - 1; i >= 0; i--)
                {
                    var n = rewindHistory[i].node;
                    if (n != null && !string.IsNullOrEmpty(n.command))
                    {
                        if (n.command.StartsWith("AUDIO:PLAY_BGM:"))
                        {
                            bgm = n.command.Substring("AUDIO:PLAY_BGM:".Length);
                            break;
                        }
                        else if (n.command == "AUDIO:STOP_BGM")
                        {
                            bgm = null;
                            break;
                        }
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
            }'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed RewindTo BGM fallback logic!")
else:
    print("Failed to match RewindTo BGM fallback logic!")
