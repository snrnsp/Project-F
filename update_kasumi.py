import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'appearance = "허리까지 오는 짙은 남보라색 긴머리. 금안. 활동적인 밤색 셔츠와 검은 하네스. 블랙톤. 단정하면서도 날카로운 인상."'

replacement = 'appearance = "발끝까지 흘러내리는 짙은 남보라색 긴 머리카락. 날카로운 청록색 눈동자. 소매를 걷어 올린 하얀 셔츠에 하이웨스트 검은 슬랙스, 검은 부츠. 목에 걸린 검은 목걸이가 포인트인, 단정하면서도 차가운 인상."'

if target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Kasumi appearance')
else:
    print('Target not found')
