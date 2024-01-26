import os

# 空行以外の行を読み出してリストを返す
def readLines(filePath):
    lineList = []
    with open(filePath, encoding="utf-8") as file:
        lineList = file.readlines()

    formatLineList = []
    for line in lineList:
        formatLine = line.rstrip()
        if formatLine != '':
            formatLineList.append(formatLine)
    
    return formatLineList