import json

colorList = []
for r in range(0,257,32):
    for g in range(0,257,32):
        for b in range(0,257,32):
            colorList.append((r,g,b))
with open("colorRanging.json", "w") as f:
    f.write(json.dumps(colorList))
