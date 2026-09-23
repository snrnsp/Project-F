import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/Data/DataLoader.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''        public static T LoadFromResources<T>(string path)
        {
            TextAsset textAsset = Resources.Load<TextAsset>(path);
            if (textAsset != null)
            {
                return JsonUtility.FromJson<T>(textAsset.text);
            }'''

replacement = '''        public static T LoadFromResources<T>(string path)
        {
            TextAsset textAsset = Resources.Load<TextAsset>(path);
            if (textAsset != null)
            {
                string json = textAsset.text;
                if (json.Length > 0 && json[0] == '\\uFEFF') json = json.Substring(1);
                return JsonUtility.FromJson<T>(json);
            }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Fixed BOM stripping in DataLoader.cs")
else:
    print("Could not find the target code in DataLoader.cs")
