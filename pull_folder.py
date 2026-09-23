import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target1 = '''        private int currentIndex = 0;

        private void Awake()'''

replacement1 = '''        private int currentIndex = 0;
        
        public List<Vector2> defaultOffsetMins = new List<Vector2>();
        public List<Vector2> defaultOffsetMaxs = new List<Vector2>();

        private void Awake()'''

target2 = '''        public void RegisterFolder(GameObject folder, Image bodyImg, Image tabImg, TextMeshProUGUI tabText)
        {
            folderObjects.Add(folder);
            folderBodyImages.Add(bodyImg);
            folderTabImages.Add(tabImg);
            folderTabTexts.Add(tabText);
        }'''

replacement2 = '''        public void RegisterFolder(GameObject folder, Image bodyImg, Image tabImg, TextMeshProUGUI tabText)
        {
            folderObjects.Add(folder);
            folderBodyImages.Add(bodyImg);
            folderTabImages.Add(tabImg);
            folderTabTexts.Add(tabText);
            
            RectTransform rt = folder.GetComponent<RectTransform>();
            defaultOffsetMins.Add(rt.offsetMin);
            defaultOffsetMaxs.Add(rt.offsetMax);
        }'''

target3 = '''                bool isSelected = (i == index);
                GameObject folder = folderObjects[i];

                if (isSelected)
                {
                    // Bring selected folder to front
                    folder.transform.SetAsLastSibling();'''

replacement3 = '''                bool isSelected = (i == index);
                GameObject folder = folderObjects[i];
                RectTransform rt = folder.GetComponent<RectTransform>();

                if (isSelected)
                {
                    // Bring selected folder to front
                    folder.transform.SetAsLastSibling();
                    
                    // Move to center/active position
                    rt.offsetMin = new Vector2(150, 30);
                    rt.offsetMax = new Vector2(-150, -200);'''

target4 = '''                else
                {
                    // Unselected: darker tab color, body hidden behind selected
                    if (i < folderTabImages.Count && folderTabImages[i] != null)'''

replacement4 = '''                else
                {
                    // Unselected: push back to the background staircase stack
                    if (defaultOffsetMins.Count > i) {
                        rt.offsetMin = defaultOffsetMins[i];
                        rt.offsetMax = defaultOffsetMaxs[i];
                    }

                    // Unselected: darker tab color, body hidden behind selected
                    if (i < folderTabImages.Count && folderTabImages[i] != null)'''


text = text.replace(target1, replacement1)
text = text.replace(target2, replacement2)
text = text.replace(target3, replacement3)
text = text.replace(target4, replacement4)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)
print('Updated ExtraUI.cs to pull the selected folder to the center active position!')
