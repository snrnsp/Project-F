import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('데이터 초기화', '데이터 삭제')
text = text.replace('データ初期化', 'データ削除')
text = text.replace('清除数据', '删除数据')
text = text.replace('清除數據', '刪除數據')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)
