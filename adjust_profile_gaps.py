import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            profileTxt.text =
                $"<color=#B46420>{l_age}:</color> {profile.age}\\n" +
                $"<color=#B46420>{l_role}:</color> {profile.role}\\n" +
                $"<color=#B46420>{l_mbti}:</color> {profile.mbti}\\n\\n" +
                $"<color=#B46420>{l_app}:</color> {profile.appearance}\\n\\n" +
                $"<color=#B46420>{l_pers}:</color> {profile.personality}\\n\\n" +
                $"<color=#B46420>{l_speech}:</color> {profile.speechStyle}\\n\\n" +
                $"<color=#B46420>{l_secret}:</color> {profile.secret}";"""

target_win = target.replace('\n', '\r\n')

replacement = """            string gap = "\\n<size=40%>\\n</size>";
            profileTxt.text =
                $"<color=#B46420>{l_age}:</color> {profile.age}\\n" +
                $"<color=#B46420>{l_role}:</color> {profile.role}\\n" +
                $"<color=#B46420>{l_mbti}:</color> {profile.mbti}" + gap +
                $"<color=#B46420>{l_app}:</color> {profile.appearance}" + gap +
                $"<color=#B46420>{l_pers}:</color> {profile.personality}" + gap +
                $"<color=#B46420>{l_speech}:</color> {profile.speechStyle}" + gap +
                $"<color=#B46420>{l_secret}:</color> {profile.secret}";"""

replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Replaced with gap (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Replaced with gap (lf)')
else:
    print('Target not found')
