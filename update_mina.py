import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'appearance = "하얀 은발. 붉은 눈. 고풍스러운 검은 드레스와 붉은 장미 코르사주. 뱀파이어를 연상시키는 고딕 룩. 나이를 가늠할 수 없는 묘한 분위기."'
target_win = target.replace('\n', '\r\n')

replacement = 'appearance = "아름다운 하늘색 머리. 깔끔하고 단정한 하얀색 옷. 나이를 가늠할 수 없는 묘한 분위기."'
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Mina appearance (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Mina appearance (lf)')
else:
    print('Target not found')
