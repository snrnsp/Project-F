import codecs

path = 'F:/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

bad_str = """            profileTxt.text =
                $"<color=#B46420>{l_age}:</color> {profile.age}
" +
                $"<color=#B46420>{l_role}:</color> {profile.role}
" +
                $"<color=#B46420>{l_mbti}:</color> {profile.mbti}

" +
                $"<color=#B46420>{l_app}:</color> {profile.appearance}

" +
                $"<color=#B46420>{l_pers}:</color> {profile.personality}

" +
                $"<color=#B46420>{l_speech}:</color> {profile.speechStyle}

" +
                $"<color=#B46420>{l_secret}:</color> {profile.secret}";"""

good_str = """            profileTxt.text =
                $"<color=#B46420>{l_age}:</color> {profile.age}\\n" +
                $"<color=#B46420>{l_role}:</color> {profile.role}\\n" +
                $"<color=#B46420>{l_mbti}:</color> {profile.mbti}\\n\\n" +
                $"<color=#B46420>{l_app}:</color> {profile.appearance}\\n\\n" +
                $"<color=#B46420>{l_pers}:</color> {profile.personality}\\n\\n" +
                $"<color=#B46420>{l_speech}:</color> {profile.speechStyle}\\n\\n" +
                $"<color=#B46420>{l_secret}:</color> {profile.secret}";"""

# Handle Windows line endings
bad_str = bad_str.replace('\n', '\r\n')

if bad_str in text:
    text = text.replace(bad_str, good_str)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Fixed C# string literal newlines!")
else:
    # try without \r
    bad_str = bad_str.replace('\r\n', '\n')
    if bad_str in text:
        text = text.replace(bad_str, good_str)
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(text)
        print("Fixed C# string literal newlines (LF mode)!")
    else:
        print("Could not find the target string.")
