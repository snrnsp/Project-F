import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'appearance = "아름다운 하늘색 머리. 깔끔하고 단정한 하얀색 옷. 나이를 가늠할 수 없는 묘한 분위기."'
target_win = target.replace('\n', '\r\n')

replacement = 'appearance = "길게 늘어뜨린 하늘색 머리카락과 서늘한 푸른 눈동자. 끝단이 해진 유령 같은 순백의 드레스를 입고 있다. 한쪽 눈을 가린 앞머리와 머리 위로 솟은 장식이 특징적이며, 둥둥 떠다니는 듯한 신비롭고 기묘한 분위기를 풍긴다."'
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Mina appearance with deep analysis (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Mina appearance with deep analysis (lf)')
else:
    print('Target not found')
