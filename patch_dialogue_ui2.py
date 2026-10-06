import re

with open('Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Fix MoveCharacterTo to immediately snap if already there, preventing any weird StartCoroutine delays
old_block2 = '''        private void MoveCharacterTo(CharacterPosition pos, float targetX)
        {
            int idx = (int)pos;
            Image img = GetCharacterImage(pos);
            if (img == null) return;

            if (_moveCoroutines[idx] != null)
            {
                StopCoroutine(_moveCoroutines[idx]);
            }
            _moveCoroutines[idx] = StartCoroutine(SmoothMoveCharacter(img, targetX));
        }'''

new_block2 = '''        private void MoveCharacterTo(CharacterPosition pos, float targetX)
        {
            int idx = (int)pos;
            Image img = GetCharacterImage(pos);
            if (img == null) return;

            if (_moveCoroutines[idx] != null)
            {
                StopCoroutine(_moveCoroutines[idx]);
            }
            
            float startX = (img.rectTransform.anchorMin.x + img.rectTransform.anchorMax.x) / 2f;
            if (Mathf.Abs(startX - targetX) < 0.01f)
            {
                SetCharacterAnchorX(img.rectTransform, targetX);
                return;
            }
            
            _moveCoroutines[idx] = StartCoroutine(SmoothMoveCharacter(img, targetX));
        }'''

content = content.replace(old_block2, new_block2)

with open('Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Patched DialogueUI.cs 2")
