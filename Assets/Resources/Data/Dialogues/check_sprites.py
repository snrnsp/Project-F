import json, os
files = ["ch0_origin.json", "ch0_gathering.json", "ch0_opening.json", "ch1_morning.json", "ch1_night.json", "ch1_investigation_talk.json", "ch1_result_perfect.json", "ch1_resolution.json", "ch1_epilogue.json", "ch1_result_fail.json"]

with open("sprite_report.txt", "w", encoding="utf-8") as out:
    for f in files:
        if not os.path.exists(f): continue
        with open(f, "r", encoding="utf-8-sig") as fin:
            d = json.load(fin)
            out.write("\n# " + f + "\n")
            bg = None
            for n in d.get("nodes", []):
                speaker = n.get("speaker", "")
                L = n.get("characterSpriteLeft", "")
                R = n.get("characterSpriteRight", "")
                curr_bg = n.get("backgroundSprite", "")
                
                if curr_bg:
                    if bg and curr_bg != bg:
                        out.write("Node " + str(n["id"]) + ": BG changed from " + bg + " to " + curr_bg + "\n")
                    bg = curr_bg
                
                if speaker and speaker != "NARRATOR" and "의뢰인" not in speaker and "어머니" not in speaker and "아버지" not in speaker:
                    if speaker not in L and speaker not in R:
                        out.write("Node " + str(n["id"]) + ": Speaker " + speaker + " is speaking but not on screen! L: " + L + " R: " + R + "\n")

