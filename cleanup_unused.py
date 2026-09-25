import sys, os, shutil
sys.stdout.reconfigure(encoding='utf-8')

# 미사용 파일을 _legacy 폴더로 이동
legacy_dir = 'F:/Project-F/Assets/Resources/Data/Dialogues/_legacy'
os.makedirs(legacy_dir, exist_ok=True)

files_to_move = ['ch1_prologue.json', 'ch1_incident.json']
for fname in files_to_move:
    src = f'F:/Project-F/Assets/Resources/Data/Dialogues/{fname}'
    dst = os.path.join(legacy_dir, fname)
    if os.path.exists(src):
        if os.path.exists(dst):
            print(f"  ⏭️ {fname}: 이미 _legacy에 존재")
        else:
            shutil.move(src, dst)
            print(f"  ✅ {fname} → _legacy/ 이동 완료")
    else:
        print(f"  ⏭️ {fname}: 원본 없음 (이미 이동됨?)")

print("\n미사용 파일 정리 완료!")
