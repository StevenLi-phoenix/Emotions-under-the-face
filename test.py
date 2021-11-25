import json
import tkinter as yk

root = tk.TK()
colorDictionary = {"文字信息":[255,255,255],
"文字信息":[255,255,255],
"文字信息":[255,255,255],
"文字信息":[255,255,255],
"文字信息":[255,255,255],
"文字信息":[255,255,255],
"文字信息":[255,255,255],
"文字信息":[255,255,255],
"文字信息":[255,255,255],
}
with open("colorDictionary.json", "w") as f:
    f.write(json.dumps(colorDictionary))