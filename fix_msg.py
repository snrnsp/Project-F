import sys

old_str = "현재 오블리비언은 '<color=#80C0FF>프리 알파</color>(소프트웨어나 게임 개발 과정에서 정식 알파 테스트 이전의 초기 제작 및 설계 단계)'에 있습니다!"
new_str = "현재 오블리비언은 '<color=#80C0FF>프리 알파</color>'\\n(소프트웨어나 게임 개발 과정에서 정식 알파 테스트 이전의 초기 제작 및 설계 단계)에 있습니다!"

for path in ['F:/Project-F/Assets/Scripts/UI/LobbyUI.cs', 'F:/Project-F/Assets/Resources/Localization/game_text.csv']:
    with open(path, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    
    if old_str in text:
        text = text.replace(old_str, new_str)
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(text)
        print(f'Replaced in {path}')
    else:
        print(f'Not found in {path}')
