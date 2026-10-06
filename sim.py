def ComputeLayoutTargets(owner):
    result = [0.25, 0.5, 0.75]
    used = [s for s in range(3) if owner[s] is not None]
    if len(used) == 1: xs = [0.5]
    elif len(used) == 2: xs = [0.25, 0.75]
    else: xs = [0.20, 0.50, 0.80]
    for i in range(len(used)):
        result[used[i]] = xs[i]
    return result

active_pos = {"세이카": 0, "카스미": 2}
prev_owner = ["세이카", None, "카스미"]

new_owner = [None, "리나", None]
new_names = {"리나"}
prev_slot_of = {"세이카": 0, "카스미": 2}

targetX = ComputeLayoutTargets(new_owner)
print("Node 10 targetX:", targetX)

for s in range(3):
    name = new_owner[s]
    if name is not None:
        if name in prev_slot_of:
            print(f"Node 10: {name} stays at slot {s}")
        else:
            startX = targetX[s]
            startX = 1.5
            print(f"Node 10: {name} slides from {startX} to {targetX[s]}")

# Node 11
active_pos = {"리나": 1}
prev_owner = [None, "리나", None]
new_owner = ["카스미", "리나", "세이카"]
new_names = {"카스미", "리나", "세이카"}
prev_slot_of = {"리나": 1}

targetX11 = ComputeLayoutTargets(new_owner)
print("Node 11 targetX:", targetX11)

for s in range(3):
    name = new_owner[s]
    if name is not None:
        if name in prev_slot_of:
            from_slot = prev_slot_of[name]
            if from_slot != s:
                print(f"Node 11: {name} glides from slot {from_slot} to {s}")
            else:
                print(f"Node 11: {name} stays at slot {s} and moves to {targetX11[s]}")
        else:
            startX = targetX11[s]
            startX = 1.5 if targetX11[s] > 0.5 else -0.5
            print(f"Node 11: {name} slides from {startX} to {targetX11[s]}")
