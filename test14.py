import os, sys
sys.stdout.reconfigure(encoding='utf-8')
for d in os.listdir('Assets/Resources/Characters/하루카'):
    if os.path.isdir(os.path.join('Assets/Resources/Characters/하루카', d)):
        print('하루카 subfolder:', d)
for d in os.listdir('Assets/Resources/Characters/리나'):
    if os.path.isdir(os.path.join('Assets/Resources/Characters/리나', d)):
        print('리나 subfolder:', d)
