import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'UIHelper.SetField(lobbyUi, "continueButton", null);' in line:
        start_idx = i
    if 'UIHelper.SetField(lobbyUi, "continueText", null);' in line and start_idx != -1:
        end_idx = i
        break

print(f"Start: {start_idx}, End: {end_idx}")

if start_idx != -1 and end_idx != -1:
    lines[start_idx] = '            UIHelper.SetField(lobbyUi, "continueButton", continueBtn);\n'
    lines[end_idx] = '            UIHelper.SetField(lobbyUi, "continueText", continueTuple.text);\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Replaced Attach Logic.")
else:
    print("Could not find the block.")
