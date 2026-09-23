import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target_kr = 'if (closeButtonText != null) closeButtonText.text = "\\uB2EB\\uAE30";'
rep_kr = '''if (closeButtonText != null) closeButtonText.text = "\\uB2EB\\uAE30";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "데이터 초기화";'''

target_jp = 'if (closeButtonText != null) closeButtonText.text = "\\u9589\\u3058\\u308B";'
rep_jp = '''if (closeButtonText != null) closeButtonText.text = "\\u9589\\u3058\\u308B";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "データ初期化";'''

target_sc = 'if (closeButtonText != null) closeButtonText.text = "\\u5173\\u95ED";'
rep_sc = '''if (closeButtonText != null) closeButtonText.text = "\\u5173\\u95ED";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "清除数据";'''

target_tc = 'if (closeButtonText != null) closeButtonText.text = "\\u95DC\\u958D";'
rep_tc = '''if (closeButtonText != null) closeButtonText.text = "\\u95DC\\u958D";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "清除數據";'''

if target_kr in text: text = text.replace(target_kr, rep_kr)
if target_jp in text: text = text.replace(target_jp, rep_jp)
if target_sc in text: text = text.replace(target_sc, rep_sc)
if target_tc in text: text = text.replace(target_tc, rep_tc)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated translations for delete button in SettingsUI.cs')
