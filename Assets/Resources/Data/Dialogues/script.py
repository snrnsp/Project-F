import json, os
files = ["ch0_origin.json", "ch0_gathering.json", "ch0_opening.json", "ch1_morning.json", "ch1_night.json", "ch1_investigation_talk.json", "ch1_result_perfect.json", "ch1_resolution.json", "ch1_epilogue.json", "ch1_result_fail.json"]
with open("dump.txt", "w", encoding="utf-8") as fout:
    for f in files:
        if os.path.exists(f):
            with open(f, encoding="utf-8-sig") as fin:
                d = json.load(fin)
                fout.write("=== " + f + " ===\n")
                for n in d.get("nodes", []):
                    fout.write(str(n.get("nodeId")) + " | " + str(n.get("speakerName")) + " | CMD: " + str(n.get("command")) + " | NEXT: " + str(n.get("nextNodeId")) + " | TEXT: " + repr(n.get("text")) + "\n")

