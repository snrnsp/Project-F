filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

bad_idx = -1
for i, line in enumerate(lines):
    if 'StartCoroutine(PlaySplashSequence());' in line:
        bad_idx = i
        break

if bad_idx != -1:
    lines.pop(bad_idx)
    # Insert it inside Start(), right after GameManager.Instance.OnPhaseChanged += OnPhaseChanged;
    for i, line in enumerate(lines):
        if 'GameManager.Instance.OnPhaseChanged += OnPhaseChanged;' in line:
            lines.insert(i + 2, '            StartCoroutine(PlaySplashSequence());\n')
            break

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Fixed StartCoroutine placement.")
