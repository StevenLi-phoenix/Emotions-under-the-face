import json

colorDictionary = {
    str((101, 73, 134)): "焦虑",
    str((206, 25, 0)): "力量",
    str((51, 51, 0)): "恶心",
    str((195, 243, 181)): "青春",
    str((216, 255, 21)): "支持",
    str((4, 0, 148)): "悲痛",
    str((148, 148, 148)): "无感",
    str((252, 229, 54)): "不安",
    str((227, 224, 227)): "沙雕",
}
basicColorDictionary = {
    "Red": [165, 8, 22],
    "Pink": [168, 45, 38],
    "Purple": [67, 31, 134],
    "Deep Purple": [43, 35, 140],
    "Indigo": [26, 39, 121],
    "Blue": [29, 73, 156],
    "Light Blue": [32, 88, 153],
    "Cyan": [39, 95, 99],
    "Teal": [26, 75, 64],
    "Green": [48, 92, 40],
    "Light Green": [65, 103, 41],
    "Yellow": [223, 117, 48],
    "Light Yellow": [230, 131, 55],
    "Orange": [213, 90, 38],
    "Deep Orange": [176, 65, 31],
    "Grey": [33, 33, 33],
    "Blue Grey": [41, 50, 55],
    "Brown": [59, 40, 35],
}
textColorDictionary = {
    "焦虑": (101, 73, 134),
    "力量": (206, 25, 0),
    "恶心": (51, 51, 0),
    "青春": (195, 243, 181),
    "支持": (216, 255, 21),
    "悲痛": (4, 0, 148),
    "无感": (148, 148, 148),
    "不安": (252, 229, 54),
}

with open("colorDictionary.json", "w") as f:
    f.write(json.dumps(colorDictionary))
with open("basicColorDictionary.json", "w") as f:
    f.write(json.dumps(basicColorDictionary))
