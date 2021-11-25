# author: StevenLi 李树雨
# time: 2021.11.25

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import json
import random
from PIL import Image, ImageTk
import platform

if platform.system() == "Darwin":
    from tkmacosx import Button as MacButton


class drawHalfFace():
    def __init__(self):
        self.i = 32
        # read picture
        self.pic = plt.imread("img/base.jpg")
        with open("colorDictionary.json", "r") as f:
            self.colorDictionary = json.loads(f.read())
        with open("basicColorDictionary.json", "r") as f:
            self.basicColorDictionary = json.loads(f.read())
        # test argument
        self.pic[0, 0, :] = [255, 255, 255]

        self.canDraw = np.sum(255 == self.pic, axis=2) == 3
        self.shape = self.pic.shape
        self.co = []
        for row in range(0, self.shape[0], self.i):
            for col in range(0, self.shape[1], self.i):
                boundedArea = self.canDraw[row:(row + self.i if row + self.i < self.shape[0] else self.shape[0]),
                              col:(col + self.i if col + self.i < self.shape[1] else self.shape[1])]
                if True in boundedArea:
                    self.co.append((row, col))
        # Draw Grids

    def randomColorFill(self):
        target = random.choice(self.co)
        self.co.remove(target)
        colorCode = [random.randint(0, 255) for i in range(3)]
        for row in range(self.i):
            for col in range(self.i):
                if [255, 255, 255] in self.pic[target[0] + row, target[1] + col, :]:
                    self.pic[target[0] + row, target[1] + col, :] = colorCode

    def targetColorFill(self, color):
        """
        Fill ramdom place with target color set
        :param color: [r, g, b] list
        :return: None
        """
        print(color)
        target = random.choice(self.co)
        self.co.remove(target)
        colorCode = color
        for row in range(self.i):
            for col in range(self.i):
                if [255, 255, 255] in self.pic[target[0] + row, target[1] + col, :]:
                    self.pic[target[0] + row, target[1] + col, :] = colorCode

    def displayPicture(self):
        plt.imshow(self.pic)

    def savePicture(self):
        plt.imsave("output.jpg", self.pic)

    def saveCheckPoint(self):
        path = "npy/"
        np.save(f"{path}self.pic.npy", self.pic)
        np.save(f"{path}self.co.npy", self.co)
        np.save(f"{path}self.canDraw.npy", self.canDraw)


if __name__ == '__main__':
    c = drawHalfFace()


    # todo: 从检查点恢复数据

    def submit_word(Event = None):
        global photo
        label_text.configure(text=f"Remaining:{len(c.co)} pixels")
        if len(c.co) == 0:
            label_text.configure(text=f"Remaining:{len(c.co)} pixels\nNo available pixels")
            c.savePicture()
            raise ValueError(f"Index out of range: length{len(c.co)}")
        input_text_values = input_text.get()
        print(input_text_values)
        if input_text_values != "":
            if input_text_values[0]=="#":
                c.targetColorFill([int(input_text_values[1:3],16),int(input_text_values[3:5],16),int(input_text_values[5:7],16)])
            else:
                for input_text_value in input_text_values:
                    if input_text_value in c.colorDictionary.keys():
                        color = c.colorDictionary[input_text_value]
                        c.targetColorFill(color)
                    else:
                        c.randomColorFill()
        else:
            c.randomColorFill()
        photo = ImageTk.PhotoImage(Image.fromarray(c.pic).resize((800, 600)))
        label_img.configure(image=photo)
        # label_img.image = photo
        # root.update()

    def updateInputText(color):
        input_text.delete(0,"end")
        input_text.insert(0, color)

    # ------------------- tkinter GUI config start -------------------
    root = tk.Tk()
    root.title("Demo: pictureFullFill")
    photo = ImageTk.PhotoImage(Image.fromarray(c.pic).resize((800, 600)))

    colorSelector = tk.Frame(root)
    colorSelector.grid(row=0, column=0, sticky=tk.NSEW)
    colorBoard = []
    colorStorages = []
    colorDictionaryKeys = list(c.colorDictionary.keys())
    for i in range(len(c.basicColorDictionary)):
        sub_key = list(c.basicColorDictionary.keys())[i]
        sub_text = tk.Text(colorSelector, height=2, width=20)
        sub_text.insert("insert", sub_key)
        sub_text.grid(row=i, column=0)
        colorSeries = []
        r_limite, g_limite, b_limite = c.basicColorDictionary[sub_key]
        rL = [i for i in range(r_limite, 255, int((254 - r_limite) // 9))]
        gL = [i for i in range(g_limite, 255, int((254 - g_limite) // 9))]
        bL = [i for i in range(b_limite, 255, int((254 - b_limite) // 9))]
        for f in range(min(len(rL), len(gL), len(bL))-1):
            r, g, b = rL[f], gL[f], bL[f]
            sub_color = "#%02x%02x%02x" % (r, g, b)
            if platform.system() == "Darwin":
                sub_button = MacButton(colorSelector, text=f"{c.colorDictionary[str((r,g,b))] if str((r, g, b)) in colorDictionaryKeys else sub_color}", command=lambda ccommand=sub_color:updateInputText(ccommand), bg=sub_color, fg="black", highlightbackground=sub_color,width=50)
            else:
                sub_button = tk.Button(colorSelector, text=f"{c.colorDictionary[str((r,g,b))] if str((r, g, b)) in colorDictionaryKeys else sub_color}", command=lambda ccommand=sub_color:updateInputText(ccommand), bg=sub_color, fg="black", highlightbackground=sub_color,width=50)
            sub_button.grid(row=i, column=9 - f)
            colorStorages.append(str((r,g,b)))
            colorSeries.append(sub_button)
        colorBoard.append(colorSeries)

    label_img = tk.Label(root, image=photo)
    label_img.grid(row=0, column=1, columnspan=5)
    label_text = tk.Label(root, text="Place text")
    label_text.grid(row=0, column=1, sticky=tk.NW)
    input_text = tk.Entry(root)
    input_text.grid(row=1, column=1, columnspan=4, sticky=tk.NSEW)
    button_submit = tk.Button(root, text="submit", command=submit_word)
    button_submit.grid(row=1, column=5, sticky=tk.NSEW)
    root.bind('<Return>', submit_word)
    with open("colorStorages.json", "w") as f:
        f.write(json.dumps(colorStorages))
    # ------------------- tkinter GUI config end   -------------------
    # mainloop update
    root.mainloop()
