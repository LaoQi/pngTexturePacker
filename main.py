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

# global analyseLineNo
# global analyseLineCount
# global rectlist
rectlist = []
analyseLineNo = 0    #    分析行数
analyseLineCount = 0    #    总行数

def getfilepath():
    filepath = filedialog.askopenfilename()
    if filepath:
        global pngPath
        pngPath = os.path.abspath(filepath)
        filePathEntry.insert(0, filepath)    # 将选择好的路径加入到entry里面
        
def outfilepath():
    filepath = filedialog.askdirectory()
    if filepath:
        outDictory = os.path.abspath(filepath)
        outDictoryEntry.insert(0, filepath)    # 将选择好的路径加入到entry里面
        
def go():
    anaThread = threading.Thread(target = runthread, args = ())
#     rectlist = analyse(file)
    anaThread.start()
    while(anaThread.is_alive()):
        print(analyseLineNo, analyseLineCount)
        time.sleep(0.1)
    print(rectlist)
#     cnt = 0
#     while cnt < 30:
#         print(analyseLineNo,analyseLineCount)
#         time.sleep(0.5)
#         cnt += 1

def runthread():
    global rectlist
    rectlist = analyse(pngPath)

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
