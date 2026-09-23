import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add globalMgrRef
text = text.replace('private SettingsUI settingsUiRef;', 'private SettingsUI settingsUiRef;\n        private GlobalUIManager globalMgrRef;')

# In CreateGlobalUI, save globalMgrRef and remove the old settingsUI init
target_global = '''            var globalMgr = globalRoot.AddComponent<GlobalUIManager>();
            
            // Find settings root
            var settingsUI = settingsUiRef;
            if (settingsUI != null) globalMgr.Initialize(settingsUI.gameObject);'''

replacement_global = '''            var globalMgr = globalRoot.AddComponent<GlobalUIManager>();
            globalMgrRef = globalMgr;'''

text = text.replace(target_global, replacement_global)

# In CreateSettingsUI, initialize globalMgrRef
target_settings = '''            settingsUiRef = settingsUi;'''
replacement_settings = '''            settingsUiRef = settingsUi;
            if (globalMgrRef != null) globalMgrRef.Initialize(settingsRoot);'''

text = text.replace(target_settings, replacement_settings)

# Move CreateGlobalUI in Awake
target_awake = '''            CreateLobbyUI();
            CreateSettingsUI();
            CreateLanguageUI();
            CreateBacklogUI();
            CreateExtraUI();
            CreateGlobalUI();'''

replacement_awake = '''            CreateLobbyUI();
            CreateGlobalUI();
            CreateSettingsUI();
            CreateLanguageUI();
            CreateBacklogUI();
            CreateExtraUI();'''

text = text.replace(target_awake, replacement_awake)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Moved GlobalUI below overlay windows')
