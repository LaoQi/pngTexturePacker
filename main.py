# coding=utf-8
import os
import threading
import time
from tkinter import *
import tkinter.filedialog as filedialog
from pngPacker import *
from threading import Thread

__version__ = "0.0.2"

top = Tk()
top.geometry("390x90")
top.title("pngPacker   ---  version %s" % __version__)
filePathLabel = Label(top, text = "", width = "30")
outDictoryLabel = Label(top, text = "", width = "30")

pngPath = ""
outDictory = ""

# global rectlist
rectlist = []

def getfilepath():
    filepath = filedialog.askopenfilename()
    if filepath:
        global pngPath
        pngPath = os.path.abspath(filepath)
        filePathLabel.config(text = filepath)    # 将选择好的路径加入到Label里面
        controlBar("未开始", 0)


def outfilepath():
    filepath = filedialog.askdirectory()
    if filepath:
        global outDictory
        outDictory = os.path.abspath(filepath)
        outDictoryLabel.config(text = filepath)

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
    rectlist = trimList(analyse(pngPath), [5, 5])
    print(rectlist)
    writeFile(rectlist, outDictory, "name")

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
getBtn = Button(top, text = "打开", command = getfilepath, width = 10)
outBtn = Button(top, text = "输出目录", command = outfilepath, width = 10)
analyseBtn = Button(top, text = "开始", command = go, width = 10)

filePathLabel.grid(row = 0, column = 0)
getBtn.grid(row = 0, column = 1)
outDictoryLabel.grid(row = 1, column = 0)
outBtn.grid(row = 1, column = 1)
analyseBtn.grid(row = 3, column = 1)
bar.grid(row = 3, column = 0)

top.mainloop()

# if __name__ == "__main__":
# main()
