import json
from pathlib import Path


distance = 20
width = 10
height = 10

directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
offset = [200, 100]

data = {"nodes": [], "edges": []}

for y in range(height):
    for x in range(width):
        data["nodes"].append([offset[0] + x*distance, offset[1] + y*distance])
        data["edges"].append([])

for y in range(height):
    for x in range(width):
        for d in directions:
            pos = [x + d[0], y + d[1]]
            if 0 <= pos[0] and pos[0] < width and 0 <= pos[1] and pos[1] < height:
                data["edges"][y*width + x].append(pos[1] * width + pos[0])
            

with open(Path(__file__).parent / "body.json", "w") as file:
    json.dump(data, file, indent=2)