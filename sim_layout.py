def compute(owner):
    result = [0.25, 0.5, 0.75]
    used = [s for s in range(3) if owner[s] is not None]
    if len(used) == 1: xs = [0.5]
    elif len(used) == 2: xs = [0.25, 0.75]
    else: xs = [0.2, 0.5, 0.8]
    for i, u in enumerate(used): result[u] = xs[i]
    return result

print("Node 9:")
print(compute(["세이카", None, "카스미"]))
print("Node 10:")
print(compute([None, "리나", None]))
print("Node 11:")
print(compute(["카스미", "리나", "세이카"]))
