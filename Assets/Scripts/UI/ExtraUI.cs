using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TMPro;
using HalloweenVN.Core;

namespace HalloweenVN.UI
{
    public class CharacterProfile
    {
        public string id; // language-independent identifier (Korean name), used for layout checks
        public string name;
        public string spritePath;
        public string age;
        public string role;
        public string mbti;
        public string appearance;
        public string personality;
        public string speechStyle;
        public string secret;
    }

    public class ExtraUI : MonoBehaviour
    {
        [SerializeField] private GameObject extraPanel;
        [SerializeField] private Button closeButton;
        [SerializeField] private TMPro.TextMeshProUGUI titleText;
        [SerializeField] private TMPro.TextMeshProUGUI closeBtnText;
        [SerializeField] private GameObject globalSettingsButton;
        [SerializeField] private GameObject lobbySettingsButton;

        // Folder-based structure: each character has its own folder GameObject
        private List<CharacterProfile> profiles = new List<CharacterProfile>();
        private List<GameObject> folderObjects = new List<GameObject>();
        private List<Image> folderBodyImages = new List<Image>();
        private List<Image> folderTabImages = new List<Image>();
        private List<TextMeshProUGUI> folderTabTexts = new List<TextMeshProUGUI>();
        private int currentIndex = 0;
        
        public List<Vector2> defaultOffsetMins = new List<Vector2>();
        public List<Vector2> defaultOffsetMaxs = new List<Vector2>();

        // Folder colors (real manila folder look)
        private static readonly Color32 selectedFolderColor = new Color32(210, 185, 140, 255);
        private static readonly Color32 unselectedTabColor = new Color32(160, 135, 100, 255);
        private static readonly Color32 selectedTabTextColor = new Color32(60, 40, 20, 255);
        private static readonly Color32 unselectedTabTextColor = new Color32(220, 210, 190, 255);

        private void Awake()
        {
            InitializeProfiles();
        }

        private void Start()
        {
            UpdateLanguage();
        }

        private void OnEnable()
        {
            if (closeButton != null)
                closeButton.onClick.AddListener(Hide);
        }

        private void OnDisable()
        {
            if (closeButton != null)
                closeButton.onClick.RemoveListener(Hide);
        }

        private void InitializeProfiles()
    {
        profiles.Clear();
        // All texts come from the localization table (Loc); Korean is the source/default.

        profiles.Add(new CharacterProfile
        {
            id = "세이카",
            name = Loc.Get("speaker.세이카", "세이카"),
            spritePath = "Characters/세이카/기본",
            age = Loc.Get("ui.extra.seika_age", "25세"),
            role = Loc.Get("ui.extra.seika_role", "사무소 소장 / 경영·법무 담당"),
            mbti = "ENTJ",
            appearance = Loc.Get("ui.extra.seika_appearance", "허리 아래까지 흘러내리는 짙은 남색 긴 머리카락에 금색 헤어핀. 맑고 차가운 파란 눈동자. 검은색 롱 스커트에 차콜 그레이 재킷, 검은 숄더백을 걸친 세련되고 도시적인 분위기."),
            personality = Loc.Get("ui.extra.seika_personality", "「네버모어 오컬트 탐정 사무소」의 설립자이자 소장. 카리스마가 있고 결단력이 빠르며, 할로윈과 오컬트에 진심으로 열광한다."),
            speechStyle = Loc.Get("ui.extra.seika_speech", "반말 위주. 호탕하게 웃는 편.\n\"후훗, 보기 좋잖아? 네버모어라는 이름에 딱 맞는 인테리어지.\""),
            secret = Loc.Get("ui.extra.seika_secret", "사무소를 차린 진짜 이유: 과거 자신이 경험한 설명할 수 없는 사건의 진상을 밝히기 위해.")
        });

        profiles.Add(new CharacterProfile
        {
            id = "카스미",
            name = Loc.Get("speaker.카스미", "카스미"),
            spritePath = "Characters/카스미/기본",
            age = Loc.Get("ui.extra.kasumi_age", "23세"),
            role = Loc.Get("ui.extra.kasumi_role", "수석 탐정 / 현장 지휘"),
            mbti = "INTJ",
            appearance = Loc.Get("ui.extra.kasumi_appearance", "은회색 단발머리. 날카로운 호박색 눈동자. 활동하기 편한 슬림핏 트렌치 코트. 단정하고 이성적인 분위기."),
            personality = Loc.Get("ui.extra.kasumi_personality", "철저한 이성주의자. 모든 현상에는 과학적 원인이 있다고 확신한다. 사건을 객관적이고 논리적으로 해결하려 한다."),
            speechStyle = Loc.Get("ui.extra.kasumi_speech", "존댓말 위주. 딱딱하고 사무적.\n\"...전 유령 따위는 믿지 않습니다. 분명 트릭이 있을 겁니다.\""),
            secret = Loc.Get("ui.extra.kasumi_secret", "어릴 적 트라우마로 인해 사실 '귀신'을 극도로 무서워한다. 탐정이 된 이유도 그것.")
        });

        profiles.Add(new CharacterProfile
        {
            id = "리나",
            name = Loc.Get("speaker.리나", "리나"),
            spritePath = "Characters/리나/기본",
            age = Loc.Get("ui.extra.rina_age", "21세"),
            role = Loc.Get("ui.extra.rina_role", "행동 대장 / 무력 담당"),
            mbti = "ESTP",
            appearance = Loc.Get("ui.extra.rina_appearance", "밝은 분홍색 트윈테일. 스포티한 야구 점퍼와 숏팬츠. 활동적이고 톡톡 튀는 스타일."),
            personality = Loc.Get("ui.extra.rina_personality", "생각보다 몸이 먼저 나가는 행동파. 활기차고 용감하지만 지루한 것을 견디지 못한다. 사무소에 가만히 있는 것을 제일 싫어한다."),
            speechStyle = Loc.Get("ui.extra.rina_speech", "반말 위주. 목소리가 크다.\n\"그냥 문 부수고 들어가면 안 돼?!\""),
            secret = Loc.Get("ui.extra.rina_secret", "의외로 요리 실력이 뛰어나다. 단, 시각적으로는 매우 끔찍한 결과물을 만들어낸다.")
        });

        profiles.Add(new CharacterProfile
        {
            id = "리리스",
            name = Loc.Get("speaker.리리스", "리리스"),
            spritePath = "Characters/리리스/기본",
            age = Loc.Get("ui.extra.lilith_age", "20세"),
            role = Loc.Get("ui.extra.lilith_role", "정보원 / 해커 & 발명가"),
            mbti = "ISTP",
            appearance = Loc.Get("ui.extra.lilith_appearance", "헝클어진 보라색 머리. 두꺼운 안경. 오버핏 후드티와 헤드폰. 항상 다크서클이 있다."),
            personality = Loc.Get("ui.extra.lilith_personality", "귀차니스트 천재. 사람보다 기계와 대화하는 것을 더 편하게 생각한다. 기계에 '이름'을 붙여주는 취미가 있다."),
            speechStyle = Loc.Get("ui.extra.lilith_speech", "작은 목소리. 단답형.\n\"...해킹 완료. 3초 걸렸어.\""),
            secret = Loc.Get("ui.extra.lilith_secret", "어떤 사람의 목소리든 완벽히 복제하는 AI를 발명했다. 자신이 대답하기 귀찮을 때 쓴다.")
        });

        profiles.Add(new CharacterProfile
        {
            id = "미나",
            name = Loc.Get("speaker.미나", "미나"),
            spritePath = "Characters/미나/기본",
            age = Loc.Get("ui.extra.mina_age", "1,000세(?)"),
            role = Loc.Get("ui.extra.mina_role", "오컬트 고문 / 자칭 흡혈귀"),
            mbti = "INFJ",
            appearance = Loc.Get("ui.extra.mina_appearance", "창백한 피부에 은발. 고딕 로리타 풍의 드레스. 신비로운 붉은 눈동자."),
            personality = Loc.Get("ui.extra.mina_personality", "스스로를 1000살 먹은 흡혈귀라 칭하는 중2병 소녀. 평소엔 엉뚱하지만 오컬트 지식은 진짜다."),
            speechStyle = Loc.Get("ui.extra.mina_speech", "시대극 말투.\n\"크큭... 어리석은 인간이여. 나의 피가 두려운가?\""),
            secret = Loc.Get("ui.extra.mina_secret", "햇빛 알레르기가 있어서 낮에 밖에 나가지 못할 뿐이다. 사실 마늘은 좋아한다(알리오 올리오 매니아).")
        });

        profiles.Add(new CharacterProfile
        {
            id = "하루카",
            name = Loc.Get("speaker.하루카", "하루카"),
            spritePath = "Characters/하루카/기본",
            age = Loc.Get("ui.extra.haruka_age", "19세(최연소)"),
            role = Loc.Get("ui.extra.haruka_role", "사무소 막내 / 메이드"),
            mbti = "ISFJ",
            appearance = Loc.Get("ui.extra.haruka_appearance", "단정한 흑발 숏컷. 완벽하게 다림질된 메이드복. 상냥한 미소."),
            personality = Loc.Get("ui.extra.haruka_personality", "항상 친절하고 성실하다. 청소와 홍차 내리기에 진심이다."),
            speechStyle = Loc.Get("ui.extra.haruka_speech", "존댓말.\n\"홍차 한 잔 다 드시면, 다음 사건 파일 가져다 드릴게요.\""),
            secret = Loc.Get("ui.extra.haruka_secret", "화가 나면 아무도 말릴 수 없다. 카스미조차 하루카가 화내면 눈치를 본다.")
        });
    }
    public void RegisterFolder(GameObject folder, Image bodyImg, Image tabImg, TextMeshProUGUI tabText)
        {
            folderObjects.Add(folder);
            folderBodyImages.Add(bodyImg);
            folderTabImages.Add(tabImg);
            folderTabTexts.Add(tabText);
            
            RectTransform rt = folder.GetComponent<RectTransform>();
            defaultOffsetMins.Add(rt.offsetMin);
            defaultOffsetMaxs.Add(rt.offsetMax);
        }

        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            
            // Re-initialize language dynamically every time we open the book!
            InitializeProfiles();
            UpdateTabNames();
            UpdateLanguage(); // Ensure font and sizes are synced every time it opens

            if (extraPanel != null)
            {
                extraPanel.SetActive(true);
                SelectCharacter(currentIndex); // Refresh current selection
            }
            if (globalSettingsButton != null) globalSettingsButton.SetActive(false);
            if (lobbySettingsButton != null) lobbySettingsButton.SetActive(false);
        }

        public void Hide()
        {
            if (extraPanel != null)
                extraPanel.SetActive(false);
            if (globalSettingsButton != null) globalSettingsButton.SetActive(true);
            if (lobbySettingsButton != null) lobbySettingsButton.SetActive(true);
        }

                public void UpdateLanguage()
        {
            bool isGothic = !HalloweenVN.Core.SettingsData.UseHandwritingFont;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(HalloweenVN.Core.SettingsData.Language);
            var currentFont = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);

            for (int i = 0; i < folderObjects.Count; i++)
            {
                if (currentFont != null)
                {
                    if (titleText != null) titleText.font = currentFont;
                    if (closeBtnText != null) closeBtnText.font = currentFont;

                    if (i < folderTabTexts.Count && folderTabTexts[i] != null)
                        folderTabTexts[i].font = currentFont;
                        
                    var folderTr = folderObjects[i].transform;
                    var nameTxt = folderTr.Find("Body/Scroll/Viewport/Content/NameText")?.GetComponent<TMPro.TextMeshProUGUI>();
                    var profileTxt = folderTr.Find("Body/Scroll/Viewport/Content/ProfileText")?.GetComponent<TMPro.TextMeshProUGUI>();
                    
                    if (nameTxt != null) nameTxt.font = currentFont;
                    if (profileTxt != null) profileTxt.font = currentFont;
                }
            }

            if (titleText != null) titleText.fontSize = isGothic ? 28 : 36;
            if (closeBtnText != null) closeBtnText.fontSize = isGothic ? 24 : 30;

            // Re-fetch localized profile texts / tab names for the current language
            InitializeProfiles();
            UpdateTabNames();

            SelectCharacter(currentIndex);
        }

        private void UpdateTabNames()
        {
            for (int i = 0; i < folderTabTexts.Count; i++)
            {
                if (i < profiles.Count && folderTabTexts[i] != null)
                {
                    folderTabTexts[i].text = profiles[i].name;
                }
            }
        }

        private void UpdateProfileText(TextMeshProUGUI profileTxt, CharacterProfile profile)
        {
            if (profileTxt == null) return;
            string l_age = Loc.Get("ui.extra.label_age", "나이");
            string l_role = Loc.Get("ui.extra.label_role", "역할");
            string l_mbti = "MBTI";
            string l_app = Loc.Get("ui.extra.label_appearance", "외모");
            string l_pers = Loc.Get("ui.extra.label_personality", "성격");
            string l_speech = Loc.Get("ui.extra.label_speech", "말투");
            string l_secret = Loc.Get("ui.extra.label_secret", "비밀");

            string gap = "\n<size=40%>\n</size>";
            profileTxt.text =
                $"<color=#B46420>{l_age}:</color> {profile.age}\n" +
                $"<color=#B46420>{l_role}:</color> {profile.role}\n" +
                $"<color=#B46420>{l_mbti}:</color> {profile.mbti}" + gap +
                $"<color=#B46420>{l_app}:</color> {profile.appearance}" + gap +
                $"<color=#B46420>{l_pers}:</color> {profile.personality}" + gap +
                $"<color=#B46420>{l_speech}:</color> {profile.speechStyle}" + gap +
                $"<color=#B46420>{l_secret}:</color> {profile.secret}";
        }

        public void SelectCharacter(int index)
        {
            if (index < 0 || index >= profiles.Count) return;
            currentIndex = index;

            // First, correct the Z-order for unselected folders to maintain the stack
            for (int i = 0; i < folderObjects.Count; i++)
            {
                if (i != index)
                {
                    // Insert at index 2 (right after background/shadow).
                    // As we iterate 0->5, later folders push earlier ones forward.
                    // This perfectly restores the 5->0 depth order for the unselected stack!
                    folderObjects[i].transform.SetSiblingIndex(2);
                }
            }
            // Bring selected folder to the front of the folder stack (but behind Header/CloseBtn)
            if (folderObjects.Count > 0)
                folderObjects[index].transform.SetSiblingIndex(2 + folderObjects.Count - 1);

            // Update folder visuals
            for (int i = 0; i < folderObjects.Count; i++)
            {
                bool isSelected = (i == index);
                GameObject folder = folderObjects[i];
                RectTransform rt = folder.GetComponent<RectTransform>();

                if (isSelected)
                {
                    // Move to center/active position
                    rt.offsetMin = new Vector2(250, 80);
                    rt.offsetMax = new Vector2(-250, -210);

                    // Selected folder: bright manila color
                    if (i < folderBodyImages.Count && folderBodyImages[i] != null)
                        folderBodyImages[i].color = selectedFolderColor;
                    if (i < folderTabImages.Count && folderTabImages[i] != null)
                        folderTabImages[i].color = selectedFolderColor;
                    
                    Image seamImg = folder.transform.Find("TabContainer/Seam")?.GetComponent<Image>();
                    if (seamImg != null) seamImg.color = selectedFolderColor;
                    if (i < folderTabTexts.Count && folderTabTexts[i] != null)
                    {
                        bool isGothic = !HalloweenVN.Core.SettingsData.UseHandwritingFont;
                        folderTabTexts[i].color = selectedTabTextColor;
                        folderTabTexts[i].fontSize = isGothic ? 24 : 45;
                        folderTabTexts[i].fontStyle = FontStyles.Bold;
                    }
                }
                else
                {
                    // Unselected: push back to the background staircase stack
                    if (defaultOffsetMins.Count > i) {
                        rt.offsetMin = defaultOffsetMins[i];
                        rt.offsetMax = defaultOffsetMaxs[i];
                    }

                    // Unselected: darker tab color, body hidden behind selected
                    if (i < folderTabImages.Count && folderTabImages[i] != null)
                        folderTabImages[i].color = unselectedTabColor;
                    
                    Image seamImg = folder.transform.Find("TabContainer/Seam")?.GetComponent<Image>();
                    if (seamImg != null) seamImg.color = unselectedTabColor;
                    if (i < folderTabTexts.Count && folderTabTexts[i] != null)
                    {
                        bool isGothic = !HalloweenVN.Core.SettingsData.UseHandwritingFont;
                        folderTabTexts[i].color = unselectedTabTextColor;
                        folderTabTexts[i].fontSize = isGothic ? 18 : 35;
                        folderTabTexts[i].fontStyle = FontStyles.Normal;
                    }
                }
            }

            // Update content of the selected folder
            CharacterProfile profile = profiles[index];

            // Find the portrait and texts inside the selected folder
            Transform folderTr = folderObjects[index].transform;
            Image portrait = folderTr.Find("Body/Portrait")?.GetComponent<Image>();
            TextMeshProUGUI nameTxt = folderTr.Find("Body/Scroll/Viewport/Content/NameText")?.GetComponent<TextMeshProUGUI>();
            TextMeshProUGUI profileTxt = folderTr.Find("Body/Scroll/Viewport/Content/ProfileText")?.GetComponent<TextMeshProUGUI>();

            if (portrait != null)
            {
                Sprite sprite = Resources.Load<Sprite>(profile.spritePath);
                if (sprite == null) {
                    Sprite[] allSprites = Resources.LoadAll<Sprite>(profile.spritePath);
                    if (allSprites != null && allSprites.Length > 0) sprite = allSprites[0];
                }
                
                if (sprite != null) { portrait.sprite = sprite; portrait.color = Color.white; }
                else { portrait.color = new Color(0, 0, 0, 0); }
                
                RectTransform portRt = portrait.GetComponent<RectTransform>();
                if (profile.id == "미나") {
                    // Keep Mina at her original size
                    portRt.offsetMin = new Vector2(60, 60);
                    portRt.offsetMax = new Vector2(10, -50);
                } else if (profile.id == "카스미" || profile.id == "하루카") {
                    // Shrink Kasumi and Haruka (increase vertical padding)
                    portRt.offsetMin = new Vector2(60, 100);
                    portRt.offsetMax = new Vector2(10, -90);
                } else {
                    // Shrink Seika, Rina, Lilith
                    portRt.offsetMin = new Vector2(30, 100);
                    portRt.offsetMax = new Vector2(-20, -90);
                }
            }
            if (nameTxt != null) {
                bool isGothic = !HalloweenVN.Core.SettingsData.UseHandwritingFont;
                nameTxt.text = profile.name;
                nameTxt.fontSize = isGothic ? 34 : 48;
            }
            if (profileTxt != null) {
                bool isGothic = !HalloweenVN.Core.SettingsData.UseHandwritingFont;
                profileTxt.fontSize = isGothic ? 24 : 32;
            }
            UpdateProfileText(profileTxt, profile);

        }
    }
}


