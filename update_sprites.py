import json
import os

file_path = "F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json"

with open(file_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

def sprite(char_name, expr):
    return f"Characters/{char_name}/{expr}" if char_name else ""

def get_layout(node_id):
    if 2 <= node_id <= 4: return ["리나", "카스미"]
    if 5 <= node_id <= 8: return ["리리스", "미나"]
    if 9 <= node_id <= 14: return ["하루카", "미나"]
    if 15 <= node_id <= 17: return ["카스미"]
    if 18 <= node_id <= 25: return ["리리스", "카스미", "리나"]
    if 26 <= node_id <= 28: return ["리리스", "하루카"]
    if 29 <= node_id <= 37: return ["세이카", "카스미"]
    if 38 <= node_id <= 40: return ["세이카", "리나"]
    if 41 <= node_id <= 44: return ["미나", "세이카"]
    if 45 <= node_id <= 50: return ["하루카", "세이카"]
    if 51 <= node_id <= 61: return ["하루카"]
    if 62 <= node_id <= 66: return ["리나", "카스미"]
    if 67 <= node_id <= 69: return ["미나"]
    if 70 <= node_id <= 79: return ["세이카", "카스미"]
    if 80 <= node_id <= 85: return ["리리스", "미나", "리나"]
    if 86 <= node_id <= 87: return ["리나", "세이카"]
    if 88 <= node_id <= 91: return ["하루카", "세이카"]
    return None

def get_expression(speaker, text, node_id):
    expr = "기본"
    if not text: return expr
    
    if "또...?!" in text: return "놀람"
    if "기다려요" in text: return "찡그림"
    if "모스 부호?!" in text: return "놀람"
    if "유령이 피아노로" in text: return "당황"
    if "보여. 누군가가 보여." in text: return "음침"
    if "젊은 여자야" in text: return "음침"
    if "무언가에 지독하게" in text: return "측은"
    if "저, 저요?!" in text: return "당황"
    if "알아요. 아무도" in text: return "측은"
    if "따뜻해요." in text: return "미소"
    if "이런 비과학적인" in text: return "측은"
    if "안심한 것이다." in text: return "측은"
    if "가장 따뜻한" in text: return "미소"
    if "주먹으로 때려서" in text: return "찡그림"
    if "반드시 이름까지" in text: return "찡그림"
    if "잊혀진 이들을" in text: return "기본"
    if "시간이 지나면" in text: return "측은"
    
    if speaker == "세이카":
        if "사라졌어" in text or "지워지고" in text: expr = "음침"
        if "구할 수는 없어" in text: expr = "측은"
    elif speaker == "미나":
        if "투명해져" in text or "지우는 것이다" in text: expr = "음침"
        if "안심한" in text or "따뜻한" in text: expr = "미소"
    elif speaker == "하루카":
        if "따뜻해요" in text or "여기 있어요" in text: expr = "미소"
        if "알아요" in text or "의미가 있었던" in text: expr = "측은"
    elif speaker == "카스미":
        if "비과학적인" in text: expr = "측은"
        if "의문입니다" in text: expr = "찡그림"
    elif speaker == "리나":
        if "주먹으로" in text: expr = "찡그림"
        
    return expr

changes = 0

for node in data["nodes"]:
    speaker = node.get("speaker", "").strip()
    node_id = node.get("id")
    text = node.get("text", "")
    
    if not speaker:
        continue
        
    s_left = node.get("characterSpriteLeft", "")
    s_center = node.get("characterSpriteCenter", "")
    s_right = node.get("characterSpriteRight", "")
    
    if s_left == "" and s_center == "" and s_right == "":
        layout = get_layout(node_id)
        if not layout:
            layout = [speaker]
            
        if speaker not in layout:
            if len(layout) < 3:
                layout.append(speaker)
            else:
                layout[1] = speaker
                
        pos = {"Left": "", "Center": "", "Right": ""}
        if len(layout) == 1:
            pos["Center"] = sprite(layout[0], get_expression(layout[0], text if layout[0] == speaker else "", node_id))
        elif len(layout) == 2:
            pos["Left"] = sprite(layout[0], get_expression(layout[0], text if layout[0] == speaker else "", node_id))
            pos["Right"] = sprite(layout[1], get_expression(layout[1], text if layout[1] == speaker else "", node_id))
        elif len(layout) >= 3:
            pos["Left"] = sprite(layout[0], get_expression(layout[0], text if layout[0] == speaker else "", node_id))
            pos["Center"] = sprite(layout[1], get_expression(layout[1], text if layout[1] == speaker else "", node_id))
            pos["Right"] = sprite(layout[2], get_expression(layout[2], text if layout[2] == speaker else "", node_id))
            
        node["characterSpriteLeft"] = pos["Left"]
        node["characterSpriteCenter"] = pos["Center"]
        node["characterSpriteRight"] = pos["Right"]
        
        changes += 1

print(f"Updated {changes} nodes.")

with open(file_path, "w", encoding="utf-8-sig") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
