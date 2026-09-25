import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'appearance = "연한 갈색 숏컷 머리. 붉은색 X자 귀걸이. 푸른 눈. 검은 오버사이즈 봄버 재킷. 워커 부츠. 스포티하고 힙한 자세."'

replacement = 'appearance = "어깨 아래까지 내려오는 웨이브 진 갈색 머리에 X자 헤어핀. 파란 눈동자. 검은 홀터넥 이너 위에 소매를 걷어 입은 검은 오버사이즈 카고 재킷. 체크무늬 숏 팬츠에 회색 레이스업 워커. 힙하고 자유분방한 스트릿 스타일."'

if target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Rina appearance')
else:
    print('Target not found')
