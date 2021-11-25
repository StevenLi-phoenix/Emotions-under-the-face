# author: StevenLi 李树雨
# time: 2021.11.25

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import json
import random
from PIL import Image, ImageTk


class drawHalfFace():
    def __init__(self):
        self.i = 32
        # read picture
        self.pic = plt.imread("img/base.jpg")
        with open("colorDictionary.json", "r") as f:
            self.colorDictionary = json.loads(f.read())
        with open("colorRanging.json", "r") as f:
            self.colorRanging = np.array(json.loads(f.read()))
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

    def submit_word():
        global photo
        label_text.configure(text=f"Remaining:{len(c.co)} pixels")
        if len(c.co) == 0:
            label_text.configure(text=f"Remaining:{len(c.co)} pixels\nNo available pixels")
            c.savePicture()
            raise ValueError(f"Index out of range: length{len(c.co)}")
        for input_text_value in input_text.get():
            print(input_text_value)
            if input_text_value in c.colorDictionary.keys():
                color = c.colorDictionary[input_text_value]
                c.targetColorFill(color)
            else:
                c.randomColorFill()
        photo = ImageTk.PhotoImage(Image.fromarray(c.pic).resize((800, 600)))
        label_img.configure(image=photo)
        # label_img.image = photo
        # root.update()


    # ------------------- tkinter GUI config start -------------------
    root = tk.Tk()
    root.title("Demo: pictureFullFill")
    photo = ImageTk.PhotoImage(Image.fromarray(c.pic).resize((800, 600)))
    colorChoose = tk.Listbox(root)
    colorChoose.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)
    for item in c.colorRanging:
        colorChoose.insert(tk.END, item)
    label_img = tk.Label(root, image=photo)
    label_img.grid(row=0, column=1, columnspan=5)
    label_text = tk.Label(root, text="Place text")
    label_text.grid(row=0, column=1, sticky=tk.NW)
    input_text = tk.Entry(root)
    input_text.grid(row=1, column=1, columnspan=4, sticky=tk.NSEW)
    button_submit = tk.Button(root, text="submit", command=submit_word)
    button_submit.grid(row=1, column=5, sticky=tk.NSEW)
    # ------------------- tkinter GUI config end   -------------------
    # mainloop update
    root.mainloop()
