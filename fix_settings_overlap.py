import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

update_code = '''        private void Update()
        {
            if (textSpeedSlider != null) {
                RectTransform tsRt = textSpeedSlider.GetComponent<RectTransform>();
                if (tsRt.anchoredPosition.x != 100 || tsRt.anchoredPosition.y != -100) {
                    tsRt.anchoredPosition = new Vector2(100, -100);
                    tsRt.sizeDelta = new Vector2(240, 20);
                }
            }
            if (textSpeedLabel != null) {
                RectTransform tlRt = textSpeedLabel.GetComponent<RectTransform>();
                if (tlRt.anchoredPosition.x != -160 || tlRt.anchoredPosition.y != -100) {
                    tlRt.anchoredPosition = new Vector2(-160, -100);
                    tlRt.sizeDelta = new Vector2(280, 40);
                }
            }
        }'''

if update_code in content:
    content = content.replace(update_code, '')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Removed hacky Update method.")
else:
    print("Could not find Update method to remove.")
