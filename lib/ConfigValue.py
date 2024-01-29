import glob
import natsort
import os
import re

from lib.TextFile import TextFile
from lib.PathLib import PathLib
class ConfigValue:
    def __init__(self, configFilePath):
        self.destRootFolderPath = ''
        self.evidenceFolderPrefix = ''
        self.existEvidencePathList = []
        self.notExistEvidencePathList = []
        self.isRequireEnter = False

        configFile = TextFile(PathLib.toSlashDelimiter(configFilePath)).deleteCommentLine('//')

        isEvidencePathBlock = False
        evidencePathStringList = []
        for textLine in configFile.textLineList:
            searchResult = re.findall('COPY_DEST_FOLDER_PATH=(.+)', textLine)
            if not searchResult == []:
                self.destRootFolderPath = PathLib.toSlashDelimiter(searchResult[0])
                if os.path.isdir(self.destRootFolderPath):
                     # 存在しないフォルダが保存先のフォルダに指定されていた場合はフォルダを新規作成する
                    os.makedirs(searchResult[0], exist_ok=True)
                continue

            searchResult = re.findall('EVIDENCE_FOLDER_PREFIX=(.+)', textLine)
            if not searchResult == []:
                self.evidenceFolderPrefix = searchResult[0]
                continue

            if textLine == 'WAIT_ENTER':
                self.isRequireEnter = True
                continue

            searchResult = re.findall('EVIDENCE_SRC_PATH=(.+)', textLine)
            if not searchResult == []:
                evidenceSrcPath = PathLib.toSlashDelimiter(searchResult[0])
                continue

            if textLine == 'EVIDENCE_PATH_START':
                isEvidencePathBlock = True
                continue
            
            if textLine == 'EVIDENCE_PATH_END':
                isEvidencePathBlock = False
                continue

            if isEvidencePathBlock:
                evidencePathStringList.append(textLine)
                continue
        
        targetEvidencePathList = []
        # エビデンスの検索パスとエビデンスパスを繋げたパスを、コピーするエビデンスとする
        for evidencePathString in evidencePathStringList:
            targetEvidencePathList.append(
                os.path.join(evidenceSrcPath, evidencePathString)
            )

        for targetEvidencePath in targetEvidencePathList:
            # 指定されたエビデンスパスを検索
            searchEvidencePathList = glob.glob(targetEvidencePath)
            # エビデンスが存在する場合
            if not searchEvidencePathList == []:
                self.existEvidencePathList.extend(searchEvidencePathList)

            # エビデンスが存在しなかった場合
            else:
                self.notExistEvidencePathList.append(targetEvidencePath)

        # PathString型に変換
        self.existEvidencePathList = [PathLib.toSlashDelimiter(evidencePath) for evidencePath in self.existEvidencePathList]
        self.notExistEvidencePathList = [PathLib.toSlashDelimiter(evidencePath) for evidencePath in self.notExistEvidencePathList]

        # パス名の重複を削除
        self.existEvidencePathList = list(set(self.existEvidencePathList))
        self.notExistEvidencePathList = list(set(self.notExistEvidencePathList))

        # ソート
        self.existEvidencePathList = natsort.natsorted(self.existEvidencePathList)
        self.notExistEvidencePathList = natsort.natsorted(self.notExistEvidencePathList)
    
    def isNotSetEvidencePath(self):
        return (self.existEvidencePathList == []) and (self.notExistEvidencePathList == [])
