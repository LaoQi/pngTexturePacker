# coding=utf-8
import os
import threading
import time
from tkinter import Button, Frame, Label, Entry, Tk
from tkinter import Canvas
import tkinter.filedialog as filedialog
from pngPacker import trimList, getstatus, resetStatus, writeFile, analyse
from tkinter.constants import RIGHT

__version__ = "0.0.3"

root = Tk()
# root.geometry("385x150")
root.title("pngPacker   ---  version %s" % __version__)
top = Frame(root, width = 390, height = 90)
advancedFrame = Frame(root, width = 390, height = 90)

filePathLabel = Label(top, text = "", width = 30)
outDictoryLabel = Label(top, text = "", width = 30)
outNameEntry = Entry(advancedFrame)
outNameEntry.textvariable = "image_"
limitXEntry = Entry(advancedFrame, width = 2)
limitYEntry = Entry(advancedFrame, width = 2)

pngPath = ""
outDictory = ""
name = "image_"

# global rectlist
rectlist = []

def getfilepath():
    filepath = filedialog.askopenfilename()
    if filepath:
        global pngPath
        pngPath = os.path.abspath(filepath)
        filePathLabel.config(text = filepath)    # 将选择好的路径加入到Label里面
        nameByfile()
        controlBar("未开始", 0)


def outfilepath():
    filepath = filedialog.askdirectory()
    if filepath:
        global outDictory
        outDictory = os.path.abspath(filepath)
        outDictoryLabel.config(text = filepath)

def nameByfile():
    global name
    if pngPath:
        name = os.path.basename(pngPath)[:-4]    # 去除.png扩展名
        temp = outNameEntry.get()
        outNameEntry.delete(0, len(temp))
        outNameEntry.insert(0, name)

def go():
    if not pngPath:
        return
    if not outDictory:
        return
    anaThread = threading.Thread(target = runthread, args = ())
    anaThread.start()
    viewThread = threading.Thread(target = runstatusThread, args = (anaThread,))
    viewThread.start()

def runstatusThread(anaThread):
    if anaThread :
        while(anaThread.is_alive()):
            status = getstatus()
            if status[1] == 0:
                controlBar("初始化..." , rate = 0)
            elif status[0] < status[1]:
                rate = int(status[0] * 100 / status[1])
                controlBar("%d%%" % rate, rate)
            else:
                controlBar("文件生成中", 100)
            time.sleep(0.1)
        controlBar("完成", 100)
        resetStatus()

def runthread():
    global rectlist
    limit = list(map(lambda x: bool(x) and int(x) or 1, [limitXEntry.get(), limitYEntry.get()]))
    rectlist = trimList(analyse(pngPath), limit)
    print(rectlist)
    writeFile(rectlist, outDictory, outNameEntry.get())

items = {}
bar = Canvas(top, width = 300, height = 20, bg = "white")
items['bar'] = bar.create_rectangle(2, 1, 1, 20, fill = "blue")
items['text'] = bar.create_text(140, 13, text = "未开始", fill = "black")

def controlBar(text = "未开始", rate = 0):
    global items
    global bar
    bar.coords(items['bar'], 2, 1, rate * 3, 20)
    bar.itemconfig(items['text'], text = text)


# label = Label(top, text = 'hello ,python')
# label.pack(fill=BOTH)

top.pack()
advancedFrame.pack(anchor = "nw", pady = 20)

getBtn = Button(top, text = "打开", command = getfilepath, width = 10)
outBtn = Button(top, text = "输出目录", command = outfilepath, width = 10)
analyseBtn = Button(top, text = "开始", command = go, width = 10)

customNameLabel = Label(advancedFrame, text = "自定义名称 : ", width = 10)
customNameLabel.propagate(False)
customNameLabel.pack(anchor = "nw", side = "left")
outNameEntry.pack(anchor = "ne", side = "left")
cutlimitLabel = Label(advancedFrame, text = "大小限制 : ")
cutlimitLabel.pack(anchor = "nw", side = "left")
limitXEntry.pack(anchor = "ne", side = "left")
Label(advancedFrame, text="X", width = 2).pack(anchor = "ne", side = "left")
limitYEntry.pack(anchor = "nw", side = "left")

filePathLabel.grid(row = 0, column = 0)
getBtn.grid(row = 0, column = 1)
outDictoryLabel.grid(row = 1, column = 0)
outBtn.grid(row = 1, column = 1)
analyseBtn.grid(row = 3, column = 1)
bar.grid(row = 3, column = 0)

top.mainloop()

# if __name__ == "__main__":
# main()
