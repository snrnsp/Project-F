import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')
with codecs.open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'private System.Collections.IEnumerator PlaySplashSequence()' in line:
        for j in range(i, i+30):
            print(lines[j].rstrip('\r\n'))
        break
