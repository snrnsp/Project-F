import sys

path = 'F:/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

start_sig = "private void InitializeProfiles()"
end_sig = "public void RegisterFolder"

start_idx = content.find(start_sig)
end_idx = content.find(end_sig)

new_method = """private void InitializeProfiles()
    {
        profiles.Clear();
        var lang = HalloweenVN.Core.SettingsData.Language;
        bool isEn = lang == HalloweenVN.Core.GameLanguage.English;

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Seika" : "세이카",
            spritePath = "Characters/세이카/기본",
            age = isEn ? "25" : "25세",
            role = isEn ? "Director / Management & Legal" : "사무소 소장 / 경영·법무 담당",
            mbti = "ENTJ",
            appearance = isEn ? "Long dark navy hair flowing down to the waist with a gold hairpin. Clear, cold blue eyes. A sophisticated, urban look with a black long skirt, charcoal grey jacket, and a black shoulder bag." 
                              : "허리 아래까지 흘러내리는 짙은 남색 긴 머리카락에 금색 헤어핀. 맑고 차가운 파란 눈동자. 검은색 롱 스커트에 차콜 그레이 재킷, 검은 숄더백을 걸친 세련되고 도시적인 분위기.",
            personality = isEn ? "Founder and director of 'Nevermore Occult Detective Agency'. Charismatic and decisive, with a genuine passion for Halloween and the occult."
                               : "「네버모어 오컬트 탐정 사무소」의 설립자이자 소장. 카리스마가 있고 결단력이 빠르며, 할로윈과 오컬트에 진심으로 열광한다.",
            speechStyle = isEn ? "Mostly informal. Laughs heartily.\\n\\\"Fufu, looks good, doesn't it? An interior perfectly suited for the name Nevermore.\\\""
                               : "반말 위주. 호탕하게 웃는 편.\\n\\\"후훗, 보기 좋잖아? 네버모어라는 이름에 딱 맞는 인테리어지.\\\"",
            secret = isEn ? "The real reason she opened the agency: to uncover the truth behind an inexplicable incident she experienced in the past."
                          : "사무소를 차린 진짜 이유: 과거 자신이 경험한 설명할 수 없는 사건의 진상을 밝히기 위해."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Kasumi" : "카스미",
            spritePath = "Characters/카스미/기본",
            age = isEn ? "23" : "23세",
            role = isEn ? "Chief Detective / Field Command" : "수석 탐정 / 현장 지휘",
            mbti = "INTJ",
            appearance = isEn ? "Short silver-gray hair. Cool amber eyes. Wears a sleek trench coat. Professional and sharp look." 
                              : "은회색 단발머리. 날카로운 호박색 눈동자. 활동하기 편한 슬림핏 트렌치 코트. 단정하고 이성적인 분위기.",
            personality = isEn ? "Strict rationalist. Believes everything has a logical explanation. Tries to solve 'occult' cases with science." 
                               : "철저한 이성주의자. 모든 현상에는 과학적 원인이 있다고 확신한다. 사건을 객관적이고 논리적으로 해결하려 한다.",
            speechStyle = isEn ? "Polite and formal.\\n\\\"...I don't believe in ghosts. There must be a trick.\\\"" 
                               : "존댓말 위주. 딱딱하고 사무적.\\n\\\"...전 유령 따위는 믿지 않습니다. 분명 트릭이 있을 겁니다.\\\"",
            secret = isEn ? "Due to childhood trauma, she is actually terrified of 'ghosts'." : "어릴 적 트라우마로 인해 사실 '귀신'을 극도로 무서워한다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Rina" : "리나",
            spritePath = "Characters/리나/기본",
            age = isEn ? "21" : "21세",
            role = isEn ? "Action Leader / Muscle" : "행동 대장 / 무력 담당",
            mbti = "ESTP",
            appearance = isEn ? "Bright pink twin-tails. Sporty and energetic style with a baseball jacket and shorts." 
                              : "밝은 분홍색 트윈테일. 스포티한 야구 점퍼와 숏팬츠. 활동적이고 톡톡 튀는 스타일.",
            personality = isEn ? "Action before thought. Energetic and brave, but easily bored." 
                               : "생각보다 몸이 먼저 나가는 행동파. 활기차고 용감하지만 지루한 것을 견디지 못한다.",
            speechStyle = isEn ? "Casual and loud.\\n\\\"Can't we just kick the door down?!\\\"" 
                               : "반말 위주. 목소리가 크다.\\n\\\"그냥 문 부수고 들어가면 안 돼?!\\\"",
            secret = isEn ? "Surprisingly skilled at cooking." : "의외로 요리 실력이 뛰어나다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Lilith" : "리리스",
            spritePath = "Characters/리리스/기본",
            age = isEn ? "20" : "20세",
            role = isEn ? "Informant / Hacker & Inventor" : "정보원 / 해커 & 발명가",
            mbti = "ISTP",
            appearance = isEn ? "Messy purple hair, thick glasses. Usually wears oversized hoodies and headphones." 
                              : "헝클어진 보라색 머리. 두꺼운 안경. 오버핏 후드티와 헤드폰.",
            personality = isEn ? "Lazy genius. Prefers dealing with machines over people." 
                               : "귀차니스트 천재. 사람보다 기계와 대화하는 것을 더 편하게 생각한다.",
            speechStyle = isEn ? "Mumbles softly. Short answers.\\n\\\"...hacking complete. It took 3 seconds.\\\"" 
                               : "작은 목소리. 단답형.\\n\\\"...해킹 완료. 3초 걸렸어.\\\"",
            secret = isEn ? "Created an AI that can perfectly mimic any human voice." : "어떤 사람의 목소리든 완벽히 복제하는 AI를 발명했다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Mina" : "미나",
            spritePath = "Characters/미나/기본",
            age = isEn ? "1,000(?)" : "1,000세(?)",
            role = isEn ? "Occult Advisor / Self-proclaimed Vampire" : "오컬트 고문 / 자칭 흡혈귀",
            mbti = "INFJ",
            appearance = isEn ? "Pale skin and silver hair. Gothic Lolita style dress. Mysterious red eyes." 
                              : "창백한 피부에 은발. 고딕 로리타 풍의 드레스. 신비로운 붉은 눈동자.",
            personality = isEn ? "A girl with Chuunibyou who claims to be a 1000-year-old vampire. Her occult knowledge, however, is real." 
                               : "스스로를 1000살 먹은 흡혈귀라 칭하는 중2병 소녀. 평소엔 엉뚱하지만 오컬트 지식은 진짜다.",
            speechStyle = isEn ? "Theatrical and archaic.\\n\\\"Hehe... Foolish human. Do you fear my blood?\\\"" 
                               : "시대극 말투.\\n\\\"크큭... 어리석은 인간이여. 나의 피가 두려운가?\\\"",
            secret = isEn ? "She just has a sunlight allergy and can't go out during the day." : "햇빛 알레르기가 있어서 낮에 밖에 나가지 못할 뿐이다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Haruka" : "하루카",
            spritePath = "Characters/하루카/기본",
            age = isEn ? "19" : "19세",
            role = "사무소 막내 / 메이드", // Oops, let me just replace this in python string
            mbti = "ISFJ",
            appearance = "단정한 흑발 숏컷. 완벽하게 다림질된 메이드복. 상냥한 미소.",
            personality = "항상 친절하고 성실하다. 청소와 홍차 내리기에 진심이다.",
            speechStyle = "존댓말.\\n\"홍차 한 잔 다 드시면, 다음 사건 파일 가져다 드릴게요.\"",
            secret = "화가 나면 아무도 말릴 수 없다. 카스미조차 하루카가 화내면 눈치를 본다."
        });
    }

    """

# Replace the incomplete Haruka part
new_method = new_method.replace('role = "사무소 막내 / 메이드"', 'role = isEn ? "Agency Junior / Maid" : "사무소 막내 / 메이드"')
new_method = new_method.replace('appearance = "단정한 흑발 숏컷. 완벽하게 다림질된 메이드복. 상냥한 미소."', 'appearance = isEn ? "Neat black short hair. Perfectly ironed maid outfit. Gentle smile." : "단정한 흑발 숏컷. 완벽하게 다림질된 메이드복. 상냥한 미소."')
new_method = new_method.replace('personality = "항상 친절하고 성실하다. 청소와 홍차 내리기에 진심이다."', 'personality = isEn ? "Always kind and diligent. Serious about cleaning and brewing tea." : "항상 친절하고 성실하다. 청소와 홍차 내리기에 진심이다."')
new_method = new_method.replace('speechStyle = "존댓말.\\n\\"홍차 한 잔 다 드시면, 다음 사건 파일 가져다 드릴게요.\\""', 'speechStyle = isEn ? "Polite.\\n\\\"Once you finish your tea, I\'ll bring you the next case file.\\\"" : "존댓말.\\n\\\"홍차 한 잔 다 드시면, 다음 사건 파일 가져다 드릴게요.\\\""')
new_method = new_method.replace('secret = "화가 나면 아무도 말릴 수 없다. 카스미조차 하루카가 화내면 눈치를 본다."', 'secret = isEn ? "Unstoppable when angry. Even Kasumi walks on eggshells when Haruka is mad." : "화가 나면 아무도 말릴 수 없다. 카스미조차 하루카가 화내면 눈치를 본다."')

content = content[:start_idx] + new_method + content[end_idx:]

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("ExtraUI.cs profile initialization properly translated (English/Korean)")
