import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '// Title Text (Top Left)' in line:
        start_idx = i
    if 'titleOutline.effectDistance =' in line and start_idx != -1:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_code = """        // Title Logo Image (Top Left)
        GameObject titleObj = UIHelper.CreateUIObject("LobbyTitleLogo", lobbyPanelRoot.transform);
        RectTransform titleRt = titleObj.GetComponent<RectTransform>();
        UIHelper.SetAnchors(titleRt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
        titleRt.anchoredPosition = new Vector2(250, 320); // Moved a bit to the right since it's wider
        titleRt.sizeDelta = new Vector2(500, 196); // 1999x786 aspect ratio
        Image lobbyTitleLogo = UIHelper.AddImage(titleObj, Color.white);
        lobbyTitleLogo.preserveAspect = true;
"""
    lines[start_idx:end_idx+1] = [new_code]

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated properly")
