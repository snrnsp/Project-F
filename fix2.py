# -*- coding: cp949 -*-
import os

extra_ui = """using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TMPro;

namespace HalloweenVN.UI
{
    public class CharacterProfile
    {
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
        [SerializeField] private GameObject backlogPanel;
        [SerializeField] private Button closeButton;
        
        // Character Info
        [SerializeField] private Image portraitImage;
        [SerializeField] private TextMeshProUGUI nameText;
        [SerializeField] private TextMeshProUGUI profileText;
        
        private List<CharacterProfile> profiles = new List<CharacterProfile>();
        private List<Button> characterTabs = new List<Button>();

        private void Awake()
        {
            InitializeProfiles();
        }

        private void OnEnable()
        {
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }
        }

        private void OnDisable()
        {
            if (closeButton != null)
            {
                closeButton.onClick.RemoveListener(Hide);
            }
        }

        private void InitializeProfiles()
        {
            profiles.Clear();

            profiles.Add(new CharacterProfile
            {
                name = "세이카 (Seika)",
                spritePath = "Characters/세이카/기본",
                age = "25세",
                role = "사무소 소장 / 경영·법무 담당",
                mbti = "ENTJ",
                appearance = "짙은 보라~남색 단발머리에 하트 모양 골드 귀걸이. 맑은 푸른 눈. 검은 트렌치코트 안쪽의 버건디 컬러가 세련되고 도시적인 분위기.",
                personality = "「네버모어 오컬트 탐정 사무소」의 설립자이자 소장. 카리스마가 있고 결단력이 빠르며, 할로윈과 오컬트에 진심으로 열광한다.",
                speechStyle = "반말 위주. 호탕하게 웃는 편.\\n\"후훗, 보기 좋잖아? '네버모어'라는 이름에 딱 맞는 인테리어지.\"",
                secret = "사무소를 차린 진짜 이유: 과거 자신이 경험한 '설명할 수 없는 사건'의 진상을 밝히기 위해."
            });

            profiles.Add(new CharacterProfile
            {
                name = "카스미 (Kasumi)",
                spritePath = "Characters/카스미/기본",
                age = "23세",
                role = "수석 탐정 / 실질적 두뇌",
                mbti = "INTJ",
                appearance = "허리까지 오는 짙은 남보라색 긴머리. 금안. 활동적인 밤색 셔츠와 검은 하네스. 블랙톤. 단정하면서도 날카로운 인상.",
                personality = "철저한 현실주의자. 유령, 혼, 초자연적 현상 따위는 믿지 않으며, 모든 사건에는 반드시 물리적 원인이 있다고 확신한다. 겉으로는 차갑지만 동료가 위험에 처하면 가장 먼저 앞장선다.",
                speechStyle = "존댓말 위주. 격식 있고 건조하게.\\n\"...몇 번을 말씀드렸습니까. 유령 따위는 존재하지 않는다고요.\"",
                secret = "어린 시절 해결하지 못한 '사라진 언니'의 장기 미제 사건을 쫓고 있다. 탐정이 된 진짜 이유."
            });

            profiles.Add(new CharacterProfile
            {
                name = "리나 (Rina)",
                spritePath = "Characters/리나/기본",
                age = "21세",
                role = "현장 돌격 담당 / 행동대장",
                mbti = "ESTP",
                appearance = "연한 갈색 숏컷 머리. 붉은색 X자 귀걸이. 푸른 눈. 검은 오버사이즈 봄버 재킷. 워커 부츠. 스포티하고 힙한 자세.",
                personality = "생각보다 몸이 먼저 움직이는 타입. 겁이 없고 도발적이며 에너지가 넘친다. 사무소에서 가장 시끄러운 존재. 의외로 동물적인 직감은 날카롭다.",
                speechStyle = "반말 위주. 활기차고 직설적.\\n\"아 진짜?! 또 귀신 타령이야? 이번엔 그냥 때려부수고 들어가면 안 돼?\"",
                secret = "사실 어둠을 무서워한다. 또, 폐건물이나 위험한 현장에 갈 때 가장 가까운 사람을 꼭 매달고 가는 버릇이 있다."
            });

            profiles.Add(new CharacterProfile
            {
                name = "리리스 (Lilith)",
                spritePath = "Characters/리리스/기본",
                age = "20세",
                role = "기술·정보 담당 / 해커 & 드론 조종사",
                mbti = "ISTP",
                appearance = "은발 트윈테일. 고양이 모양 헤드셋. 청록색 눈동자. 항상 태블릿과 해킹용 케이블을 들고 다니는 너드스타일.",
                personality = "말수가 적고 만사를 귀찮아하는 천재 해커. 온라인에서는 '유령 드론'이라는 닉네임으로 유명하다. 인간보다 기계(특히 자신이 개조한 정찰 드론 '잭오')를 더 신뢰한다.",
                speechStyle = "단답형 위주. 무심하게.\\n\"...백도어 열었어. 3초 뒤에 카메라 꺼질 거야. 귀찮게 하지 마.\"",
                secret = "매일 밤 잭오(드론)를 이용해 도시 전체의 '이상 열원'을 스캔하고 있다. 무엇을 찾고 있는지는 아무도 모른다."
            });

            profiles.Add(new CharacterProfile
            {
                name = "미나 (Mina)",
                spritePath = "Characters/미나/기본",
                age = "1,000살",
                role = "오컬트 고문 / 정체불명의 조력자",
                mbti = "INFJ",
                appearance = "하얀 은발. 붉은 눈. 고풍스러운 검은 드레스와 붉은 장미 코르사주. 뱀파이어를 연상시키는 고딕 룩. 나이를 가늠할 수 없는 묘한 분위기.",
                personality = "자신이 1000년을 묵은 원혼이라고 주장하는 중2병 소녀. 평소에는 알 수 없는 시를 읊거나 저주를 내리겠다며 허세를 부리지만, 오컬트 지식만큼은 전문가 수준이다.",
                speechStyle = "고어체(하오체/하게체) 위주. 과장되게.\\n\"크큭... 어리석은 인간들이여. 이 저택의 심연을 엿볼 준비는 되었느냐?\"",
                secret = "사실 무서운 것을 보면 가장 먼저 도망치거나 기절한다. 진짜 나이와 정체는 본인도 모른다(기억상실)."
            });

            profiles.Add(new CharacterProfile
            {
                name = "하루카 (Haruka)",
                spritePath = "Characters/하루카/기본",
                age = "19세",
                role = "사무소 접수 및 행정 / 마스코트",
                mbti = "ISFJ",
                appearance = "부드러운 연갈색 긴 생머리. 눈물점이 있는 호박색 눈. 프릴이 달린 단정한 블라우스와 치마. 다정하고 차분한 인상.",
                personality = "네버모어의 상식인이자 엄마 같은 존재. 괴짜들 사이에서 유일하게 정상적인 사고방식을 가졌다. 청소, 요리, 의뢰인 접대를 완벽하게 해낸다.",
                speechStyle = "존댓말 위주. 다정하고 부드럽게.\\n\"다들 싸우지 마세요~! 차 끓여왔으니까 진정하고 다시 얘기해 봐요.\"",
                secret = "화가 나면 팀 내에서 가장 무섭다. 특히 예산을 함부로 쓸 때 (세이카의 할로윈 소품 구매 등) 나오는 미소는 모두를 떨게 한다."
            });
        }

        public void RegisterTab(Button tab)
        {
            characterTabs.Add(tab);
        }

        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (extraPanel != null)
            {
                extraPanel.SetActive(true);
                SelectCharacter(0); // Show Seika by default
            }
        }

        public void Hide()
        {
            if (extraPanel != null)
            {
                extraPanel.SetActive(false);
            }
        }

        public void SelectCharacter(int index)
        {
            if (index < 0 || index >= profiles.Count) return;

            CharacterProfile profile = profiles[index];
            
            if (nameText != null) nameText.text = profile.name;
            
            if (portraitImage != null)
            {
                Sprite sprite = Resources.Load<Sprite>(profile.spritePath);
                if (sprite != null)
                {
                    portraitImage.sprite = sprite;
                    portraitImage.color = Color.white;
                }
                else
                {
                    portraitImage.color = new Color(0,0,0,0); // Hide if not found
                }
            }

            if (profileText != null)
            {
                profileText.text = 
                    $"<color=#ffaa00>나이:</color> {profile.age}\\n" +
                    $"<color=#ffaa00>역할:</color> {profile.role}\\n" +
                    $"<color=#ffaa00>MBTI:</color> {profile.mbti}\\n\\n" +
                    $"<color=#ffaa00>외모:</color> {profile.appearance}\\n\\n" +
                    $"<color=#ffaa00>성격:</color> {profile.personality}\\n\\n" +
                    $"<color=#ffaa00>말투:</color> {profile.speechStyle}\\n\\n" +
                    $"<color=#ffaa00>비밀:</color> {profile.secret}";
            }
        }
    }
}"""

settings_ui = """using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using HalloweenVN.Core;

namespace HalloweenVN.UI
{
    public class SettingsUI : MonoBehaviour
    {
        [SerializeField] private GameObject settingsPanel;
        [SerializeField] private Slider textSpeedSlider;
        [SerializeField] private Text textSpeedLabel;
        [SerializeField] private Slider bgmVolumeSlider;
        [SerializeField] private Text bgmVolumeLabel;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Text sfxVolumeLabel;
        [SerializeField] private Toggle fullscreenToggle;
        [SerializeField] private Button closeButton;
        
        [SerializeField] private Text previewTextLabel;
        [SerializeField] private Text titleTextLabel;
        [SerializeField] private Text closeButtonText;
        private Coroutine typingCoroutine;
        private string previewMessage = "텍스트 속도가 이 정도로 출력됩니다. 눈으로 확인해 보세요!";

        private void OnEnable()
        {
            if (textSpeedSlider != null)
            {
                textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                textSpeedSlider.onValueChanged.AddListener(OnTextSpeedChanged);
            }
            if (bgmVolumeSlider != null)
            {
                bgmVolumeSlider.value = SettingsData.BGMVolume;
                bgmVolumeSlider.onValueChanged.AddListener(OnBGMVolumeChanged);
            }
            if (sfxVolumeSlider != null)
            {
                sfxVolumeSlider.value = SettingsData.SFXVolume;
                sfxVolumeSlider.onValueChanged.AddListener(OnSFXVolumeChanged);
            }
            if (fullscreenToggle != null)
            {
                fullscreenToggle.isOn = SettingsData.IsFullScreen;
                fullscreenToggle.onValueChanged.AddListener(OnFullscreenChanged);
            }
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }

            UpdateLabels();
            UpdateLanguage();
        }

        public void UpdateLanguage()
        {
            GameLanguage lang = SettingsData.Language;

            if (lang == GameLanguage.Korean)
            {
                if (titleTextLabel != null) titleTextLabel.text = "설정";
                if (textSpeedLabel != null) textSpeedLabel.text = "텍스트 속도";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "닫기";
                previewMessage = "텍스트 속도가 이 정도로 출력됩니다. 눈으로 확인해 보세요!";
            }
            else if (lang == GameLanguage.English)
            {
                if (titleTextLabel != null) titleTextLabel.text = "Settings";
                if (textSpeedLabel != null) textSpeedLabel.text = "Text Speed";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "Close";
                previewMessage = "This is a text speed test. Please check it carefully!";
            }
            else if (lang == GameLanguage.Japanese)
            {
                if (titleTextLabel != null) titleTextLabel.text = "設定";
                if (textSpeedLabel != null) textSpeedLabel.text = "テキスト速度";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "閉じる";
                previewMessage = "テキスト速度のテストです。ご確認ください。";
            }
            else if (lang == GameLanguage.ChineseSimplified)
            {
                if (titleTextLabel != null) titleTextLabel.text = "设置";
                if (textSpeedLabel != null) textSpeedLabel.text = "文本速度";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "背景音乐";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "音效";
                if (closeButtonText != null) closeButtonText.text = "关闭";
                previewMessage = "这是文本速度测试。请仔细检查！";
            }
            else if (lang == GameLanguage.ChineseTraditional)
            {
                if (titleTextLabel != null) titleTextLabel.text = "設定";
                if (textSpeedLabel != null) textSpeedLabel.text = "文本速度";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "背景音樂";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "音效";
                if (closeButtonText != null) closeButtonText.text = "關閉";
                previewMessage = "這是文本速度測試。請仔細檢查。";
            }
            
            PlayPreviewText();
        }

        private void OnDisable()
        {
            if (textSpeedSlider != null) textSpeedSlider.onValueChanged.RemoveListener(OnTextSpeedChanged);
            if (bgmVolumeSlider != null) bgmVolumeSlider.onValueChanged.RemoveListener(OnBGMVolumeChanged);
            if (sfxVolumeSlider != null) sfxVolumeSlider.onValueChanged.RemoveListener(OnSFXVolumeChanged);
            if (fullscreenToggle != null) fullscreenToggle.onValueChanged.RemoveListener(OnFullscreenChanged);
            if (closeButton != null) closeButton.onClick.RemoveListener(Hide);
        }

        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(true);
                if (textSpeedSlider != null) textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                if (bgmVolumeSlider != null) bgmVolumeSlider.value = SettingsData.BGMVolume;
                if (sfxVolumeSlider != null) sfxVolumeSlider.value = SettingsData.SFXVolume;
                if (fullscreenToggle != null) fullscreenToggle.isOn = SettingsData.IsFullScreen;
                
                UpdateLabels();
                PlayPreviewText();
            }
        }

        public void Hide()
        {
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(false);
            }
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
                typingCoroutine = null;
            }
        }

        private void PlayPreviewText()
        {
            if (previewTextLabel == null) return;
            
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
            }
            
            if (gameObject.activeInHierarchy)
            {
                typingCoroutine = StartCoroutine(TypePreviewCoroutine());
            }
        }
        
        private System.Collections.IEnumerator TypePreviewCoroutine()
        {
            int totalChars = previewMessage.Length;
            
            while (true)
            {
                previewTextLabel.text = "";
                
                for (int i = 0; i <= totalChars; i++)
                {
                    previewTextLabel.text = previewMessage.Substring(0, i);
                    yield return new WaitForSeconds(SettingsData.TextSpeed);
                }
                
                yield return new WaitForSeconds(2f);
            }
        }

        private void OnTextSpeedChanged(float val)
        {
            SettingsData.TextSpeed = SliderToSpeed(val);
            UpdateLabels();
            PlayPreviewText();
        }

        private void OnBGMVolumeChanged(float val)
        {
            SettingsData.BGMVolume = val;
            UpdateLabels();
        }

        private void OnSFXVolumeChanged(float val)
        {
            SettingsData.SFXVolume = val;
            UpdateLabels();
        }

        private void OnFullscreenChanged(bool val)
        {
            SettingsData.IsFullScreen = val;
            Screen.fullScreen = val;
        }

        private void UpdateLabels()
        {
        }

        private float SpeedToSlider(float speed)
        {
            float t = Mathf.InverseLerp(0.1f, 0.01f, speed);
            return Mathf.Lerp(0f, 100f, t);
        }

        private float SliderToSpeed(float sliderVal)
        {
            float t = Mathf.InverseLerp(0f, 100f, sliderVal);
            return Mathf.Lerp(0.1f, 0.01f, t);
        }
    }
}"""

with open("c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs", "w", encoding="utf-8-sig") as f:
    f.write(extra_ui)

with open("c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs", "w", encoding="utf-8-sig") as f:
    f.write(settings_ui)

print("Files successfully written with UTF-8 BOM encoding!")
