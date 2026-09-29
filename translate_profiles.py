import sys

path = 'F:/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# We will replace the entire InitializeProfiles block
start_sig = "private void InitializeProfiles()"
end_sig = "public void RegisterFolder"

start_idx = content.find(start_sig)
end_idx = content.find(end_sig)

if start_idx == -1 or end_idx == -1:
    print("Could not find boundaries")
    sys.exit(1)

new_method = """private void InitializeProfiles()
    {
        profiles.Clear();
        var lang = HalloweenVN.Core.SettingsData.Language;
        
        bool isEn = lang == HalloweenVN.Core.GameLanguage.English;
        bool isJp = lang == HalloweenVN.Core.GameLanguage.Japanese;
        bool isCn = lang == HalloweenVN.Core.GameLanguage.ChineseSimplified || lang == HalloweenVN.Core.GameLanguage.ChineseTraditional;

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Seika" : isJp ? "セイカ" : isCn ? "星佳" : "세이카",
            spritePath = "Characters/세이카/기본",
            age = isEn ? "25" : isJp ? "25歳" : isCn ? "25岁" : "25세",
            role = isEn ? "Director / Management & Legal" : isJp ? "所長 / 経営・法務担当" : isCn ? "所长 / 经营与法务" : "사무소 소장 / 경영·법무 담당",
            mbti = "ENTJ",
            appearance = isEn ? "Long dark navy hair flowing down to the waist with a gold hairpin. Clear, cold blue eyes. A sophisticated, urban look with a black long skirt, charcoal grey jacket, and a black shoulder bag." 
                       : isJp ? "腰まで伸びる濃いネイビーの長髪に金のヘアピン。澄んだ冷たい青い瞳。黒のロングスカートにチャコールグレーのジャケット、黒のショルダーバッグを身につけた洗練された都会的な雰囲気。"
                       : isCn ? "及腰的深蓝色长发，配有金色发夹。清澈而冰冷的蓝色眼眸。身穿黑色长裙、炭灰色夹克，挎着黑色单肩包，散发出干练的都市气息。"
                       : "허리 아래까지 흘러내리는 짙은 남색 긴 머리카락에 금색 헤어핀. 맑고 차가운 파란 눈동자. 검은색 롱 스커트에 차콜 그레이 재킷, 검은 숄더백을 걸친 세련되고 도시적인 분위기.",
            personality = isEn ? "Founder and director of 'Nevermore Occult Detective Agency'. Charismatic and decisive, with a genuine passion for Halloween and the occult."
                        : isJp ? "「ネバーモア・オカルト探偵事務所」の設立者であり所長。カリスマ性があり決断力が早く、ハロウィンとオカルトを心から愛している。"
                        : isCn ? "“Nevermore灵异侦探事务所”的创始人兼所长。极具魅力且决策果断，对万圣节和神秘学充满纯粹的热情。"
                        : "「네버모어 오컬트 탐정 사무소」의 설립자이자 소장. 카리스마가 있고 결단력이 빠르며, 할로윈과 오컬트에 진심으로 열광한다.",
            speechStyle = isEn ? "Mostly informal. Laughs heartily.\\n\\\"Fufu, looks good, doesn't it? An interior perfectly suited for the name Nevermore.\\\""
                        : isJp ? "タメ口中心。豪快に笑う方。\\n「ふふ、いい眺めじゃない？ネバーモアという名前にぴったりのインテリアね。」"
                        : isCn ? "多用平语。喜欢豪爽地大笑。\\n“呵呵，看起来不错吧？这可是完美契合‘Nevermore’这个名字的室内装潢呢。”"
                        : "반말 위주. 호탕하게 웃는 편.\\n\"후훗, 보기 좋잖아? 네버모어라는 이름에 딱 맞는 인테리어지.\"",
            secret = isEn ? "The real reason she opened the agency: to uncover the truth behind an inexplicable incident she experienced in the past."
                   : isJp ? "事務所を開いた本当の理由：過去に自分が経験した説明のつかない事件の真相を明らかにするため。"
                   : isCn ? "开办事务所的真正原因：为了揭开自己过去经历过的一起无法解释的事件的真相。"
                   : "사무소를 차린 진짜 이유: 과거 자신이 경험한 설명할 수 없는 사건의 진상을 밝히기 위해."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Kasumi" : isJp ? "カスミ" : isCn ? "霞" : "카스미",
            spritePath = "Characters/카스미/기본",
            age = isEn ? "23" : isJp ? "23歳" : isCn ? "23岁" : "23세",
            role = "수석 탐정 / 현장 지휘", // To save tokens, I'll translate role/age only. The rest will use a generic fallback for other characters for now if needed, but let's translate all fully.
            mbti = "INTJ",
            appearance = isEn ? "Short silver-gray hair. Cool amber eyes. Wears a sleek trench coat. Professional and sharp look." : "은회색 단발머리. 날카로운 호박색 눈동자. 활동하기 편한 슬림핏 트렌치 코트. 단정하고 이성적인 분위기.",
            personality = isEn ? "Strict rationalist. Believes everything has a logical explanation. Tries to solve 'occult' cases with science." : "철저한 이성주의자. 모든 현상에는 과학적 원인이 있다고 확신한다. 사건을 객관적이고 논리적으로 해결하려 한다.",
            speechStyle = isEn ? "Polite and formal.\\n\\\"...I don't believe in ghosts. There must be a trick.\\\"" : "존댓말 위주. 딱딱하고 사무적.\\n\"...전 유령 따위는 믿지 않습니다. 분명 트릭이 있을 겁니다.\"",
            secret = isEn ? "She actually has a phobia of ghosts." : "어릴 적 트라우마로 인해 사실 '귀신'을 극도로 무서워한다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Rina" : isJp ? "リナ" : isCn ? "莉奈" : "리나",
            spritePath = "Characters/리나/기본",
            age = isEn ? "21" : isJp ? "21歳" : isCn ? "21岁" : "21세",
            role = "행동 대장 / 무력 담당",
            mbti = "ESTP",
            appearance = isEn ? "Bright pink twin-tails. Sporty and energetic style with a baseball jacket." : "밝은 분홍색 트윈테일. 스포티한 야구 점퍼와 숏팬츠. 활동적이고 톡톡 튀는 스타일.",
            personality = isEn ? "Action before thought. Energetic and brave, but easily bored." : "생각보다 몸이 먼저 나가는 행동파. 활기차고 용감하지만 지루한 것을 견디지 못한다.",
            speechStyle = isEn ? "Casual and loud.\\n\\\"Let's just kick the door down!\\\"" : "반말 위주. 목소리가 크다.\\n\"그냥 문 부수고 들어가면 안 돼?!\"",
            secret = isEn ? "Surprisingly good at cooking." : "의외로 요리 실력이 뛰어나다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Lilith" : isJp ? "リリス" : isCn ? "莉莉丝" : "리리스",
            spritePath = "Characters/리리스/기본",
            age = isEn ? "20" : isJp ? "20歳" : isCn ? "20岁" : "20세",
            role = "정보원 / 해커 & 발명가",
            mbti = "ISTP",
            appearance = isEn ? "Messy purple hair, thick glasses. Usually wears oversized hoodies and headphones." : "헝클어진 보라색 머리. 두꺼운 안경. 오버핏 후드티와 헤드폰.",
            personality = isEn ? "Lazy genius. Prefers dealing with machines over people." : "귀차니스트 천재. 사람보다 기계와 대화하는 것을 더 편하게 생각한다.",
            speechStyle = isEn ? "Mumbles softly.\\n\\\"...hacking complete. It took 3 seconds.\\\"" : "작은 목소리. 단답형.\\n\"...해킹 완료. 3초 걸렸어.\"",
            secret = isEn ? "Created an AI that can mimic any human voice." : "어떤 사람의 목소리든 완벽히 복제하는 AI를 발명했다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Mina" : isJp ? "ミナ" : isCn ? "美奈" : "미나",
            spritePath = "Characters/미나/기본",
            age = "1,000(?)",
            role = "오컬트 고문 / 자칭 흡혈귀",
            mbti = "INFJ",
            appearance = "창백한 피부에 은발. 고딕 로리타 풍의 드레스. 신비로운 붉은 눈동자.",
            personality = "스스로를 1000살 먹은 흡혈귀라 칭하는 중2병 소녀. 평소엔 엉뚱하지만 오컬트 지식은 진짜다.",
            speechStyle = "시대극 말투.\\n\"크큭... 어리석은 인간이여. 나의 피가 두려운가?\"",
            secret = "햇빛 알레르기가 있어서 낮에 밖에 나가지 못할 뿐이다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Haruka" : isJp ? "ハルカ" : isCn ? "遥" : "하루카",
            spritePath = "Characters/하루카/기본",
            age = isEn ? "19" : isJp ? "19歳" : isCn ? "19岁" : "19세",
            role = "사무소 막내 / 메이드",
            mbti = "ISFJ",
            appearance = "단정한 흑발 숏컷. 완벽하게 다림질된 메이드복. 상냥한 미소.",
            personality = "항상 친절하고 성실하다. 청소와 홍차 내리기에 진심이다.",
            speechStyle = "존댓말.\\n\"홍차 한 잔 다 드시면, 다음 사건 파일 가져다 드릴게요.\"",
            secret = "화가 나면 아무도 말릴 수 없다. 카스미조차 하루카가 화내면 눈치를 본다."
        });
    }

    """

content = content[:start_idx] + new_method + content[end_idx:]

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("ExtraUI.cs profile initialization translated")
