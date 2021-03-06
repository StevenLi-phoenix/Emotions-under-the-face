# author: StevenLi 李树雨
# time: 2021.12.2

import json
import platform
import random
import time
import tkinter as tk
import tkinter.messagebox as msg
from os.path import exists
from os import mkdir


import numpy as np
from PIL import Image, ImageTk

if platform.system() == "Darwin": # tkinter.Button has display error on mac so instead import another remade tkmacosx for replace
    from tkmacosx import Button as MacButton


class drawHalfFace():
    def __init__(self):
        # control
        self.i = 32 # matrix size
        loadColorDic = True # load "colorDictionary.json" ?
        self.colorDictDefaultValue = "default" # "default" or any str
        self.printLog = False # whether print logs
        self.pictureResizeWidth = 800 # resized picture height (mainly caused by picture too big or too small
        self.pictureResizeHeight = 600 # resized picture weight (mainly caused by picture too big or too small
        self.picturePath = "img/base.jpg" # picture path
        self.npyPath = "npy/" # saved & load npy files path
        self.colorDictionaryPath = "colorDictionary.json" # load "colorDictionary.json" path
        self.basicColorDictionaryPath = "basicColorDictionary.json" # load "basicColorDictionary.json" path
        self.drawGrid = False # whether draw grids
        gridColor = (0,0,0) # the color of grid

        # read picture
        self.pic = np.array(Image.open(self.picturePath))
        if loadColorDic:
            try:
                with open(self.colorDictionaryPath, "r") as f:
                    self.colorDictionary = json.loads(f.read())
            except Exception as e:
                if self.printLog: print(f"Read file: {self.colorDictionaryPath} failed\n{e}")
                self.colorDictionary = {}
        else:
            self.colorDictionary = {}
        try:
            with open(self.basicColorDictionaryPath, "r") as f:
                self.basicColorDictionary = json.loads(f.read())
        except Exception as e:
            if self.printLog: print(f"Read file: {self.basicColorDictionaryPath} failed\n{e}")
            self.colorDictionary = {}
        self.textColorDictionary = dict(zip(self.colorDictionary.values(), self.colorDictionary.keys()))
        self.canDraw = np.sum(255 == self.pic, axis=2) == 3
        self.shape = self.pic.shape
        self.co = []
        for row in range(0, self.shape[0], self.i):
            for col in range(0, self.shape[1], self.i):
                boundedArea = self.canDraw[row:(row + self.i if row + self.i < self.shape[0] else self.shape[0]),
                              col:(col + self.i if col + self.i < self.shape[1] else self.shape[1])]
                if True in boundedArea:
                    self.co.append((row, col))
                if self.drawGrid:
                    for indexR in range(0, self.shape[0]):
                        if self.canDraw[indexR, col]:
                            self.pic[indexR, col] = gridColor
            if self.drawGrid:
                for indexC in range(0, self.shape[0]):
                    if self.canDraw[row, indexC]:
                        self.pic[row, indexC] = gridColor
        # todo: Draw Grids

    def randomColorFill(self):
        colorCode = [random.randint(0, 255) for i in range(3)]
        self.targetColorFill(colorCode)

    def targetColorFill(self, color):
        """
        Fill ramdom place with target color set
        :param color: [r, g, b] list
        :return: None
        """
        target = random.choice(self.co)
        self.co.remove(target)
        if self.printLog:print(color, "@", target)
        colorCode = color
        for row in range(self.i if self.i < self.shape[0] else self.shape[0]):
            for col in range(self.i if self.i < self.shape[1] else self.shape[1]):
                if [255, 255, 255] in self.pic[target[0] + row if target[0] + row < self.shape[0] else self.shape[0],
                                      target[1] + col if target[1] + col < self.shape[1] - 1 else self.shape[1] - 1, :]:
                    self.pic[target[0] + row if target[0] + row < self.shape[0] else self.shape[0],
                    target[1] + col if target[1] + col < self.shape[1] - 1 else self.shape[1] - 1, :] = colorCode
                    if self.printLog:print(f"\rProgressing row: {row}\tcol:{col}\tto:{colorCode}", end="")
        if self.printLog:print(f"\rProgressing Done")

    def fillAllBlack(self, colorCode=None):
        if self.printLog: print("Test method start: printing all black")
        if colorCode is None:
            colorCode = [0, 0, 0]
        for target in self.co:
            for row in range(self.i):
                for col in range(self.i):
                    if [255, 255, 255] in self.pic[target[0] + row, target[1] + col, :]:
                        self.pic[target[0] + row, target[1] + col, :] = colorCode
        self.co.clear()

    def savePicture(self):
        Image.fromarray(self.pic).save("img/output.png", format="png")

    def saveCheckPoint(self):
        if not exists(self.npyPath):mkdir(self.npyPath)
        with open(f"{self.npyPath}self.co.list", "w") as f:
            f.write(json.dumps(self.co))
        np.save(f"{self.npyPath}self.pic.npy", self.pic)
        np.save(f"{self.npyPath}self.canDraw.npy", self.canDraw)

    def loadCheckPoint(self):
        with open(f"{self.npyPath}self.co.list", "r") as f:
            self.co = json.loads(f.read())
        self.pic = np.load(f"{self.npyPath}self.pic.npy")
        self.canDraw = np.load(f"{self.npyPath}self.canDraw.npy")


class timer():
    def __init__(self):
        self.time_recored = 0
        self.timeList = []
        self.accTime = time.time()

    def start(self):
        self.time_recored = time.time()
        return self

    def recored(self, name=None):
        self.timeList.append(
            f"ABS:{'{:.10f}'.format(time.time() - self.time_recored)},\t ACC:{'{:.10f}'.format(time.time() - self.accTime, 10)},\t {name}")
        self.accTime = time.time()

    def __str__(self):
        return "\n".join(self.timeList)

    def stop(self):
        print(str(self))
        return str(self)


if __name__ == '__main__':
    c = drawHalfFace()


    def submit_word(_=None):
        global photo
        label_text.configure(text=f"Remaining:{len(c.co)} pixels")
        if len(c.co) == 0:
            label_text.configure(text=f"Remaining:{len(c.co)} pixels\nNo available pixels")
            c.savePicture()
            raise ValueError(f"Index out of range: length{len(c.co)}")
        input_text_values = input_text.get()
        print(input_text_values)
        if input_text_values != "":
            if input_text_values[0] == "#":
                c.targetColorFill(
                    [int(input_text_values[1:3], 16), int(input_text_values[3:5], 16), int(input_text_values[5:7], 16)])
            elif "test" in input_text_values:
                c.fillAllBlack()
            elif "load" in input_text_values:
                c.loadCheckPoint()
            elif "help" in input_text_values or "h" == input_text_values:
                msg.showinfo("HELP",
                             "test: See all available pixels.\nload: load last auto checkpoint\nSelect colors on the left columns and click submit or enter to fill colors on her face.")
            elif "copyright" in input_text_values or "author" in input_text_values:
                msg.showinfo("COPYRIGHTS", "All rights reserved, Author: 李树雨StevenLi")
            elif input_text_values in c.textColorDictionary.keys():
                print([int(i) for i in c.textColorDictionary[input_text_values][1:-1].split(",")])
                c.targetColorFill([int(i) for i in c.textColorDictionary[input_text_values][1:-1].split(",")])

            else:
                c.randomColorFill()
        else:
            c.randomColorFill()
        c.saveCheckPoint()
        photo = ImageTk.PhotoImage(Image.fromarray(c.pic).resize((c.pictureResizeWidth, c.pictureResizeHeight)))
        label_img.configure(image=photo)
        label_img.update()


    def updateInputText(color):
        input_text.delete(0, "end")
        input_text.insert(0, color)


    def updatePciture():
        global photo
        while True:
            photo = ImageTk.PhotoImage(Image.fromarray(c.pic).resize((c.pictureResizeWidth, c.pictureResizeHeight)))


    # ------------------- tkinter GUI config start -------------------
    # msg.showinfo("Info", "Author: StevenLi李树雨\nCopyrights all rights reserve.")
    root = tk.Tk()
    root.title("Demo: pictureFullFill\t\tAuthor: StevenLi李树雨 - all rights reserve.")
    photo = ImageTk.PhotoImage(Image.fromarray(c.pic).resize((c.pictureResizeWidth, c.pictureResizeHeight)))
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
        r_limite, g_limite, b_limite = c.basicColorDictionary[str(sub_key)]
        rL = [i for i in range(r_limite, 255, int((254 - r_limite) // 9))]
        gL = [i for i in range(g_limite, 255, int((254 - g_limite) // 9))]
        bL = [i for i in range(b_limite, 255, int((254 - b_limite) // 9))]
        for f in range(min(len(rL), len(gL), len(bL)) - 1):
            r, g, b = rL[f], gL[f], bL[f]
            sub_color = "#%02x%02x%02x" % (r, g, b)
            if c.colorDictDefaultValue == "default":
                sub_button_text = str(sub_color)
            else:
                sub_button_text = c.colorDictDefaultValue
            if platform.system() == "Darwin":
                sub_button = MacButton(colorSelector,
                                       text=f"{c.colorDictionary[str((r, g, b))] if str((r, g, b)) in colorDictionaryKeys else sub_button_text}",
                                       command=lambda ccommand=sub_color: updateInputText(ccommand), bg=sub_color,
                                       fg="black", highlightbackground=sub_color, width=50)
            else:
                sub_button = tk.Button(colorSelector,
                                       text=f"{c.colorDictionary[str((r, g, b))] if str((r, g, b)) in colorDictionaryKeys else sub_button_text}",
                                       command=lambda ccommand=sub_color: updateInputText(ccommand), bg=sub_color,
                                       fg="black", highlightbackground=sub_color, width=5)
            sub_button.grid(row=i, column=9 - f)
            colorStorages.append(str((r, g, b)))
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
    # ------------------- tkinter GUI config end   -------------------
    # mainloop update
    root.mainloop()
