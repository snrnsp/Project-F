import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix ShadowBox border
target_shadow = 'shadowImg.sprite = UIHelper.CreateRoundedRectSprite(10, 2, new Color32(80, 60, 40, 255), new Color32(60, 45, 25, 255));'
rep_shadow = 'shadowImg.sprite = UIHelper.CreateRoundedRectSprite(10, 4, new Color32(80, 60, 40, 255), new Color32(60, 45, 25, 255));'
text = text.replace(target_shadow, rep_shadow)

# Fix Body border
target_body = 'bodyImg.sprite = UIHelper.CreateRoundedRectSprite(10, 2, Color.white, folderBorder);'
rep_body = 'bodyImg.sprite = UIHelper.CreateRoundedRectSprite(10, 4, Color.white, folderBorder);'
text = text.replace(target_body, rep_body)

# Fix Tab border
target_tab = 'tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, Color.white, folderBorder);'
rep_tab = 'tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 4, Color.white, folderBorder);'
text = text.replace(target_tab, rep_tab)

# Fix TabContainer overlap (from 2px to 4px)
target_overlap = '''                // Move down by 2 pixels so the bottom edge overlaps and hides the Body's top border
                tabContainerRt.anchoredPosition = new Vector2(0, 53);
                tabContainerRt.sizeDelta = new Vector2(-6, 55);'''
rep_overlap = '''                // Move down by 4 pixels to perfectly cover the thicker 4px Body top border
                tabContainerRt.anchoredPosition = new Vector2(0, 51);
                tabContainerRt.sizeDelta = new Vector2(-6, 55);'''
text = text.replace(target_overlap, rep_overlap)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated border thicknesses to 4px')
