import re

with open('Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_method = '''        private static float[] ComputeLayoutTargets(string[] owner)
        {
            float[] result = { 0.25f, 0.5f, 0.75f };
            List<int> used = new List<int>();
            for (int s = 0; s < 3; s++) if (owner[s] != null) used.Add(s);
            float[] xs;
            if (used.Count == 1) xs = new[] { 0.5f };
            else if (used.Count == 2) xs = new[] { 0.25f, 0.75f };
            else xs = new[] { 0.20f, 0.50f, 0.80f };
            
            for (int i = 0; i < used.Count; i++)
            {
                int s = used[i];
                float target = xs[i];
                string name = owner[s];
                
                // Character specific visual offsets to account for sprite widths
                if (name == "리나") // 850px (narrow)
                {
                    if (target < 0.5f) target += 0.05f;
                    else if (target > 0.5f) target -= 0.05f;
                }
                
                result[s] = target;
            }
            return result;
        }'''

new_method = '''        private static float[] ComputeLayoutTargets(string[] owner)
        {
            float[] result = { 0.25f, 0.5f, 0.75f };
            bool centerUsed = owner[1] != null;
            
            for (int s = 0; s < 3; s++)
            {
                if (owner[s] == null) continue;
                
                float target = 0.5f;
                if (s == 0) target = centerUsed ? 0.2f : 0.25f;      // Left slot
                else if (s == 1) target = 0.5f;                      // Center slot (Always fixed)
                else if (s == 2) target = centerUsed ? 0.8f : 0.75f; // Right slot
                
                // Character specific visual offsets to account for sprite widths
                if (owner[s] == "리나") // 850px (narrow)
                {
                    if (target < 0.5f) target += 0.05f;
                    else if (target > 0.5f) target -= 0.05f;
                }
                
                result[s] = target;
            }
            return result;
        }'''

if old_method in content:
    content = content.replace(old_method, new_method)
    with open('Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Patched ComputeLayoutTargets to use strict slots successfully!")
else:
    print("Could not find old_method in DialogueUI.cs.")
