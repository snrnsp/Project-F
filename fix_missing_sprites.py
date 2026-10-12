import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'// 2\. New owner per slot.*?newNames\.Add\(name\);\r?\n\s*\}'

replacement = r'''// 2. New owner per slot (same character listed twice — keep the first slot only)
            string[] newOwner = new string[3];
            HashSet<string> newNames = new HashSet<string>();
            for (int s = 0; s < 3; s++)
            {
                if (string.IsNullOrEmpty(requested[s])) continue;
                
                // If the sprite doesn't actually exist in the game, treat it as empty
                Sprite testSp = LoadSpriteCached(requested[s]);
                if (testSp == null)
                {
                    string fallback = null;
                    int slash = requested[s].LastIndexOf('/');
                    if (slash > 0) fallback = requested[s].Substring(0, slash) + "/기본";
                    if (fallback != null) testSp = LoadSpriteCached(fallback);
                }
                
                if (testSp == null)
                {
                    requested[s] = null;
                    continue;
                }

                string name = ExtractBaseName(requested[s]);
                if (newNames.Contains(name)) { requested[s] = null; continue; }
                newOwner[s] = name;
                newNames.Add(name);
            }'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed missing sprite slot allocation!")
else:
    print("Failed to match pattern!")
