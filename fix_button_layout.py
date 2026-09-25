import codecs

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

bad_str = """            float startY = 160f; // Center adjusted (+160 to -160 for 5 buttons)"""
good_str = """            float startY = 120f; // Center adjusted for 4 buttons"""

# Handle Windows newlines
bad_str_win = bad_str.replace('\n', '\r\n')

if bad_str_win in text:
    text = text.replace(bad_str_win, good_str.replace('\n', '\r\n'))
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Fixed button layout spacing (win lf)!")
else:
    if bad_str in text:
        text = text.replace(bad_str, good_str)
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(text)
        print("Fixed button layout spacing (lf)!")
    else:
        print("Could not find the startY line.")
