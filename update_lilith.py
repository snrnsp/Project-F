import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'appearance = "은발 트윈테일. 고양이 모양 헤드셋. 청록색 눈동자. 항상 태블릿과 해킹용 케이블을 들고 다니는 너드스타일."'

replacement = 'appearance = "안쪽이 청록색인 은백색 투톤 숏컷 보브. 파란 눈동자. 검은 크롭 탑 위에 하얀 집업 후드 재킷을 걸치고, 하얀 드로스트링 숏 팬츠 차림. 허벅지의 하얀 밴드와 접혀 내린 스트라이프 레그워머, 큼직한 하얀 레이스업 부츠가 테크웨어 스타일을 완성한다."'

if target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Lilith appearance')
else:
    print('Target not found')
