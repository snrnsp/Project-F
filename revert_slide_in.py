import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''                        bool isFirst = _activeSpeakerPositions.Count == 1;
                        // noFade가 true이면 페이드 대신 슬라이드 인을 의도한 것일 수 있으므로 조건에 추가
                        if (node.slideIn || !isFirst || node.noFade)
                        {
                            // 중앙(0.5f)일 경우 오른쪽(1.5f)에서 등장하도록 수정 (유저 요청)
                            float offScreenX = (targetX < 0.5f) ? -0.5f : 1.5f;
                            SetCharacterAnchorX(rt, offScreenX);
                            MoveCharacterTo(assignedPos, targetX);
                        }
                        else
                        {
                            SetCharacterAnchorX(rt, targetX);
                        }'''

replacement = '''                        bool isFirst = _activeSpeakerPositions.Count == 1;
                        if (node.slideIn || !isFirst)
                        {
                            // Start from off-screen (left or right depending on target position)
                            float offScreenX = (targetX < 0.5f) ? -0.5f : (targetX > 0.5f ? 1.5f : -0.5f);
                            SetCharacterAnchorX(rt, offScreenX);
                            MoveCharacterTo(assignedPos, targetX);
                        }
                        else
                        {
                            SetCharacterAnchorX(rt, targetX);
                        }'''

target_win = target.replace('\n', '\r\n')
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Reverted slide-in logic (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Reverted slide-in logic (lf)')
else:
    print('Target not found')
