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
        bool isJp = lang == HalloweenVN.Core.GameLanguage.Japanese;
        bool isCn = lang == HalloweenVN.Core.GameLanguage.ChineseSimplified || lang == HalloweenVN.Core.GameLanguage.ChineseTraditional;

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Seika" : isJp ? "セイカ" : isCn ? "星佳" : "세이카",
            spritePath = "Characters/세이카/기본",
            age = isEn ? "25" : isJp ? "25歳" : isCn ? "25岁" : "25세",
            role = isEn ? "Director / Management & Legal" : isJp ? "事務所所長 / 経営・法務担当" : isCn ? "事务所所长 / 经营与法务" : "사무소 소장 / 경영·법무 담당",
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
                        : isJp ? "タメ口中心。豪快に笑う方。\\n\\\"ふふっ、いい眺めじゃない？ネバーモアという名前にぴったりのインテリアね。\\\""
                        : isCn ? "多用平语。喜欢豪爽地大笑。\\n\\\"呵呵，看起来不错吧？这可是完美契合‘Nevermore’这个名字的室内装潢呢。\\\""
                        : "반말 위주. 호탕하게 웃는 편.\\n\\\"후훗, 보기 좋잖아? 네버모어라는 이름에 딱 맞는 인테리어지.\\\"",
            secret = isEn ? "The real reason she opened the agency: to uncover the truth behind an inexplicable incident she experienced in the past."
                   : isJp ? "事務所を開設した本当の理由：過去に自ら経験した不可解な事件の真相を解明するため。"
                   : isCn ? "开办事务所的真正原因：为了揭开自己过去经历过的一起无法解释的事件的真相。"
                   : "사무소를 차린 진짜 이유: 과거 자신이 경험한 설명할 수 없는 사건의 진상을 밝히기 위해."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Kasumi" : isJp ? "カスミ" : isCn ? "霞" : "카스미",
            spritePath = "Characters/카스미/기본",
            age = isEn ? "23" : isJp ? "23歳" : isCn ? "23岁" : "23세",
            role = isEn ? "Chief Detective / Field Command" : isJp ? "首席探偵 / 現場指揮" : isCn ? "首席侦探 / 现场指挥" : "수석 탐정 / 현장 지휘",
            mbti = "INTJ",
            appearance = isEn ? "Short silver-gray hair. Cool amber eyes. Wears a sleek trench coat. Professional and sharp look."
                       : isJp ? "銀灰色のボブヘア。鋭い琥珀色の瞳。動きやすいスリムフィットのトレンチコート。端正で理性的な雰囲気。"
                       : isCn ? "银灰色短发。锐利的琥珀色眼眸。穿着方便活动的修身风衣。端庄且理性的氛围。"
                       : "은회색 단발머리. 날카로운 호박색 눈동자. 활동하기 편한 슬림핏 트렌치 코트. 단정하고 이성적인 분위기.",
            personality = isEn ? "Strict rationalist. Believes everything has a logical explanation. Tries to solve cases objectively and logically."
                        : isJp ? "徹底した理性主義者。全ての現象には科学的な原因があると確信している。事件を客観的かつ論理的に解決しようとする。"
                        : isCn ? "彻底的理性主义者。坚信所有现象都有科学依据。试图客观且有逻辑地解决案件。"
                        : "철저한 이성주의자. 모든 현상에는 과학적 원인이 있다고 확신한다. 사건을 객관적이고 논리적으로 해결하려 한다.",
            speechStyle = isEn ? "Polite and formal.\\n\\\"...I don't believe in ghosts. There must be a trick.\\\""
                        : isJp ? "敬語中心。硬い事務的な話し方。\\n\\\"…私は幽霊など信じません。必ずトリックがあるはずです。\\\""
                        : isCn ? "主要使用敬语。生硬且公事公办。\\n\\\"……我不相信什么幽灵。这肯定是有诡计的。\\\""
                        : "존댓말 위주. 딱딱하고 사무적.\\n\\\"...전 유령 따위는 믿지 않습니다. 분명 트릭이 있을 겁니다.\\\"",
            secret = isEn ? "Due to childhood trauma, she is actually terrified of 'ghosts'. That is also the reason she became a detective."
                   : isJp ? "幼い頃のトラウマにより、実は「お化け」を極度に恐れている。探偵になった理由もそれである。"
                   : isCn ? "因为童年的心理阴影，其实极度害怕“鬼怪”。这也是她成为侦探的原因。"
                   : "어릴 적 트라우마로 인해 사실 '귀신'을 극도로 무서워한다. 탐정이 된 이유도 그것."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Rina" : isJp ? "リナ" : isCn ? "莉奈" : "리나",
            spritePath = "Characters/리나/기본",
            age = isEn ? "21" : isJp ? "21歳" : isCn ? "21岁" : "21세",
            role = isEn ? "Action Leader / Muscle" : isJp ? "行動隊長 / 武力担当" : isCn ? "行动队长 / 武力担当" : "행동 대장 / 무력 담당",
            mbti = "ESTP",
            appearance = isEn ? "Bright pink twin-tails. Sporty and energetic style with a baseball jacket and shorts."
                       : isJp ? "明るいピンク色のツインテール。スポーティなスタジャンとショートパンツ。活動的で個性的なスタイル。"
                       : isCn ? "明亮的粉色双马尾。运动风格的棒球夹克和短裤。充满活力且个性鲜明的风格。"
                       : "밝은 분홍색 트윈테일. 스포티한 야구 점퍼와 숏팬츠. 활동적이고 톡톡 튀는 스타일.",
            personality = isEn ? "Action before thought. Energetic and brave, but easily bored. Hates sitting still in the office the most."
                        : isJp ? "考えるより先に体が動く行動派。活発で勇敢だが、退屈なことが我慢できない。事務所でじっとしているのが一番嫌い。"
                        : isCn ? "身体比大脑先行动的行动派。活泼勇敢，但无法忍受无聊。最讨厌的就是乖乖待在事务所里。"
                        : "생각보다 몸이 먼저 나가는 행동파. 활기차고 용감하지만 지루한 것을 견디지 못한다. 사무소에 가만히 있는 것을 제일 싫어한다.",
            speechStyle = isEn ? "Casual and loud.\\n\\\"Can't we just kick the door down?!\\\""
                        : isJp ? "タメ口中心。声が大きい。\\n\\\"ただドアをぶっ壊して入っちゃダメ？！\\\""
                        : isCn ? "多用平语。嗓门很大。\\n\\\"直接把门砸开冲进去不行吗？！\\\""
                        : "반말 위주. 목소리가 크다.\\n\\\"그냥 문 부수고 들어가면 안 돼?!\\\"",
            secret = isEn ? "Surprisingly skilled at cooking. However, visually, she creates horrifying results."
                   : isJp ? "意外と料理の腕前は抜群。ただし、視覚的には非常に恐ろしい仕上がりになる。"
                   : isCn ? "出人意料地厨艺精湛。只不过，在视觉上会呈现出极其可怕的结果。"
                   : "의외로 요리 실력이 뛰어나다. 단, 시각적으로는 매우 끔찍한 결과물을 만들어낸다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Lilith" : isJp ? "リリス" : isCn ? "莉莉丝" : "리리스",
            spritePath = "Characters/리리스/기본",
            age = isEn ? "20" : isJp ? "20歳" : isCn ? "20岁" : "20세",
            role = isEn ? "Informant / Hacker & Inventor" : isJp ? "情報員 / ハッカー＆発明家" : isCn ? "情报员 / 黑客与发明家" : "정보원 / 해커 & 발명가",
            mbti = "ISTP",
            appearance = isEn ? "Messy purple hair, thick glasses. Usually wears oversized hoodies and headphones. Always has dark circles."
                       : isJp ? "ボサボサの紫髪。分厚い眼鏡。オーバーサイズのパーカーとヘッドホン。常にクマがある。"
                       : isCn ? "乱蓬蓬的紫色头发。厚重的眼镜。宽大的连帽衫和耳机。总是带着黑眼圈。"
                       : "헝클어진 보라색 머리. 두꺼운 안경. 오버핏 후드티와 헤드폰. 항상 다크서클이 있다.",
            personality = isEn ? "Lazy genius. Prefers dealing with machines over people. Has a hobby of giving 'names' to machines."
                        : isJp ? "めんどくさがり屋の天才。人より機械と話す方が楽だと考えている。機械に「名前」をつける趣味がある。"
                        : isCn ? "怕麻烦的天才。比起和人交流，觉得和机器说话更轻松。有给机器“起名字”的爱好。"
                        : "귀차니스트 천재. 사람보다 기계와 대화하는 것을 더 편하게 생각한다. 기계에 '이름'을 붙여주는 취미가 있다.",
            speechStyle = isEn ? "Mumbles softly. Short answers.\\n\\\"...hacking complete. It took 3 seconds.\\\""
                        : isJp ? "声が小さい。短答型。\\n\\\"…ハッキング完了。3秒かかった。\\\""
                        : isCn ? "声音很小。回答简短。\\n\\\"……黑客入侵完毕。花了3秒。\\\""
                        : "작은 목소리. 단답형.\\n\\\"...해킹 완료. 3초 걸렸어.\\\"",
            secret = isEn ? "Created an AI that can perfectly mimic any human voice. She uses it when she is too lazy to answer."
                   : isJp ? "どんな人の声でも完全に複製するAIを発明した。自分が返事をするのが面倒な時に使う。"
                   : isCn ? "发明了一个能完美复制任何人声音的AI。在自己懒得回答时使用。"
                   : "어떤 사람의 목소리든 완벽히 복제하는 AI를 발명했다. 자신이 대답하기 귀찮을 때 쓴다."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Mina" : isJp ? "ミナ" : isCn ? "美奈" : "미나",
            spritePath = "Characters/미나/기본",
            age = isEn ? "1,000(?)" : isJp ? "1,000歳(?)" : isCn ? "1,000岁(?)" : "1,000세(?)",
            role = isEn ? "Occult Advisor / Self-proclaimed Vampire" : isJp ? "オカルト顧問 / 自称吸血鬼" : isCn ? "神秘学顾问 / 自称吸血鬼" : "오컬트 고문 / 자칭 흡혈귀",
            mbti = "INFJ",
            appearance = isEn ? "Pale skin and silver hair. Gothic Lolita style dress. Mysterious red eyes."
                       : isJp ? "青白い肌に銀髪。ゴスロリ風のドレス。神秘的な赤い瞳。"
                       : isCn ? "苍白的皮肤与银发。哥特洛丽塔风格的洋装。神秘的红色眼眸。"
                       : "창백한 피부에 은발. 고딕 로리타 풍의 드레스. 신비로운 붉은 눈동자.",
            personality = isEn ? "A girl with Chuunibyou who claims to be a 1000-year-old vampire. Her occult knowledge, however, is real."
                        : isJp ? "自らを1000歳の吸血鬼と称する中二病の少女。普段は突飛だがオカルトの知識は本物。"
                        : isCn ? "自称是活了1000岁的吸血鬼的中二病少女。平时古灵精怪，但神秘学知识是货真价实的。"
                        : "스스로를 1000살 먹은 흡혈귀라 칭하는 중2병 소녀. 평소엔 엉뚱하지만 오컬트 지식은 진짜다.",
            speechStyle = isEn ? "Theatrical and archaic.\\n\\\"Hehe... Foolish human. Do you fear my blood?\\\""
                        : isJp ? "時代劇口調。\\n\\\"くくっ…愚かな人間よ。我の血が恐ろしいか？\\\""
                        : isCn ? "古装剧腔调。\\n\\\"呵呵……愚蠢的人类。你害怕我的血吗？\\\""
                        : "시대극 말투.\\n\\\"크큭... 어리석은 인간이여. 나의 피가 두려운가?\\\"",
            secret = isEn ? "She just has a sunlight allergy and can't go out during the day. Actually loves garlic (Aglio e Olio fanatic)."
                   : isJp ? "日光アレルギーがあるため昼間に外に出られないだけ。実はニンニクが好き（アーリオ・オーリオマニア）。"
                   : isCn ? "只是因为有阳光过敏症所以白天没法出门。实际上很喜欢大蒜（蒜香意面狂热者）。"
                   : "햇빛 알레르기가 있어서 낮에 밖에 나가지 못할 뿐이다. 사실 마늘은 좋아한다(알리오 올리오 매니아)."
        });

        profiles.Add(new CharacterProfile
        {
            name = isEn ? "Haruka" : isJp ? "ハルカ" : isCn ? "遥" : "하루카",
            spritePath = "Characters/하루카/기본",
            age = isEn ? "19 (Youngest)" : isJp ? "19歳(最年少)" : isCn ? "19岁(最年少)" : "19세(최연소)",
            role = isEn ? "Agency Junior / Maid" : isJp ? "事務所の末っ子 / メイド" : isCn ? "事务所老幺 / 女仆" : "사무소 막내 / 메이드",
            mbti = "ISFJ",
            appearance = isEn ? "Neat black short hair. Perfectly ironed maid outfit. Gentle smile."
                       : isJp ? "端正な黒髪のショートカット。完璧にアイロンがけされたメイド服。優しい微笑み。"
                       : isCn ? "端庄的黑色短发。熨烫得完美无瑕的女仆装。温柔的微笑。"
                       : "단정한 흑발 숏컷. 완벽하게 다림질된 메이드복. 상냥한 미소.",
            personality = isEn ? "Always kind and diligent. Serious about cleaning and brewing tea."
                        : isJp ? "常に親切で誠実。掃除と紅茶を淹れることに全力を注ぐ。"
                        : isCn ? "总是亲切又认真。对打扫和泡红茶十分投入。"
                        : "항상 친절하고 성실하다. 청소와 홍차 내리기에 진심이다.",
            speechStyle = isEn ? "Polite.\\n\\\"Once you finish your tea, I'll bring you the next case file.\\\""
                        : isJp ? "敬語。\\n\\\"紅茶を飲み終えられましたら、次の事件ファイルをお持ちしますね。\\\""
                        : isCn ? "使用敬语。\\n\\\"等您喝完这杯红茶，我就把下一份案件档案给您拿来。\\\""
                        : "존댓말.\\n\\\"홍차 한 잔 다 드시면, 다음 사건 파일 가져다 드릴게요.\\\"",
            secret = isEn ? "Unstoppable when angry. Even Kasumi walks on eggshells when Haruka is mad."
                   : isJp ? "怒ると誰も止められない。カスミでさえハルカが怒ると顔色を伺う。"
                   : isCn ? "一旦生气起来谁也拦不住。连霞在遥生气时也会看她的眼色。"
                   : "화가 나면 아무도 말릴 수 없다. 카스미조차 하루카가 화내면 눈치를 본다."
        });
    }
    """

content = content[:start_idx] + new_method + content[end_idx:]

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("ExtraUI.cs fully localized in EN, JP, CN, KO")
