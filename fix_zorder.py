import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# We need to extract the Header & CloseBtn creation and move it AFTER the folder loop.
# Let's find the Header block.
header_start = text.find('            // ===== Header =====')
shadow_start = text.find('            // ===== Back shadow box')

if header_start != -1 and shadow_start != -1:
    header_block = text[header_start:shadow_start]
    
    # Remove header block from its current position
    text = text[:header_start] + text[shadow_start:]
    
    # Insert header block AFTER the folder loop
    loop_end_str = '            extraUiRef = extraUi;'
    loop_end_idx = text.find(loop_end_str)
    
    if loop_end_idx != -1:
        text = text[:loop_end_idx] + header_block + '\n' + text[loop_end_idx:]
        
        # Now reverse the for loop!
        # Change `for (int ci = 0; ci < folderCount; ci++)`
        # and remove `folder.transform.SetAsFirstSibling();`
        
        text = text.replace('for (int ci = 0; ci < folderCount; ci++)', 'for (int ci = folderCount - 1; ci >= 0; ci--)')
        text = text.replace('                // SetAsFirstSibling ensures that Folder 0 is front-most, Folder 1 is behind 0, etc.\n                folder.transform.SetAsFirstSibling();\n', '')
        
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(text)
        print("Restructured UI creation order: reversed loop and moved header to top!")
    else:
        print("Could not find loop end")
else:
    print("Could not find header or shadow start")
