import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''        private static float\[\] ComputeLayoutTargets\(string\[\] owner\)\r?\n\s*\{\r?\n\s*float\[\] result = \{ 0\.25f, 0\.5f, 0\.75f \};\r?\n\s*for \(int s = 0; s < 3; s\+\+\)\r?\n\s*\{\r?\n\s*if \(owner\[s\] == null\) continue;\r?\n\s*float target = 0\.5f;\r?\n\s*if \(s == 0\) target = 0\.25f;\r?\n\s*else if \(s == 1\) target = 0\.5f;\r?\n\s*else if \(s == 2\) target = 0\.75f;\r?\n\s*// Character specific visual offsets to account for sprite widths\r?\n\s*if \(owner\[s\] == "리나"\) // 850px \(narrow\)\r?\n\s*\{\r?\n\s*if \(target < 0\.5f\) target \+= 0\.05f;\r?\n\s*else if \(target > 0\.5f\) target -= 0\.05f;\r?\n\s*\}\r?\n\s*result\[s\] = target;\r?\n\s*\}\r?\n\s*return result;\r?\n\s*\}'''

replacement = r'''        private static float[] ComputeLayoutTargets(string[] owner)
        {
            // Shifted the base left/right anchors slightly to the right (0.28, 0.78) 
            // to counteract the characters' visual mass making the scene feel left-heavy.
            float[] result = { 0.28f, 0.5f, 0.78f };
            for (int s = 0; s < 3; s++)
            {
                if (owner[s] == null) continue;
                
                float target = 0.5f;
                if (s == 0) target = 0.28f;
                else if (s == 1) target = 0.5f;
                else if (s == 2) target = 0.78f;
                
                // Character specific visual offsets to account for sprite widths
                if (owner[s] == "리나") // 850px (narrow)
                {
                    if (target < 0.5f) target += 0.05f;
                    else if (target > 0.5f) target -= 0.05f;
                }
                else if (owner[s] == "하루카")
                {
                    // Haruka's sprite has a lot of hair extending to the right, which pushes her body left visually.
                    if (target > 0.5f) target += 0.03f; 
                }
                
                result[s] = target;
            }
            return result;
        }'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed ComputeLayoutTargets in DialogueUI!")
else:
    print("Failed to match ComputeLayoutTargets!")
