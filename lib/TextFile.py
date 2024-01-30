import os
import lib.Error as Error

class TextFile:
    def __init__(self, filePath):
        self.filePath = filePath
        self.textLineList = []

        if not os.path.isfile(self.filePath):
            raise Error.NotExistPath(self.filePath)

        with open(self.filePath, encoding="utf-8") as file:
            self.textLineList = file.readlines()

        # 改行のみの行を削除 & 行末の改行を削除
        self.textLineList = [textLine.rstrip() for textLine in self.textLineList if not textLine.rstrip() == '']

    @classmethod
    def __isCommentLine(cls, line, commentStartString):
        if commentStartString == '':
            return False
        
        return line[0:len(commentStartString)] == commentStartString

    def deleteCommentLine(self, commentStartString):
        self.textLineList = [textLine for textLine in self.textLineList if not TextFile.__isCommentLine(textLine, commentStartString)]
        return self