import json
import tkinter
from tkinter import *
import tkmacosx

with open("colorStorages.json", "r") as f:
    colorStorages = json.loads(f.read())
with open("colorDictionary.json", "r") as f:
    colorDictionary = json.loads(f.read())

root = tkinter.Tk()
root.title("Demo: colorAliasConfig")
width,height = 800,450
root.geometry("%dx%d+30+30"%(width,height))
root.resizable(0,0)

canvas=Canvas(root,width=width,height=height,scrollregion=(0,0,width,height)) #创建canvas
canvas.place(x = 0, y = 0) #放置canvas的位置
frame=Frame(canvas) #把frame放在canvas里
frame.place(x=0, y=0, width=width, height=height) #frame的长宽，和canvas差不多的

vbar=Scrollbar(canvas,orient=VERTICAL) #竖直滚动条
vbar.place(x = width-20,width=20,height=height)
vbar.configure(command=canvas.yview)

hbar=Scrollbar(canvas,orient=HORIZONTAL)#水平滚动条
hbar.place(x =0,y=height-20,width=width,height=20)
hbar.configure(command=canvas.xview)

canvas.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set) #设置
canvas.create_window((800,450), window=frame)  #create_window

colorDictionaryKeys = list(colorDictionary.keys())
changeList = []
for i in range(len(colorStorages)):
    tkinter.Label(frame, text=colorStorages[i]).grid(row=i, column=0)
    r,g,b = (int(j) for j in colorStorages[i].replace("(","").replace(")","").split(","))
    tkinter.Label(frame, text=f"{colorDictionary[str((r,g,b))] if str((r,g,b)) in colorDictionaryKeys else None}", bg="#%02x%02x%02x" % (r,g,b), width=15).grid(row=i, column=1)
    InputText = tkinter.Entry(frame)
    InputText.grid(row=i, column=3)
    InputButtom = tkinter.Button(frame)
    InputButtom.grid(row=i, column=4)
    changeList.append([InputText, InputButtom])
frame.update()
tkinter.mainloop()