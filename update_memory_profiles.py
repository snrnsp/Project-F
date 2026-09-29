import sys
from datetime import datetime

path = 'F:/Project-F/PROJECT_MEMORY.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

now = datetime.now().strftime('%Y-%m-%d')
log_entry = f'| {now} | 영어 번역 시 누락되었던 캐릭터 프로필 원문 디테일(하루카의 최연소, 리리스의 기계 이름 짓기, 미나의 마늘 애호가 등) 전면 복구 및 재번역 적용 |\n'

if '|------|-----------|\n' in content:
    content = content.replace('|------|-----------|\n', '|------|-----------|\n' + log_entry)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
