import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'rb') as f:
    text = f.read().decode('utf-8')

text = text.replace(
    'private void OnNewGameClicked()\n        {\n',
    'private void OnNewGameClicked()\n        {\n            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);\n'
)
text = text.replace(
    'private void OnNewGameClicked()\r\n        {\r\n',
    'private void OnNewGameClicked()\r\n        {\r\n            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);\r\n'
)

text = text.replace(
    'private void OnContinueClicked()\n        {\n',
    'private void OnContinueClicked()\n        {\n            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);\n'
)
text = text.replace(
    'private void OnContinueClicked()\r\n        {\r\n',
    'private void OnContinueClicked()\r\n        {\r\n            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);\r\n'
)

with open(path, 'wb') as f:
    f.write(codecs.BOM_UTF8 + text.encode('utf-8'))

print("Updated LobbyUI.cs successfully")
