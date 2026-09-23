import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''            Dictionary<CharacterPosition, float> layoutTargets = new Dictionary<CharacterPosition, float>();
            if (totalChars == 1)
            {
                CharacterPosition? pos = requestedChars[0].explicitPos;
                layoutTargets[pos ?? CharacterPosition.Center] = 0.5f;
            }
            else if (totalChars == 2)
            {
                // Sort by position enum to get consistent left-right order
                var sorted = new List<CharacterPosition?>();
                foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                layoutTargets[sorted[0] ?? CharacterPosition.Left] = 0.34f;
                layoutTargets[sorted[1] ?? CharacterPosition.Right] = 0.78f;
            }
            else if (totalChars >= 3)
            {
                var sorted = new List<CharacterPosition?>();
                foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                layoutTargets[sorted[0] ?? CharacterPosition.Left] = 0.24f;
                layoutTargets[sorted[1] ?? CharacterPosition.Center] = 0.56f;
                layoutTargets[sorted[2] ?? CharacterPosition.Right] = 0.88f;
            }'''

replacement = '''            Dictionary<CharacterPosition, float> layoutTargets = new Dictionary<CharacterPosition, float>();
            if (totalChars == 1)
            {
                CharacterPosition? pos = requestedChars[0].explicitPos;
                layoutTargets[pos ?? CharacterPosition.Center] = 0.5f;
            }
            else if (totalChars == 2)
            {
                var sorted = new List<CharacterPosition?>();
                foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                layoutTargets[sorted[0] ?? CharacterPosition.Left] = 0.25f;
                layoutTargets[sorted[1] ?? CharacterPosition.Right] = 0.75f;
            }
            else if (totalChars >= 3)
            {
                var sorted = new List<CharacterPosition?>();
                foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                layoutTargets[sorted[0] ?? CharacterPosition.Left] = 0.20f;
                layoutTargets[sorted[1] ?? CharacterPosition.Center] = 0.50f;
                layoutTargets[sorted[2] ?? CharacterPosition.Right] = 0.80f;
            }

            // Apply visual offsets for sprites that have off-center bodies
            foreach (var req in requestedChars)
            {
                CharacterPosition assignedPos = req.explicitPos ?? CharacterPosition.Center;
                if (totalChars == 2)
                {
                    var sorted = new List<CharacterPosition?>();
                    foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                    sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                    if (req.explicitPos == sorted[0]) assignedPos = sorted[0] ?? CharacterPosition.Left;
                    if (req.explicitPos == sorted[1]) assignedPos = sorted[1] ?? CharacterPosition.Right;
                }
                else if (totalChars >= 3)
                {
                    var sorted = new List<CharacterPosition?>();
                    foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                    sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                    if (req.explicitPos == sorted[0]) assignedPos = sorted[0] ?? CharacterPosition.Left;
                    if (req.explicitPos == sorted[1]) assignedPos = sorted[1] ?? CharacterPosition.Center;
                    if (req.explicitPos == sorted[2]) assignedPos = sorted[2] ?? CharacterPosition.Right;
                }

                if (layoutTargets.ContainsKey(assignedPos))
                {
                    if (req.baseName == "세이카") layoutTargets[assignedPos] -= 0.08f;
                    else if (req.baseName == "카스미") layoutTargets[assignedPos] -= 0.03f;
                    else if (req.baseName == "미나") layoutTargets[assignedPos] -= 0.03f;
                    else if (req.baseName == "하루카") layoutTargets[assignedPos] -= 0.03f;
                    else if (req.baseName == "리리스") layoutTargets[assignedPos] -= 0.04f;
                }
            }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated DialogueUI to center layouts and apply visual character offsets')
else:
    print('Target not found')
