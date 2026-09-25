import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'appearance = "부드러운 연갈색 긴 생머리. 눈물점이 있는 호박색 눈. 프릴이 달린 단정한 블라우스와 치마. 다정하고 차분한 인상."'

replacement = 'appearance = "허리까지 흘러내리는 짙은 회보라색 긴 머리에 하얀 꽃 머리핀. 부드러운 연보라빛 눈동자. 하얀 캐미솔 원피스 위에 연핑크 크롭 데님 재킷을 걸치고, 허리에 리본이 묶인 프릴 롱 스커트에 하얀 스트랩 샌들. 다정하고 청초한 인상."'

if target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Haruka appearance')
else:
    print('Target not found')
