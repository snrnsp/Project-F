import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''                        bool isFirst = _activeSpeakerPositions.Count == 1;
                        if (node.slideIn || !isFirst)
                        {
                            // Start from off-screen (left or right depending on target position)
                            float offScreenX = (targetX < 0.5f) ? -0.5f : (targetX > 0.5f ? 1.5f : -0.5f);
                            SetCharacterAnchorX(rt, offScreenX);
                            MoveCharacterTo(assignedPos, targetX);
                        }'''

replacement = '''                        bool isFirst = _activeSpeakerPositions.Count == 1;
                        if (node.slideIn || !isFirst)
                        {
                            // Start from off-screen (left or right depending on target position)
                            float offScreenX = (targetX < 0.5f) ? -0.5f : (targetX > 0.5f ? 1.5f : -0.5f);
                            
                            // 명시적으로 slideFromRight가 true이면 중앙 캐릭터라도 오른쪽에서 등장
                            if (node.slideFromRight) offScreenX = 1.5f;

                            SetCharacterAnchorX(rt, offScreenX);
                            MoveCharacterTo(assignedPos, targetX);
                        }'''

target_win = target.replace('\n', '\r\n')
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated DialogueUI (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated DialogueUI (lf)')
else:
    print('Target not found')
