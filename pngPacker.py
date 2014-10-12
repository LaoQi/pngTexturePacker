# coding=utf-8
import png
import os

# 全局变量
pngdata = []
analyseLineNo = 0
analyseLineCount = 0

"""四个数据为一点 RGBA, 采用行扫描法"""    
def scanLine(lineData, y):
    lineLen = len(lineData)
    # 前一个是否没有像素
    temp = True
    pontList = []
    count = 0
    for i in range(0, lineLen, 4):
        if not isAlpha(i, y):
            if temp :
                pontList.insert(count, [i, y])
                temp = False
            if i >= lineLen - 4:    #    最后一个像素
                pontList[count] += [i, y]
                temp = True
                count += 1
        else :
            if not temp :
                pontList[count] += [i, y]
                temp = True
                count += 1
    return count, pontList
    
"""判断是否为透明"""
def isAlpha(x, y):
#     if pngdata[y][x] == 0 and pngdata[y][x + 1] == 0 and pngdata[y][x + 2] == 0 and pngdata[y][x + 3] == 0 :
#         return True
    if pngdata[y][x + 3] == 0:
        return True
    return False

"""判断两个区间是否关联"""
def isRelate(l1, l2):
    if l1[0] >= l2[0] and l1[0] <= l2[2]:    # l1左端 在 l2中间
        rtn = True
    elif l1[2] >= l2[0] and l1[2] <= l2[2]:    # l1右端 在 l2中间
        rtn = True
    elif l1[0] <= l2[0] and l1[2] >= l2[2]:    # l1 在l2中间
        rtn = True
    elif l1[0] >= l2[0] and l1[2] <= l2[2]:    # l2 在l1中间
        rtn = True
    else:
        rtn = False
    return rtn

"""返回矩阵构成的图片数据"""
def makePngData(r):
    rtn = []
    for i in range(r[1], r[3] + 1):
        temp = pngdata[i]
        rtn.append(temp[r[0]:r[2]])
    return rtn    
    
"""分析图片，生产切割矩阵点"""
def analyse(pngPath):
    file = open(pngPath, "rb")
    r = png.Reader(file)
    global pngdata
    global analyseLineNo
    global analyseLineCount
    
    pngdata = list(r.read()[2])
    pnglen = len(pngdata)
    analyseLineCount = pnglen
    rectList = []    #    矩阵列表
    tempRect = []    #    矩阵临时表
    dellistT = []    #    临时表删除元素
    dellistR = []    #    返回表删除元素
    
    for l in range(0, pnglen):
        analyseLineNo = l + 1
        result = scanLine(pngdata[l], l)

#         print("扫描到 %d 行" % l)
        if result[0] > 0:
            for t in range(0, len(tempRect)):
                if tempRect[t] in dellistT:
                    continue
                notChange = True
                for r in range(0, len(result[1])):
                    if isRelate(tempRect[t], result[1][r]):
                        tempRect[t][3] = result[1][r][3]
                        tempRect[t][0] = min(tempRect[t][0], result[1][r][0])
                        tempRect[t][2] = max(tempRect[t][2], result[1][r][2])
                        dellistR.append(result[1][r])
                        notChange = False

                for i in dellistR:
                    if i in result[1]:
                        result[1].remove(i)
                dellistR = []
                #    在自身寻找关联区间
                for x in range(0, len(tempRect)):
                    if tempRect[x] in dellistT:
                        continue
                    if x != t and isRelate(tempRect[t], tempRect[x]):
                        tempRect[t][1] = min(tempRect[t][1], tempRect[x][1])
                        tempRect[t][3] = max(tempRect[t][3], tempRect[x][3])
                        tempRect[t][0] = min(tempRect[t][0], tempRect[x][0])
                        tempRect[t][2] = max(tempRect[t][2], tempRect[x][2])
                        dellistT.append(tempRect[x])
                        
                if notChange:
#                     print("出现")
                    rectList.append(tempRect[t])
                    dellistT.append(tempRect[t])
                    
        else:
            if len(tempRect) > 0:
                rectList += tempRect
                tempRect = []

        for i in dellistT:
            if i in tempRect :
                tempRect.remove(i)
        dellistT = []
        tempRect += result[1]
    file.close()
    return rectList

def trimList(rectlist, limit=[3,3]):
    '''
    裁剪矩阵列表，把噪点去掉
    :param rectlist:
    :param limit:
    '''
    newlist = []
    for r in rectlist:
        if r[2] - r[0] > limit[0] and (r[3] - r[1])/4 > limit[1]:
            newlist.append(r)
    return newlist

"""输出图片"""
def writeFile(rectList, path = "temp//", name = "out"):
    '''
    输出图片
    :param rectList:分析后的矩阵
    :param path:目标地址
    :param name:命名前缀
    :param limit:大小限制，默认无限制，比如小于2x2的图片不生成
    '''
    for n in range(len(rectList)):
        s = makePngData(rectList[n])
        if len(s) > 0:
            outfile = open(os.path.join(path,name + "%d.png" % n), "wb")
            w = png.Writer(int(len(s[0]) / 4), len(s), greyscale = False, bitdepth = 8, alpha = True, planes = 4)
            w.write(outfile, s)
            outfile.close()

def getstatus():
    return analyseLineNo,analyseLineCount
    

#     rectList = analyse()
#     writeFile(rectList, "temp//", limit=[2,2])
# 
#     print(len(rectList), rectList)

