import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/ScreenTransition.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''        private void HandlePhaseChanged\(GamePhase phase\)\r?\n\s*\{\r?\n\s*if \(autoTransitionOnPhaseChange\)\r?\n\s*\{\r?\n\s*TransitionFade\(\);\r?\n\s*\}'''

replacement = r'''        private void HandlePhaseChanged(GamePhase phase)
        {
            if (autoTransitionOnPhaseChange)
            {
                // Splash screen has its own white fade logic in HalloweenUIBuilder.
                // Do not trigger a black transition fade over it!
                if (phase == GamePhase.Splash) return;
                
                TransitionFade();
            }'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed ScreenTransition HandlePhaseChanged!")
else:
    print("Failed to match ScreenTransition pattern!")
