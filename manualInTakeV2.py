import json
import tkinter.filedialog
from tkinter import *

# default data
colorStorages = ["(165, 8, 22)", "(174, 35, 47)", "(183, 62, 72)", "(192, 89, 97)", "(201, 116, 122)",
                 "(210, 143, 147)", "(219, 170, 172)", "(228, 197, 197)", "(237, 224, 222)", "(168, 45, 38)",
                 "(177, 68, 62)", "(186, 91, 86)", "(195, 114, 110)", "(204, 137, 134)", "(213, 160, 158)",
                 "(222, 183, 182)", "(231, 206, 206)", "(240, 229, 230)", "(67, 31, 134)", "(87, 55, 147)",
                 "(107, 79, 160)", "(127, 103, 173)", "(147, 127, 186)", "(167, 151, 199)", "(187, 175, 212)",
                 "(207, 199, 225)", "(227, 223, 238)", "(43, 35, 140)", "(66, 59, 152)", "(89, 83, 164)",
                 "(112, 107, 176)", "(135, 131, 188)", "(158, 155, 200)", "(181, 179, 212)", "(204, 203, 224)",
                 "(227, 227, 236)", "(26, 39, 121)", "(51, 62, 135)", "(76, 85, 149)", "(101, 108, 163)",
                 "(126, 131, 177)", "(151, 154, 191)", "(176, 177, 205)", "(201, 200, 219)", "(226, 223, 233)",
                 "(29, 73, 156)", "(54, 93, 166)", "(79, 113, 176)", "(104, 133, 186)", "(129, 153, 196)",
                 "(154, 173, 206)", "(179, 193, 216)", "(204, 213, 226)", "(229, 233, 236)", "(32, 88, 153)",
                 "(56, 106, 164)", "(80, 124, 175)", "(104, 142, 186)", "(128, 160, 197)", "(152, 178, 208)",
                 "(176, 196, 219)", "(200, 214, 230)", "(224, 232, 241)", "(39, 95, 99)", "(62, 112, 116)",
                 "(85, 129, 133)", "(108, 146, 150)", "(131, 163, 167)", "(154, 180, 184)", "(177, 197, 201)",
                 "(200, 214, 218)", "(223, 231, 235)", "(26, 75, 64)", "(51, 94, 85)", "(76, 113, 106)",
                 "(101, 132, 127)", "(126, 151, 148)", "(151, 170, 169)", "(176, 189, 190)", "(201, 208, 211)",
                 "(226, 227, 232)", "(48, 92, 40)", "(70, 110, 63)", "(92, 128, 86)", "(114, 146, 109)",
                 "(136, 164, 132)", "(158, 182, 155)", "(180, 200, 178)", "(202, 218, 201)", "(224, 236, 224)",
                 "(65, 103, 41)", "(86, 119, 64)", "(107, 135, 87)", "(128, 151, 110)", "(149, 167, 133)",
                 "(170, 183, 156)", "(191, 199, 179)", "(212, 215, 202)", "(233, 231, 225)", "(223, 117, 48)",
                 "(226, 132, 70)", "(229, 147, 92)", "(232, 162, 114)", "(235, 177, 136)", "(238, 192, 158)",
                 "(241, 207, 180)", "(244, 222, 202)", "(247, 237, 224)", "(230, 131, 55)", "(232, 144, 77)",
                 "(234, 157, 99)", "(236, 170, 121)", "(238, 183, 143)", "(240, 196, 165)", "(242, 209, 187)",
                 "(244, 222, 209)", "(246, 235, 231)", "(213, 90, 38)", "(217, 108, 62)", "(221, 126, 86)",
                 "(225, 144, 110)", "(229, 162, 134)", "(233, 180, 158)", "(237, 198, 182)", "(241, 216, 206)",
                 "(245, 234, 230)", "(176, 65, 31)", "(184, 86, 55)", "(192, 107, 79)", "(200, 128, 103)",
                 "(208, 149, 127)", "(216, 170, 151)", "(224, 191, 175)", "(232, 212, 199)", "(240, 233, 223)",
                 "(33, 33, 33)", "(57, 57, 57)", "(81, 81, 81)", "(105, 105, 105)", "(129, 129, 129)",
                 "(153, 153, 153)", "(177, 177, 177)", "(201, 201, 201)", "(225, 225, 225)", "(41, 50, 55)",
                 "(64, 72, 77)", "(87, 94, 99)", "(110, 116, 121)", "(133, 138, 143)", "(156, 160, 165)",
                 "(179, 182, 187)", "(202, 204, 209)", "(225, 226, 231)", "(59, 40, 35)", "(80, 63, 59)",
                 "(101, 86, 83)", "(122, 109, 107)", "(143, 132, 131)", "(164, 155, 155)", "(185, 178, 179)",
                 "(206, 201, 203)", "(227, 224, 227)"]
colorDictionary = {}

root = Tk()
root.title("Demo: colorAliasConfig")
root.resizable(0, 0)


def updateSelection(event):
    global colorDictionaryKeys
    colorDictionaryKeys = list(colorDictionary.keys())
    i = LB.curselection()
    updateView(event)
    if i != ():
        r, g, b = (int(j) for j in colorStorages[i[0]].replace("(", "").replace(")", "").split(","))
        Label.configure(text=f"{colorDictionary[str((r, g, b))] if str((r, g, b)) in colorDictionaryKeys else None}",
                        bg="#%02x%02x%02x" % (r, g, b))
        root.update()


def updateView(event):
    LB2.yview_moveto(LB.yview()[0])
    LB2.update()


def setColor():
    if LB.curselection() != ():
        colorDictionary[str(colorStorages[LB.curselection()[0]])] = InputText.get()
        updateSelection(None)
        i = LB.curselection()[0]
        LB2.delete(i)
        LB2.insert(i, InputText.get())
        LB2.update()


def updateAll():
    global colorDictionaryKeys
    colorDictionaryKeys = list(colorDictionary.keys())
    for i in range(len(colorStorages)):
        r, g, b = (int(j) for j in colorStorages[i].replace("(", "").replace(")", "").split(","))
        LB.delete(i)
        LB2.delete(i)
        LB.insert(i, f"{colorStorages[i]}")
        LB2.insert(i, f"{colorDictionary[str((r, g, b))] if str((r, g, b)) in colorDictionaryKeys else None}")
    root.update()


def saveDictionary(path="colorDictionary.json"):
    with open(path, "w") as f:
        f.write(json.dumps(colorDictionary))


def FileOpen():
    global colorDictionary
    r = tkinter.filedialog.askopenfilename(title='Open colorDictionary.json',
                                           filetypes=[('Json', '*.json'), ('All files', '*')])
    with open(r, "r") as f:
        colorDictionary = json.loads(f.read())
    updateAll()


def FileSave():
    r = tkinter.filedialog.asksaveasfilename(title='basicColorDictionary.json',
                                             initialdir=r'./',
                                             initialfile='basicColorDictionary.json')
    saveDictionary(r)


colorDictionaryKeys = list(colorDictionary.keys())
changeList = []
i = 0
r, g, b = 255, 255, 255

LB = Listbox(root)
LB2 = Listbox(root)
LB.grid(row=0, column=0, sticky=NSEW)
LB2.grid(row=0, column=1, sticky=NSEW)
LB.bind('<<ListboxSelect>>', updateSelection)
root.bind('<Motion>', updateView)
root.bind('<Enter>', updateView)
root.bind('<MouseWheel>', updateView)
for i in range(len(colorStorages)):
    r, g, b = (int(j) for j in colorStorages[i].replace("(", "").replace(")", "").split(","))
    LB.insert("end", f"{colorStorages[i]}")
    LB2.insert("end", f"{colorDictionary[str((r, g, b))] if str((r, g, b)) in colorDictionaryKeys else None}")
Label = Label(root, text="None", bg="white", width=15)
Label.grid(row=0, column=2, sticky=NSEW)
InputText = Entry(root)
InputText.grid(row=0, column=3, sticky=NSEW)
InputButtom = Button(root, text="Submit", command=setColor)
InputButtom.grid(row=0, column=4, sticky=NSEW)
# SaveButtom = Button(root, text="Save", command=saveDictionary)
# SaveButtom.grid(row=0, column=5, sticky=NSEW)
LoadButtom = Button(root, text="Upload", command=FileOpen)
LoadButtom.grid(row=0, column=5, sticky=NSEW)
SaveButtom2 = Button(root, text="Download", command=FileSave)
SaveButtom2.grid(row=0, column=6, sticky=NSEW)
root.update()
mainloop()
