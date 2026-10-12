with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()
    start = text.find('public void ShowNode')
    end = text.find('private void UpdateSpeakerHighlight', start)
    print(text[start:end].encode('ascii', 'backslashreplace').decode('ascii'))
