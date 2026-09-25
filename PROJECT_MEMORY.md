# 🎃 Project F (OBLIVION) — 프로젝트 기억 저장소

> **이 파일은 프로젝트에 대한 모든 핵심 정보를 담고 있습니다.**
> 변경사항이 발생하면 반드시 이 파일을 업데이트해야 합니다.
> 마지막 업데이트: 2026-09-24 14:05 KST

---

## 📁 프로젝트 기본 정보

| 항목 | 값 |
|------|-----|
| **프로젝트 경로** | `F:\Project-F` |
| **Git 저장소** | `F:\Project-F` (main 브랜치) |
| **Unity 버전** | 6000.3.19f1 |
| **빌드 타겟** | WebGL |
| **네임스페이스** | `HalloweenVN.*` (Core, UI, Dialogue, Investigation, Deduction, Data, Effects) |
| **게임 이름** | OBLIVION (오블리비언) |
| **장르** | 미스터리 비주얼 노벨 + 탐정 추리 |

---

## ⚠️ 치명적 주의사항 (CRITICAL)

### 인코딩 & 파일 작성
- **C# 파일 수정 시**: 반드시 `encoding='utf-8-sig'`로 읽고 쓸 것
- **Python으로 C# 문자열 주입 시**: `\n`은 `\\n`으로, `\"`는 `\\"`로 이중 이스케이프 필수
  - 잘못하면 `CS1010: Newline in constant`, `CS1039: Unterminated string literal` 발생
- **JSON 파일**: `utf-8`로 작성. BOM이 여러 개 겹칠 수 있으므로 읽을 때 `while raw.startswith(b'\xef\xbb\xbf'): raw = raw[3:]`로 제거

### WebGL 빌드 제약
- **시스템 폰트 사용 불가**: `Font.CreateDynamicFontFromOSFont()` 사용 금지
  - Legacy Text는 `Resources.Load<Font>("Fonts/MalgunGothic")`으로 직접 로드
  - TMP Text는 `TMP_FontAsset.CreateFontAsset(rawFont)`로 런타임 생성
- **System.IO.File 사용 불가**: WebGL에서는 파일 시스템 접근 안 됨. `PlayerPrefs` 사용

### HalloweenUIBuilder.cs 수정 시
- 이 파일은 **모든 UI를 코드로 생성**하는 핵심 파일 (프리팹 없음)
- Python 스크립트로 수정할 때 **파일 후반부가 잘려나가는 사고 주의**
  - `find()` 실패 시 `-1` 반환 → 파일 절삭 위험
  - 수정 전 반드시 `git status` 확인, 실패 시 `git checkout`으로 복원 가능

---

## 🏗️ 아키텍처 개요

### 게임 페이즈
```
Lobby → Dialogue → Investigation → Deduction → Result(Dialogue) → Lobby
```

| 페이즈 | 담당 스크립트 | 설명 |
|--------|-------------|------|
| `Lobby` | `LobbyUI.cs` | 타이틀 화면, 새 게임/설정/캐릭터/언어 |
| `Dialogue` | `DialogueManager.cs`, `DialogueUI.cs` | VN 대화, 선택지, 내레이션 |
| `Investigation` | `InvestigationManager.cs`, `InvestigationUI.cs` | 클릭으로 증거 수집 |
| `Deduction` | `DeductionManager.cs`, `DeductionUI.cs` | 증거↔질문 드래그앤드롭 매칭 |
| `Result` | Dialogue 페이즈 재활용 | 추리 결과에 따라 perfect/fail 대사 재생 |

### 다이얼로그 커맨드
| 커맨드 | 동작 |
|--------|------|
| `EFFECT:SHAKE` | 카메라 흔들림 |
| `EFFECT:FLASH` | 화면 백색 플래시 |
| `EFFECT:FLASH_RED` | 화면 적색 플래시 |
| `EFFECT:FADE_TO_BLACK` | 화면 암전 |
| `EFFECT:FADE_FROM_BLACK` | 암전 해제 |
| `CHANGE_PHASE:Investigation` | 수사 페이즈로 전환 |
| `CHANGE_PHASE:Deduction` | 추리 페이즈로 전환 |
| `START_DIALOGUE:id` | 다음 대화 파일로 체이닝 (페이드 트랜지션) |
| `END` | 대화 종료 → 로비 복귀 |

### 다이얼로그 노드 JSON 형식
```json
{
  "id": 0,
  "speaker": "캐릭터명 또는 빈 문자열(나레이터)",
  "text": "대사 내용",
  "characterSpriteLeft": "Characters/카스미/기본",
  "characterSpriteCenter": "",
  "characterSpriteRight": "Characters/세이카/기본",
  "backgroundSprite": "Images/배경명",
  "choices": [{"text": "선택지 텍스트", "nextNodeId": 1}],
  "nextNodeId": 1,
  "command": "",
  "slideIn": false,
  "noFade": false
}
```

---

## 👥 캐릭터 정보

| 이름 | 나이 | 역할 | MBTI | 말투 |
|------|------|------|------|------|
| **세이카** | 25 | 사무소 소장 | ENTJ | 반말, 여유롭고 장난기 있는 품격 있는 톤 |
| **카스미** | 23 | 수석 탐정 | INTJ | 경어체, 건조하고 격식. 흥분하면 반말 섞임 |
| **리나** | 21 | 현장 돌격 | ESTP | 반말, 활기차고 직설적. 감탄사 많음 |
| **리리스** | 20 | 기술/해커 | ISTP | 짧은 반말, 명사형 종결. 기계 얘기할 때만 길어짐 |
| **미나** | ?세 | 오컬트 고문 | INFP | 고풍 어투(~하느니라). 긴장하면 현대어로 복귀 |
| **하루카** | 19 | 접수/행정 | ENFP | 밝은 존댓말+반말 혼합. 물결표(~) 많음 |

### 캐릭터 스프라이트 (Characters/{이름}/{표정})
| 캐릭터 | 사용 가능한 표정 |
|--------|-----------------|
| 카스미 | 기본, 경멸, 공포, 당황2, 미소, 시선회피, 찡그림, 측은, 홍조 |
| 리나 | 기본, 경멸, 공포, 놀람, 당황, 웃음, 찡그림, 측은, 홍조 |
| 미나 | 기본, 경멸, 공포, 놀람, 당황, 미소, 삐짐, 음침, 의아, 홍조 + 검은색 버전/ |
| 세이카 | 기본, 경멸, 공포, 놀람, 당황, 웃음, 음침, 찡그림, 측은, 홍조 |
| 리리스 | 기본, 경멸, 공포, 놀람, 눈 감음, 미소, 웃음, 음침, 입 벌린 미소, 찡그림, 측은, 홍조 |
| 하루카 | 기본, 경멸, 공포, 놀람, 모자 착용, 미소, 삐짐, 웃음, 음침, 측은, 홍조 |

---

## 🗺️ 스토리 현황

### 완성된 스토리 흐름 (제1화까지)
```
[로비] → 새 게임 클릭
  ↓
ch0_origin (51노드) — 세이카의 과거: 로펌 → 이케다 저택 발견 → 네버모어 설립
  ↓ START_DIALOGUE:ch0_gathering
ch0_gathering (67노드) — 멤버 모집: 카스미→리나→리리스→미나→하루카
  ↓ START_DIALOGUE:ch0_opening
ch0_opening (16노드) — 노을시와 네버모어 분위기 소개
  ↓ START_DIALOGUE:ch1_morning
ch1_morning (69노드) — 아침 일상 + "폐쇄된 음악실 피아노 소리" 의뢰 접수
  ↓ START_DIALOGUE:ch1_night
ch1_night (28노드) — 밤 출동, 음악실 진입, 자동 연주 목격
  ↓ CHANGE_PHASE:Investigation
🔍 증거 수집 (3개: 먼지 없는 건반, 빛바랜 프로그램, 음파 분석)
  ↓ (전부 수집 후)
ch1_investigation_talk (18노드) — 증거 분석 토론
  ↓ CHANGE_PHASE:Deduction
🧩 추리 퍼즐 (3개 증거↔질문 매칭)
  ↓
ch1_result_perfect (19노드) — 완벽 추리: "나를 찾아줘" 메시지 → 제1화 완
ch1_result_fail (6노드) — 실패 → 재도전
```

### 제1화 핵심 진실
- 피아니스트는 죽은 게 아니라 노을시의 "현상"에 의해 **존재 자체가 잊혀진 것**
- 5년 주기 실종 사건과 연결되는 첫 번째 결정적 증거
- 잊혀진 존재가 아직 그곳에서 연주하고 있음 (먼지 없는 건반)

### 세계관 핵심
- **노을시 (Sunset City)**: 인구 80만 항구도시. 5년 주기로 설명 불가능한 실종 사건 발생
- **"현상"**: 사람의 존재 자체가 세상에서 지워지는 초자연적 현상 (기록, 기억 모두 소멸)
- **네버모어 오컬트 탐정 사무소**: 이케다 저택에 위치. 365일 할로윈 장식. 경찰이 닫은 파일을 다시 여는 곳

---

## 🎨 UI / 테마 정보

### 로비 화면
- 배경: `Images/lobby_bg`
- 버튼 4개: 새 게임, 캐릭터, Language, 환경 설정 (이어하기 삭제됨)
- 버튼은 언어에 따라 번역됨 (`HalloweenUIBuilder.CreateLobbyUI()` 내 switch문)
- 타이틀: "오블리비언\nOBLIVION"

### 캐릭터 설정집 (ExtraUI)
- 마닐라/크라프트지 폴더 테마
- 이름택 글자 크기: 45, 프로필 이름 크기: 60, 본문 크기: 36
- 텍스트 색상: 검정, 필기체 폰트 사용
- 클릭 관통 방지: Body와 ShadowBox에 빈 Button 컴포넌트 추가됨
- 다국어 번역 완료 (ExtraUI.cs 내 GetLabel 메서드)

### 폰트 시스템
| 용도 | 폰트 파일 | 비고 |
|------|-----------|------|
| 한국어 필기체 | NanumPenScript.ttf | 캐릭터 설정집 기본 |
| 영어 필기체 | Caveat-Regular.ttf | |
| 일본어 필기체 | ZenKurenaido-Regular.ttf | |
| 중국어 간체 필기체 | MaShanZheng-Regular.ttf | |
| 중국어 번체 필기체 | LongCang-Regular.ttf | |
| CJK 기본 (Legacy Text) | MalgunGothic.ttf | WebGL용 시스템 폰트 대체 |
| CJK 기본 (TMP) | MalgunGothic SDF.asset | |

### 다국어 지원
- 지원 언어: 한국어(기본), English, 日本語, 简体中文, 繁體中文
- `GameLanguage` enum: Korean, English, Japanese, ChineseSimplified, ChineseTraditional
- 로비 버튼, 경고 팝업, 캐릭터 설정집 모두 번역 완료
- `SettingsData.Language`로 현재 언어 참조

---

## 📂 데이터 파일 목록

### 대화 파일 (Assets/Resources/Data/Dialogues/)
| 파일명 | 노드 수 | 설명 |
|--------|---------|------|
| ch0_origin.json | 25 | 세이카의 과거 (5년 전~4년 전) |
| ch0_gathering.json | 37 | 6인 멤버 모집 |
| ch0_opening.json | 16 | 노을시/네버모어 소개 |
| ch1_morning.json | 69 | 1화 아침 일상 + 의뢰 접수 |
| ch1_night.json | 28 | 1화 밤 출동 + 피아노 장면 |
| ch1_prologue.json | 13 | 1화 축약 프롤로그 (미사용) |
| ch1_incident.json | 7 | 1화 현장 도착 (미사용, ch1_night로 대체) |
| ch1_investigation_talk.json | 18 | 1화 증거 분석 토론 |
| ch1_result_perfect.json | 19 | 1화 완벽 추리 결과 |
| ch1_result_fail.json | 6 | 1화 실패 → 재도전 |
| test_* | 각 2-5 | 테스트용 (게임에서 미사용) |
| _legacy/* | 각 5-8 | 구버전 (미사용) |

### 증거 파일 (Assets/Resources/Data/Evidence/)
| 파일명 | 증거 수 | 설명 |
|--------|---------|------|
| ch1_evidence.json | 3 | 1화: 먼지 없는 건반, 빛바랜 프로그램, 음파 분석 |
| test_evidence_db.json | 3 | 테스트용 |

### 사건 파일 (Assets/Resources/Data/Cases/)
| 파일명 | 질문 수 | 설명 |
|--------|---------|------|
| ch1_case.json | 3 | 1화: 잊혀진 피아니스트 |
| test_case.json | 3 | 테스트용 |

### 배경 이미지 (Assets/Resources/Images/)
| 파일명 | 용도 |
|--------|------|
| lobby_bg.jpg | 로비 배경 (저택 외관) |
| city_night.jpg | 노을시 야경 |
| mansion_interior.jpg | 저택/음악실 내부 |
| mansion_interior_morning.jpg | 저택 내부 (아침) |
| bg_flashback.png | 회상 씬 배경 |

---

## 🔧 핵심 스크립트 구조

```
Assets/Scripts/
├── Core/
│   ├── GameBootstrap.cs      — AutoSetup, DontDestroyOnLoad
│   ├── GameManager.cs        — 싱글톤, 페이즈 관리
│   ├── GamePhase.cs          — enum (Lobby/Dialogue/Investigation/Deduction/Result)
│   ├── SaveData.cs           — PlayerPrefs 기반 세이브
│   └── SettingsData.cs       — 설정값 (텍스트속도/볼륨/언어 등)
├── Data/
│   ├── CaseData.cs           — CaseContainer, CaseQuestion
│   ├── DataLoader.cs         — Resources.Load JSON 파서
│   ├── DialogueData.cs       — DialogueContainer, DialogueNode, DialogueChoice
│   └── EvidenceData.cs       — EvidenceDatabase, EvidenceInfo
├── Dialogue/
│   └── DialogueManager.cs    — 대화 진행/커맨드 처리/선택지/체이닝
├── Deduction/
│   └── DeductionManager.cs   — 추리 퍼즐 로직/채점
├── Investigation/
│   ├── InvestigationManager.cs — 수사 페이즈 관리
│   ├── InvestigationObject.cs  — 클릭 가능 증거 오브젝트
│   └── EvidenceInventory.cs    — 증거 인벤토리 싱글톤
├── Effects/
│   └── ScreenEffects.cs      — 화면 효과 (Shake/Flash/Fade)
└── UI/
    ├── Theme/
    │   ├── HalloweenUIBuilder.cs — 모든 UI를 코드로 생성 (핵심 파일)
    │   ├── HalloweenTheme.cs     — 색상/스타일 상수
    │   ├── UIHelper.cs           — UI 생성 유틸리티
    │   ├── ScreenTransition.cs   — 화면 전환 페이드
    │   ├── PanelAnimator.cs      — 패널 애니메이션
    │   └── SpookyTextEffect.cs   — 텍스트 효과
    ├── LobbyUI.cs            — 로비 화면
    ├── DialogueUI.cs         — 대화 UI (3슬롯 캐릭터 스테이징)
    ├── ExtraUI.cs            — 캐릭터 설정집
    ├── SettingsUI.cs         — 설정 화면
    ├── LanguageUI.cs         — 언어 선택
    ├── BacklogUI.cs          — 백로그
    ├── InvestigationUI.cs    — 수사 UI
    ├── DeductionUI.cs        — 추리 UI
    ├── EvidenceDragItem.cs   — 증거 드래그 아이템
    ├── EvidenceSlot.cs       — 증거 슬롯
    └── GlobalUIManager.cs    — 글로벌 UI 관리
```

---

## 📝 변경 이력

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-09-25 | 백로그(대화기록) 시스템 전면 수정: (1) OnPhaseChanged에서 backlogModalRoot 비활성화 제거(이벤트 구독 끊김 방지), (2) BacklogUI.cs 재작성: Start() 구독+Update() lazy fallback+OnDestroy()에서만 정리+빈 기록 안내 메시지+Lobby 복귀시 기록 초기화 |
| 2026-09-25 | 대화 로그 전수 감사(237노드): 장문 내레이션 줄바꿈 20건, 장문 대사 분할/줄바꿈 5건, 카스미 말투 수정 1건(인정할 수밖에->인정할 수밖에 없습니다), 미나 말투 급변은 의도된 연출로 유지. 총 27건 수정. |
| 2026-09-25 | 프롤로그 텍스트 깨짐 수정: ch0_origin.json 노드 5의 깨지는 글자(랐)를 우회하여 문장을 수정하고 줄바꿈 추가 (잘랐다 -> 끊었다) |
| 2026-09-25 | UI 디자인 전수 감사 및 수정: (1-2) 복사-붙여넣기 버그 수정(수사패널/백로그 제목이 언어설정으로 표시), (3) ResultPanel에 계속 버튼 추가(게임 멈춤 방지), (4) OnPhaseChanged에서 모달 오버레이 자동 닫기, (5) 색상 대비 개선(SlotEmpty/SlotFilled/SlotHighlight 밝기 상향), (6) 로비 슬라이드 -1920 하드코딩을 동적 캔버스 폭으로 변경 |
| 2026-09-25 | 추리 디자인 전수 수정 7건: (1) EvidenceDragItem/EvidenceSlot에 증거 이름 텍스트 추가, UIBuilder 프리팹 재구성(90x90 grid -> 300x50 single-column list), (2) 결과 텍스트 영어->한국어, (3) ch1_night에 발자국/온도 복선 3노드 추가, (4) 함정증거 공개 노드를 애매한 표현으로 변경, (5) 질문 Q4/Q5 표현 차별화, (6) ch1_result_fail 재작성(구체적 피드백+힌트) |
| 2026-09-25 | 추리 난이도 대폭 상향: 증거 3->7개(핵심5+함정2), 질문 3->5개, 경우의수 6->2520. EvidenceData.cs에 required 필드 추가, InvestigationManager.cs에 자동 로드 로직 추가. ch1_evidence/case/investigation_talk/result_perfect.json 모두 업데이트 |
| 2026-09-25 | 프롤로그 압축: ch0_origin(51->25노드), ch0_gathering(67->37노드). 총 118->62노드. 핵심 스토리 비트(5년 주기, 저택 메시지, 각 캐릭터 합류 계기, 시스템 밖 연설)는 모두 보존. 원본은 _legacy에 백업 |
| 2026-09-25 | 스토리 종합 리뷰: (1) ch1_result_perfect/ch1_investigation_talk의 미존재 스프라이트 5건 수정(진지->찡그림, 슬픔->측은, 미소->웃음), (2) worldbuilding.md 타임라인을 ch0_gathering 기준(3개월 내 전원 합류)으로 통일, (3) 미사용 파일(ch1_prologue, ch1_incident) _legacy 이동 |
| 2026-09-25 | 독백(화면 가림) 씬에서 대화 씬으로 넘어갈 때, 캐릭터가 0.2초간 밝게 번쩍였다가 어두워지는 하이라이트 깜빡임 현상 수정 (즉시 어두워지도록 예외 처리) |
| 2026-09-25 | 대화창에서 엔터/스페이스바 입력 시 유니티 UI 이벤트 시스템과 Input System이 중복(더블 클릭)으로 이벤트를 발생시켜 타이핑 애니메이션이 즉시 스킵되던 버그 수정 (0.05초 쿨타임 적용) |
| 2026-09-24 | DialogueUI.cs 코루틴 처리 로직 변경 중 발생한 컴파일 에러(Cannot implicitly convert type void to Coroutine) 수정 |
| 2026-09-24 | 같은 자리에서 이전 캐릭터가 퇴장(FadeOut)함과 동시에 새 캐릭터가 등장(FadeIn)할 때, 퇴장 코루틴이 뒤늦게 이미지를 비활성화시켜 새 캐릭터(리리스 등)가 안 보이게 되는 코루틴 충돌 버그 수정 |
| 2026-09-24 | 대화 진행 중 캐릭터 위치 계산 로직 불일치(0.25 vs 0.34 등)로 인해 특정 대사에서 캐릭터가 우측으로 밀리던 버그 수정 |
| 2026-09-24 | 중앙 캐릭터 슬라이드 인 방향 지정용 slideFromRight 속성 추가 및 리나 첫 등장 씬(ch0_gathering.json)에만 제한적용 (다른 씬 영향 제거) |
| 2026-09-24 | 대화창 첫 캐릭터 등장 시 페이드 효과가 없을(noFade) 경우 화면 오른쪽에서 슬라이드 인(Slide In) 하도록 애니메이션 로직 복구 |
| 2026-09-24 | 미나 캐릭터 설정집 나이 정보 업데이트 (1,000살 -> 1,000살(?)) |
| 2026-09-24 | 하루카 캐릭터 설정집 나이 정보 업데이트 (19세 -> 19세(최연소)) |
| 2026-09-24 | 캐릭터 설정집 본문 텍스트 크기 축소 (이름: 60->55, 본문: 36->32) |
| 2026-09-24 | 하루카 캐릭터 설정집 외모 정보 실제 일러스트 기반으로 전면 수정 (연갈색->회보라색 머리+꽃 핀, 호박색 눈->연보라 눈, 블라우스->캐미솔 원피스+핑크 재킷+프릴 롱스커트+샌들) |
| 2026-09-24 | 리리스 캐릭터 설정집 외모 정보 실제 일러스트 기반으로 전면 수정 (트윈테일->투톤 숏컷 보브, 헤드셋 삭제, 테크웨어 스타일 상세 묘사) |
| 2026-09-24 | 리나 캐릭터 설정집 외모 정보 실제 일러스트 기반으로 전면 수정 (숏컷->웨이브 중간 머리, 귀걸이->헤어핀, 봄버 재킷->카고 재킷+홀터넥+체크 숏팬츠+회색 워커) |
| 2026-09-24 | 카스미 캐릭터 설정집 외모 정보 실제 일러스트 기반으로 전면 수정 (금안->청록색 눈, 밤색 셔츠->하얀 셔츠, 하네스->하이웨스트 슬랙스+목걸이) |
| 2026-09-24 | 세이카 캐릭터 설정집 외모 정보 실제 일러스트 기반으로 전면 수정 (단발->긴 머리, 귀걸이->헤어핀, 트렌치코트->롱 스커트+재킷+숄더백) |
| 2026-09-24 | 미나 캐릭터 설정집 외모 정보 재수정 (실제 일러스트 기반 분석: 해진 순백의 드레스, 한쪽 눈을 가린 머리, 유령 같은 분위기 등 묘사 추가) |
| 2026-09-24 | 미나 캐릭터 설정집 외모 정보 수정 (하얀 은발/검은 드레스 -> 하늘색 머리/하얀색 옷) |
| 2026-09-24 | 설정집(ExtraUI)에서 스프라이트 로드 시 Resources.LoadAll Fallback 로직 추가 (리리스 등 다중 스프라이트 이미지 미출력 버그 수정) |
| 2026-09-24 | 대화창 텍스트 출력 중 줄내림(\\n) 발생 시 0.7초 대기 후 다음 문장 출력되도록 수정 (연출 강화) |
| 2026-09-24 | 캐릭터 설정집 본문 텍스트 단락 간 여백 대폭 축소 (TextMeshPro size 태그 활용) |
| 2026-09-24 | 캐릭터 설정집 폴더 이름택(Tab) 폰트 크기 미세 축소 (50/40 -> 45/35) |
| 2026-09-24 | 캐릭터 설정집(폴더 UI) 전체 크기 축소 및 위치 상향 조정 (가로폭 감소, 세로폭 감소, 상단 여백 감소, 하단 여백 증가) |
| 2026-09-24 | 캐릭터 설정집 폴더 이름택(Tab) 위치 아래로 미세 이동 및 폰트 크기 추가 축소 (50/40) |
| 2026-09-24 | 환경 설정 텍스트 속도 바 조절 시, 미리보기 텍스트가 처음부터 다시 재생되지 않고 출력되는 도중에 실시간으로 속도만 바뀌도록 수정 |
| 2026-09-24 | 텍스트 속도 최소/최대값 상향 조정 (가장 느릴 때 0.05초/글자, 가장 빠를 때 0.005초/글자) |
| 2026-09-24 | 환경 설정 창 진입 시 텍스트 속도가 영구적으로 느려지는 버그 수정 (Slider 범위 0~1로 정규화) |
| 2026-09-24 | 수치바 테두리가 보이지 않는 문제 해결 (Outline 컴포넌트 대신 별도의 Solid 검정색 백그라운드 객체를 생성하여 뒤에 배치) |
| 2026-09-24 | 환경 설정 수치바 배경색을 밝은 보라색으로, 테두리를 완전한 검정색으로 수정 (시인성 향상) |
| 2026-09-24 | 캐릭터 등장 시 슬라이드 애니메이션 속도 상향 (0.5s -> 0.25s) |
| 2026-09-24 | 환경 설정 수치바(Slider) 테두리 색상 및 두께 변경 (주황색 -> 다크 퍼플, 2px -> 4px) |
| 2026-09-24 | 환경 설정 수치바(Slider)에 패널과 동일한 색상의 테두리(Outline) 추가 |
| 2026-09-24 | LobbyUI.UpdateLanguage에서 삭제된 continueText 참조 에러 (NullReferenceException) 해결 |
| 2026-09-24 | 캐릭터 설정집 폴더 이름택 폰트 크기 미세 축소 (65/55 -> 55/45) |
| 2026-09-24 | ExtraUI.cs 내 폴더 탭 폰트 동적 리사이징 로직 수정 (20/16 -> 65/55) |
| 2026-09-24 | 캐릭터 설정집 폴더 이름택(Tab) 폰트 크기 확대 (45 -> 65) |
| 2026-09-24 | 설정 창 상하 테두리 두께 보강 (Outline.effectDistance Y값 증가) |
| 2026-09-24 | 설정 창 텍스트 라벨 위치 미세 하향 조정 (+15f -> +5f) |
| 2026-09-24 | 설정 창 레이아웃 세부 조정 (텍스트 속도, BGM, SFX 라벨 위치 상향) |
| 2026-09-24 | HalloweenUIBuilder.cs 내 미사용 변수(t_continue) 제거 (CS0219 경고 해결) |
| 2026-09-24 | SettingsUI 내 데이터 삭제 버튼 제거 및 닫기 버튼 중앙 정렬 |
| 2026-09-24 | Legacy Text 폰트를 시스템 폰트 → Resources/Fonts/MalgunGothic으로 변경 (WebGL 호환) |
| 2026-09-24 | 로비 버튼 다국어 번역 추가 (HalloweenUIBuilder.cs) |
| 2026-09-24 | 캐릭터 설정집 클릭 관통 방지 (Body/ShadowBox에 빈 Button 추가) |
| 2026-09-24 | 이어하기 버튼 삭제 (로비 4버튼 체제) |
| 2026-09-24 | ch1_morning.json: END → START_DIALOGUE:ch1_night 연결 |
| 2026-09-24 | ch1_night.json 생성 (28노드, 밤 출동 장면) |
| 2026-09-24 | ch1_investigation_talk.json 생성 (18노드, 증거 분석 토론) |
| 2026-09-24 | ch1_result_perfect.json 생성 (19노드, 완벽 추리 결과) |
| 2026-09-24 | ch1_result_fail.json 생성 (6노드, 실패 → 재도전) |
| 2026-09-24 | ExtraUI.cs 문자열 리터럴 이스케이프 오류 수정 |
| 2026-09-24 | SettingsUI.cs FindObjectOfType → FindFirstObjectByType 경고 수정 |

---

## 📌 향후 작업 메모

- [ ] Investigation 페이즈에 실제 클릭 가능한 오브젝트 배치 (현재 InvestigationObject가 씬에 없음)
- [ ] 캐릭터 스프라이트가 실제로 표시되는지 WebGL 빌드에서 확인
- [ ] ch1_prologue.json, ch1_incident.json은 현재 미사용 (ch1_night가 대체)
- [ ] 제2화 이후 스토리 개발
- [ ] 데이터 삭제 경고 팝업 기능 (SettingsUI 내)
- [ ] BGM/SFX 오디오 파일 추가
