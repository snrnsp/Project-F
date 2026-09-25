import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'appearance = "짙은 보라~남색 단발머리에 하트 모양 골드 귀걸이. 맑은 푸른 눈. 검은 트렌치코트 안쪽의 버건디 컬러가 세련되고 도시적인 분위기."'

replacement = 'appearance = "허리 아래까지 흘러내리는 짙은 남색 긴 머리카락에 금색 헤어핀. 맑고 차가운 파란 눈동자. 검은색 롱 스커트에 차콜 그레이 재킷, 검은 숄더백을 걸친 세련되고 도시적인 분위기."'

if target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Seika appearance')
else:
    print('Target not found')
