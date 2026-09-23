import codecs

extra_ui_code = '''using System.Collections.Generic;
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
                name = "''' + "\\uC138\\uC774\\uCE74 (Seika)" + '''",
                spritePath = "Characters/''' + "\\uC138\\uC774\\uCE74/\\uAE30\\uBCF8" + '''",
                age = "25''' + "\\uC138" + '''",
                role = "''' + "\\uC0AC\\uBB34\\uC18C \\uC18C\\uC7A5 / \\uACBD\\uC601\\u00B7\\uBC95\\uBB34 \\uB2F4\\uB2F9" + '''",
                mbti = "ENTJ",
                appearance = "''' + "\\uC9D9\\uC740 \\uBCF4\\uB77C~\\uB0A8\\uC0C9 \\uB2E8\\uBC1C\\uBA38\\uB9AC\\uC5D0 \\uD558\\uD2B8 \\uBAA8\\uC591 \\uACE8\\uB4DC \\uADC0\\uAC78\\uC774. \\uB9D1\\uC740 \\uD478\\uB978 \\uB208. \\uAC80\\uC740 \\uD2B8\\uB80C\\uCE58\\uCF54\\uD2B8 \\uC548\\uCABD\\uC758 \\uBC84\\uAC74\\uB514 \\uCEEC\\uB7EC\\uAC00 \\uC138\\uB828\\uB418\\uACE0 \\uB3C4\\uC2DC\\uC801\\uC778 \\uBD84\\uC704\\uAE30." + '''",
                personality = "''' + "\\u300C\\uB124\\uBC84\\uBAA8\\uC5B4 \\uC624\\uCEEC\\uD2B8 \\uD0D0\\uC815 \\uC0AC\\uBB34\\uC18C\\u300D\\uC758 \\uC124\\uB9BD\\uC790\\uC774\\uC790 \\uC18C\\uC7A5. \\uCE74\\uB9AC\\uC2A4\\uB9C8\\uAC00 \\uC788\\uACE0 \\uACB0\\uB2E8\\uB825\\uC774 \\uBE60\\uB974\\uBA70, \\uD560\\uB85C\\uC708\\uACFC \\uC624\\uCEEC\\uD2B8\\uC5D0 \\uC9C4\\uC2EC\\uC73C\\uB85C \\uC5F4\\uAD11\\uD55C\\uB2E4." + '''",
                speechStyle = "''' + "\\uBC18\\uB9D0 \\uC704\\uC8FC. \\uD638\\uD0D5\\uD558\\uAC8C \\uC6C3\\uB294 \\uD3B8.\\n\\\"\\uD6C4\\uD6FB, \\uBCF4\\uAE30 \\uC88B\\uC796\\uC544? '\\uB124\\uBC84\\uBAA8\\uC5B4'\\uB77C\\uB294 \\uC774\\uB984\\uC5D0 \\uB531 \\uB9DE\\uB294 \\uC778\\uD14C\\uB9AC\\uC5B4\\uC9C0.\\\"" + '''",
                secret = "''' + "\\uC0AC\\uBB34\\uC18C\\uB97C \\uCC28\\uB9B0 \\uC9C4\\uC9DC \\uC774\\uC720: \\uACFC\\uAC70 \\uC790\\uC2E0\\uC774 \\uACBD\\uD5D8\\uD55C '\\uC124\\uBA85\\uD560 \\uC218 \\uC5C6\\uB294 \\uC0AC\\uAC74'\\uC758 \\uC9C4\\uC0C1\\uC744 \\uBC1D\\uD788\\uAE30 \\uC704\\uD574." + '''"
            });

            profiles.Add(new CharacterProfile
            {
                name = "''' + "\\uCE74\\uC2A4\\uBBF8 (Kasumi)" + '''",
                spritePath = "Characters/''' + "\\uCE74\\uC2A4\\uBBF8/\\uAE30\\uBCF8" + '''",
                age = "23''' + "\\uC138" + '''",
                role = "''' + "\\uC218\\uC11D \\uD0D0\\uC815 / \\uC2E4\\uC9C8\\uC801 \\uB450\\uB1CC" + '''",
                mbti = "INTJ",
                appearance = "''' + "\\uD5C8\\uB9AC\\uAE4C\\uC9C0 \\uC624\\uB294 \\uC9D9\\uC740 \\uB0A8\\uBCF4\\uB77C\\uC0C9 \\uAE34\\uBA38\\uB9AC. \\uAE08\\uC548. \\uD65C\\uB3D9\\uC801\\uC778 \\uBC24\\uC0C9 \\uC154\\uCE20\\uC640 \\uAC80\\uC740 \\uD558\\uB124\\uC2A4. \\uBE14\\uB799\\uD1A4. \\uB2E8\\uC815\\uD558\\uBA74\\uC11C\\uB3C4 \\uB0A0\\uCE74\\uB85C\\uC6B4 \\uC778\\uC0C1." + '''",
                personality = "''' + "\\uCCA0\\uC800\\uD55C \\uD604\\uC2E4\\uC8FC\\uC758\\uC790. \\uC720\\uB839, \\uD63C, \\uCD08\\uC790\\uC5F0\\uC801 \\uD604\\uC0C1 \\uB530\\uC704\\uB294 \\uBBFF\\uC9C0 \\uC54A\\uC73C\\uBA70, \\uBAA8\\uB4E0 \\uC0AC\\uAC74\\uC5D0\\uB294 \\uBC18\\uB4DC\\uC2DC \\uBB3C\\uB9AC\\uC801 \\uC6D0\\uC778\\uC774 \\uC788\\uB2E4\\uACE0 \\uD655\\uC2E0\\uD55C\\uB2E4. \\uAC89\\uC73C\\uB85C\\uB294 \\uCC28\\uAC11\\uC9C0\\uB9CC \\uB3D9\\uB8CC\\uAC00 \\uC704\\uD5D8\\uC5D0 \\uCC98\\uD558\\uBA74 \\uAC00\\uC7A5 \\uBA3C\\uC800 \\uC55E\\uC7A5\\uC120\\uB2E4." + '''",
                speechStyle = "''' + "\\uC874\\uB313\\uB9D0 \\uC704\\uC8FC. \\uACA9\\uC2DD \\uC788\\uACE0 \\uAC74\\uC870\\uD558\\uAC8C.\\n\\\"...\\uBA87 \\uBC88\\uC744 \\uB9D0\\uC500\\uB4DC\\uB838\\uC2B5\\uB2C8\\uAE4C. \\uC720\\uB839 \\uB530\\uC704\\uB294 \\uC874\\uC7AC\\uD558\\uC9C0 \\uC54A\\uB294\\uB2E4\\uACE0\\uC694.\\\"" + '''",
                secret = "''' + "\\uC5B4\\uB9B0 \\uC2DC\\uC808 \\uD574\\uACB0\\uD558\\uC9C0 \\uBABB\\uD55C '\\uC0AC\\uB77C\\uC9C4 \\uC5B8\\uB2C8'\\uC758 \\uC7A5\\uAE30 \\uBBF8\\uC81C \\uC0AC\\uAC74\\uC744 \\uCAD3\\uACE0 \\uC788\\uB2E4. \\uD0D0\\uC815\\uC774 \\uB41C \\uC9C4\\uC9DC \\uC774\\uC720." + '''"
            });

            profiles.Add(new CharacterProfile
            {
                name = "''' + "\\uB9AC\\uB098 (Rina)" + '''",
                spritePath = "Characters/''' + "\\uB9AC\\uB098/\\uAE30\\uBCF8" + '''",
                age = "21''' + "\\uC138" + '''",
                role = "''' + "\\uD604\\uC7A5 \\uB3CC\\uACA9 \\uB2F4\\uB2F9 / \\uD589\\uB3D9\\uB300\\uC7A5" + '''",
                mbti = "ESTP",
                appearance = "''' + "\\uC5F0\\uD55C \\uAC08\\uC0C9 \\uC20F\\uCEF7 \\uBA38\\uB9AC. \\uBD89\\uC740\\uC0C9 X\\uC790 \\uADC0\\uAC78\\uC774. \\uD478\\uB978 \\uB208. \\uAC80\\uC740 \\uC624\\uBC84\\uC0AC\\uC774\\uC988 \\uBD04\\uBC84 \\uC7AC\\uD0B7. \\uC6CC\\uCEE4 \\uBD80\\uCE20. \\uC2A4\\uD3EC\\uD2F0\\uD558\\uACE0 \\uD799\\uD55C \\uC790\\uC138." + '''",
                personality = "''' + "\\uC0DD\\uAC01\\uBCF4\\uB2E4 \\uBAB8\\uC774 \\uBA3C\\uC800 \\uC6C0\\uC9C1\\uC774\\uB294 \\uD0C0\\uC785. \\uAC81\\uC774 \\uC5C6\\uACE0 \\uB3C4\\uBC1C\\uC801\\uC774\\uBA70 \\uC5D0\\uB108\\uC9C0\\uAC00 \\uB118\\uCE5C\\uB2E4. \\uC0AC\\uBB34\\uC18C\\uC5D0\\uC11C \\uAC00\\uC7A5 \\uC2DC\\uB044\\uB7EC\\uC6B4 \\uC874\\uC7AC. \\uC758\\uC678\\uB85C \\uB3D9\\uBB3C\\uC801\\uC778 \\uC9C1\\uAC10\\uC740 \\uB0A0\\uCE74\\uB86D\\uB2E4." + '''",
                speechStyle = "''' + "\\uBC18\\uB9D0 \\uC704\\uC8FC. \\uD65C\\uAE30\\uCC28\\uACE0 \\uC9C1\\uC124\\uC801.\\n\\\"\\uC544 \\uC9C4\\uC9DC?! \\uB610 \\uADC0\\uC2E0 \\uD0C0\\uB839\\uC774\\uC57C? \\uC774\\uBC88\\uC5D4 \\uADF8\\uB0E5 \\uB54C\\uB824\\uBD80\\uC218\\uACE0 \\uB4E4\\uC5B4\\uAC00\\uBA74 \\uC548 \\uB3FC?\\\"" + '''",
                secret = "''' + "\\uC0AC\\uC2E4 \\uC5B4\\uB460\\uC744 \\uBB34\\uC11C\\uC6CC\\uD55C\\uB2E4. \\uB610, \\uD3D0\\uAC74\\uBB3C\\uC774\\uB098 \\uC704\\uD5D8\\uD55C \\uD604\\uC7A5\\uC5D0 \\uAC08 \\uB54C \\uAC00\\uC7A5 \\uAC00\\uAE4C\\uC6B4 \\uC0AC\\uB78C\\uC744 \\uAF2D \\uB9E4\\uB2EC\\uACE0 \\uAC00\\uB294 \\uBC84\\uB987\\uC774 \\uC788\\uB2E4." + '''"
            });

            profiles.Add(new CharacterProfile
            {
                name = "''' + "\\uB9AC\\uB9AC\\uC2A4 (Lilith)" + '''",
                spritePath = "Characters/''' + "\\uB9AC\\uB9AC\\uC2A4/\\uAE30\\uBCF8" + '''",
                age = "20''' + "\\uC138" + '''",
                role = "''' + "\\uAE30\\uC220\\u00B7\\uC815\\uBCF4 \\uB2F4\\uB2F9 / \\uD574\\uCEE4 & \\uB4DC\\uB860 \\uC870\\uC885\\uC0AC" + '''",
                mbti = "ISTP",
                appearance = "''' + "\\uC740\\uBC1C \\uD2B8\\uC708\\uD14C\\uC77C. \\uACE0\\uC591\\uC774 \\uBAA8\\uC591 \\uD5E4\\uB4DC\\uC14B. \\uCCAD\\uB85D\\uC0C9 \\uB208\\uB3D9\\uC790. \\uD56D\\uC0C1 \\uD0DC\\uBE14\\uB9BF\\uACFC \\uD574\\uD0B9\\uC6A9 \\uCF00\\uC774\\uBE14\\uC744 \\uB4E4\\uACE0 \\uB2E4\\uB2C8\\uB294 \\uB108\\uB4DC\\uC2A4\\uD0C0\\uC77C." + '''",
                personality = "''' + "\\uB9D0\\uC218\\uAC00 \\uC801\\uACE0 \\uB9CC\\uC0AC\\uB97C \\uADC0\\uCC2E\\uC544\\uD558\\uB294 \\uCC9C\\uC7AC \\uD574\\uCEE4. \\uC628\\uB77C\\uC778\\uC5D0\\uC11C\\uB294 '\\uC720\\uB839 \\uB4DC\\uB860'\\uC774\\uB77C\\uB294 \\uB2C9\\uB124\\uC784\\uC73C\\uB85C \\uC720\\uBA85\\uD558\\uB2E4. \\uC778\\uAC04\\uBCF4\\uB2E4 \\uAE30\\uACC4(\\uD2B9\\uD788 \\uC790\\uC2E0\\uC774 \\uAC1C\\uC870\\uD55C \\uC815\\uCC30 \\uB4DC\\uB860 '\\uC7AD\\uC624')\\uB97C \\uB354 \\uC2E0\\uB8B0\\uD55C\\uB2E4." + '''",
                speechStyle = "''' + "\\uB2E8\\uB2F5\\uD615 \\uC704\\uC8FC. \\uBB34\\uC2EC\\uD558\\uAC8C.\\n\\\"...\\uBC31\\uB3C4\\uC5B4 \\uC5F4\\uC5C8\\uC5B4. 3\\uCD08 \\uB4A4\\uC5D0 \\uCE74\\uBA54\\uB77C \\uAEBC\\uC9C8 \\uAC70\\uC57C. \\uADC0\\uCC2E\\uAC8C \\uD558\\uC9C0 \\uB9C8.\\\"" + '''",
                secret = "''' + "\\uB9E4\\uC77C \\uBC24 \\uC7AD\\uC624(\\uB4DC\\uB860)\\uB97C \\uC774\\uC6A9\\uD574 \\uB3C4\\uC2DC \\uC804\\uCCB4\\uC758 '\\uC774\\uC0C1 \\uC5F4\\uC6D0'\\uC744 \\uC2A4\\uCE94\\uD558\\uACE0 \\uC788\\uB2E4. \\uBB34\\uC5C7\\uC744 \\uCC3E\\uACE0 \\uC788\\uB294\\uC9C0\\uB294 \\uC544\\uBB34\\uB3C4 \\uBAA8\\uB978\\uB2E4." + '''"
            });

            profiles.Add(new CharacterProfile
            {
                name = "''' + "\\uBBF8\\uB098 (Mina)" + '''",
                spritePath = "Characters/''' + "\\uBBF8\\uB098/\\uAE30\\uBCF8" + '''",
                age = "1,000''' + "\\uC0B4" + '''",
                role = "''' + "\\uC624\\uCEEC\\uD2B8 \\uACE0\\uBB38 / \\uC815\\uCCB4\\uBD88\\uBA85\\uC758 \\uC870\\uB825\\uC790" + '''",
                mbti = "INFJ",
                appearance = "''' + "\\uD558\\uC580 \\uC740\\uBC1C. \\uBD89\\uC740 \\uB208. \\uACE0\\uD48D\\uC2A4\\uB7EC\\uC6B4 \\uAC80\\uC740 \\uB4DC\\uB808\\uC2A4\\uC640 \\uBD89\\uC740 \\uC7A5\\uBBF8 \\uCF54\\uB974\\uC0AC\\uC8FC. \\uBC40\\uD30C\\uC774\\uC5B4\\uB97C \\uC5F0\\uC0C1\\uC2DC\\uD0A4\\uB294 \\uACE0\\uB515 \\uB8E9. \\uB098\\uC774\\uB97C \\uAC00\\uB2A0\\uD560 \\uC218 \\uC5C6\\uB294 \\uBB18\\uD55C \\uBD84\\uC704\\uAE30." + '''",
                personality = "''' + "\\uC790\\uC2E0\\uC774 1000\\uB144\\uC744 \\uBB35\\uC740 \\uC6D0\\uD63C\\uC774\\uB77C\\uACE0 \\uC8FC\\uC7A5\\uD558\\uB294 \\uC9112\\uBCD1 \\uC18C\\uB140. \\uD3C9\\uC18C\\uC5D0\\uB294 \\uC54C \\uC218 \\uC5C6\\uB294 \\uC2DC\\uB97C \\uC74A\\uAC70\\uB098 \\uC800\\uC8FC\\uB97C \\uB0B4\\uB9AC\\uACA0\\uB2E4\\uBA70 \\uD5C8\\uC138\\uB97C \\uBD80\\uB9AC\\uC9C0\\uB9CC, \\uC624\\uCEEC\\uD2B8 \\uC9C0\\uC2DD\\uB9CC\\uD07C\\uC740 \\uC804\\uBB38\\uAC00 \\uC218\\uC900\\uC774\\uB2E4." + '''",
                speechStyle = "''' + "\\uACE0\\uC5B4\\uCCB4(\\uD558\\uC624\\uCCB4/\\uD558\\uAC8C\\uCCB4) \\uC704\\uC8FC. \\uACFC\\uC7A5\\uB418\\uAC8C.\\n\\\"\\uD06C\\uD0B9... \\uC5B4\\uB9AC\\uC11D\\uC740 \\uC778\\uAC04\\uB4E4\\uC774\\uC5EC. \\uC774 \\uC800\\uD0DD\\uC758 \\uC2EC\\uC5F0\\uC744 \\uC5FF\\uBCFC \\uC900\\uBE44\\uB294 \\uB418\\uC5C8\\uB290\\uB0D0?\\\"" + '''",
                secret = "''' + "\\uC0AC\\uC2E4 \\uBB34\\uC11C\\uC6B4 \\uAC83\\uC744 \\uBCF4\\uBA74 \\uAC00\\uC7A5 \\uBA3C\\uC800 \\uB3C4\\uB9DD\\uCE58\\uAC70\\uB098 \\uAE30\\uC808\\uD55C\\uB2E4. \\uC9C4\\uC9DC \\uB098\\uC774\\uC640 \\uC815\\uCCB4\\uB294 \\uBCF8\\uC778\\uB3C4 \\uBAA8\\uB978\\uB2E4(\\uAE30\\uC5B5\\uC0C1\\uC2E4)." + '''"
            });

            profiles.Add(new CharacterProfile
            {
                name = "''' + "\\uD558\\uB8E8\\uCE74 (Haruka)" + '''",
                spritePath = "Characters/''' + "\\uD558\\uB8E8\\uCE74/\\uAE30\\uBCF8" + '''",
                age = "19''' + "\\uC138" + '''",
                role = "''' + "\\uC0AC\\uBB34\\uC18C \\uC811\\uC218 \\uBC0F \\uD589\\uC815 / \\uB9C8\\uC2A4\\uCF54\\uD2B8" + '''",
                mbti = "ISFJ",
                appearance = "''' + "\\uBD80\\uB4DC\\uB7EC\\uC6B4 \\uC5F0\\uAC08\\uC0C9 \\uAE34 \\uC0DD\\uBA38\\uB9AC. \\uB208\\uBB3C\\uC810\\uC774 \\uC788\\uB294 \\uD638\\uBC15\\uC0C9 \\uB208. \\uD504\\uB9B4\\uC774 \\uB2EC\\uB9B0 \\uB2E8\\uC815\\uD55C \\uBE14\\uB77C\\uC6B0\\uC2A4\\uC640 \\uCE58\\uB9C8. \\uB2E4\\uC815\\uD558\\uACE0 \\uCC28\\uBD84\\uD55C \\uC778\\uC0C1." + '''",
                personality = "''' + "\\uB124\\uBC84\\uBAA8\\uC5B4\\uC758 \\uC0C1\\uC2DD\\uC778\\uC774\\uC790 \\uC5C4\\uB9C8 \\uAC19\\uC740 \\uC874\\uC7AC. \\uAD34\\uC9DC\\uB4E4 \\uC0AC\\uC774\\uC5D0\\uC11C \\uC720\\uC77C\\uD558\\uAC8C \\uC815\\uC0C1\\uC801\\uC778 \\uC0AC\\uACE0\\uBC29\\uC2DD\\uC744 \\uAC00\\uC84C\\uB2E4. \\uCCAD\\uC18C, \\uC694\\uB9AC, \\uC758\\uB8B0\\uC778 \\uC811\\uB300\\uB97C \\uC644\\uBCBD\\uD558\\uAC8C \\uD574\\uB0B8\\uB2E4." + '''",
                speechStyle = "''' + "\\uC874\\uB313\\uB9D0 \\uC704\\uC8FC. \\uB2E4\\uC815\\uD558\\uACE0 \\uBD80\\uB4DC\\uB7FD\\uAC8C.\\n\\\"\\uB2E4\\uB4E4 \\uC2F8\\uC6B0\\uC9C0 \\uB9C8\\uC138\\uC694~! \\uCC28 \\uB053\\uC5EC\\uC654\\uC73C\\uB2C8\\uAE4C \\uC9C4\\uC815\\uD558\\uACE0 \\uB2E4\\uC2DC \\uC598\\uAE30\\uD574 \\uBD10\\uC694.\\\"" + '''",
                secret = "''' + "\\uD654\\uAC00 \\uB098\\uBA74 \\uD300 \\uB0B4\\uC5D0\\uC11C \\uAC00\\uC7A5 \\uBB34\\uC12D\\uB2E4. \\uD2B9\\uD788 \\uC608\\uC0B0\\uC744 \\uD568\\uBD80\\uB85C \\uC4F8 \\uB54C (\\uC138\\uC774\\uCE74\\uC758 \\uD560\\uB85C\\uC708 \\uC18C\\uD488 \\uAD6C\\uB9E4 \\uB4F1) \\uB098\\uC624\\uB294 \\uBBF8\\uC18C\\uB294 \\uBAA8\\uB450\\uB97C \\uB5A8\\uAC8C \\uD55C\\uB2E4." + '''"
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
                    $''' + '"<color=#ffaa00>\\uB098\\uC774:</color> {profile.age}\\n" +' + '''
                    $''' + '"<color=#ffaa00>\\uC5ED\\uD560:</color> {profile.role}\\n" +' + '''
                    $''' + '"<color=#ffaa00>MBTI:</color> {profile.mbti}\\n\\n" +' + '''
                    $''' + '"<color=#ffaa00>\\uC678\\uBAA8:</color> {profile.appearance}\\n\\n" +' + '''
                    $''' + '"<color=#ffaa00>\\uC131\\uACA9:</color> {profile.personality}\\n\\n" +' + '''
                    $''' + '"<color=#ffaa00>\\uB9D0\\uD22C:</color> {profile.speechStyle}\\n\\n" +' + '''
                    $''' + '"<color=#ffaa00>\\uBE44\\uBC00:</color> {profile.secret}";' + '''
            }
        }
    }
}
'''

with codecs.open("c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs", "w", encoding="utf-8-sig") as f:
    f.write(extra_ui_code)
print("ExtraUI generated using Unicode escapes!")
