import sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

fixes = 0

# 1. Store settings modal root reference
old = 'GameObject settingsRoot = UIHelper.CreateUIObject("SettingsRoot", mainCanvas.transform);'
new = 'settingsModalRoot = UIHelper.CreateUIObject("SettingsRoot", mainCanvas.transform);\n            GameObject settingsRoot = settingsModalRoot;'
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("✅ Fix 1: settingsModalRoot 저장")

# 2. Store language modal root reference
old = 'GameObject langRoot = UIHelper.CreateUIObject("LanguageRoot", mainCanvas.transform);'
new = 'languageModalRoot = UIHelper.CreateUIObject("LanguageRoot", mainCanvas.transform);\n            GameObject langRoot = languageModalRoot;'
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("✅ Fix 2: languageModalRoot 저장")

# 3. Store backlog modal root reference
old = 'GameObject backlogRoot = UIHelper.CreateUIObject("BacklogRoot", mainCanvas.transform);'
new = 'backlogModalRoot = UIHelper.CreateUIObject("BacklogRoot", mainCanvas.transform);\n            GameObject backlogRoot = backlogModalRoot;'
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("✅ Fix 3: backlogModalRoot 저장")

# 4. Store extra modal root reference
old = 'GameObject extraRoot = UIHelper.CreateUIObject("ExtraPanel", mainCanvas.transform);'
new = 'extraModalRoot = UIHelper.CreateUIObject("ExtraPanel", mainCanvas.transform);\n            GameObject extraRoot = extraModalRoot;'
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("✅ Fix 4: extraModalRoot 저장")

# 5. Fix OnPhaseChanged to close all modal overlays
old_phase = """        private void OnPhaseChanged(GamePhase phase)
        {
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(phase == GamePhase.Lobby);
            if (dialoguePanelRoot) dialoguePanelRoot.SetActive(phase == GamePhase.Dialogue || phase == GamePhase.Result);
            if (investigationPanelRoot) investigationPanelRoot.SetActive(phase == GamePhase.Investigation);
            if (deductionPanelRoot) deductionPanelRoot.SetActive(phase == GamePhase.Deduction);
        }"""
new_phase = """        private void OnPhaseChanged(GamePhase phase)
        {
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(phase == GamePhase.Lobby);
            if (dialoguePanelRoot) dialoguePanelRoot.SetActive(phase == GamePhase.Dialogue || phase == GamePhase.Result);
            if (investigationPanelRoot) investigationPanelRoot.SetActive(phase == GamePhase.Investigation);
            if (deductionPanelRoot) deductionPanelRoot.SetActive(phase == GamePhase.Deduction);

            // Close all modal overlays on phase change to prevent them from blocking input
            if (settingsModalRoot) settingsModalRoot.SetActive(false);
            if (languageModalRoot) languageModalRoot.SetActive(false);
            if (backlogModalRoot) backlogModalRoot.SetActive(false);
            if (extraModalRoot) extraModalRoot.SetActive(false);
        }"""
if old_phase in content:
    content = content.replace(old_phase, new_phase)
    fixes += 1
    print("✅ Fix 5: OnPhaseChanged에서 모달 오버레이 자동 닫기")

# 6. Fix lobby slide to use dynamic width instead of hardcoded -1920
# This is in LobbyUI.cs, not here
    
with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)

print(f"\n총 {fixes}건 수정 완료!")
