# coding=utf-8
import os
import threading
import time
from tkinter import *
import tkinter.filedialog as filedialog
from pngPacker import *
from threading import Thread

top = Tk()
#     top.geometry("500x300")
top.title("pngPacker")
filePathEntry = Entry(top)
outDictoryEntry = Entry(top)

pngPath = ""
outDictory = ""

# global rectlist
rectlist = []

def getfilepath():
    filepath = filedialog.askopenfilename()
    if filepath:
        global pngPath
        pngPath = os.path.abspath(filepath)
        filePathEntry.insert(0, filepath)    # 将选择好的路径加入到entry里面
        
def outfilepath():
    filepath = filedialog.askdirectory()
    if filepath:
        global outDictory
        outDictory = os.path.abspath(filepath)
        outDictoryEntry.insert(0, filepath)    # 将选择好的路径加入到entry里面
        
def go():
    anaThread = threading.Thread(target = runthread, args = ())
#     rectlist = analyse(file)
    anaThread.start()
    while(anaThread.is_alive()):
        status = getstatus()
        if status[1] == 0:
            print("文件加载中...")
        elif status[0] < status[1]:
            print(status)
        else:
            print("生成文件...")
        time.sleep(0.01)
#     print(rectlist)
#     cnt = 0
#     while cnt < 30:
#         print(analyseLineNo,analyseLineCount)
#         time.sleep(0.5)
#         cnt += 1

def runthread():
    global rectlist
    rectlist = trimList(analyse(pngPath), [5,5])
    print(rectlist)
#     print(outDictory)
    writeFile(rectlist, outDictory, "name")

getBtn = Button(top, text = "打开", command = getfilepath)
getBtn.pack()
filePathEntry.pack()
outBtn = Button(top, text = "输出目录", command = outfilepath)
outBtn.pack()
outDictoryEntry.pack()

analyseBtn = Button(top, text = "test", command = go)
analyseBtn.pack()

def main():
    top.mainloop()

if __name__ == "__main__":
    main()
