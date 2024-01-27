import re
import os

import lib_CopyEvidence.File_IO as File_IO
import lib_CopyEvidence.Path as Path

class ConfigValue:
    def __init__(self):
        self.evidenceFilePath = ''
        self.destRootFolderPath = ''
        self.evidenceFolderPrefix = ''
        self.isRequireEnter = False

# コンフィグ値を読み出す
def readConfigValue(configFilePath):
    configValue = ConfigValue()
    isExistEvidenceFile = True

    lineList = File_IO.readLines(configFilePath)
    for line in lineList:
        firstChar = line[0]
        # コメントなので読み飛ばし
        if firstChar == '#':
            continue
        
        searchResult = re.findall('EVIDENCE_FILE_PATH=(.+)', line)
        if not searchResult == []:
            configValue.evidenceFilePath = Path.convertPathDelimiterToSlash(searchResult[0])
            # 存在しないファイルが指定されている場合はエラー
            if not os.path.isfile(configValue.evidenceFilePath):
                isExistEvidenceFile = False
                break
            else:
                continue

        searchResult = re.findall('DEST_FOLDER_PATH=(.+)', line)
        if not searchResult == []:
            configValue.destRootFolderPath = Path.convertPathDelimiterToSlash(searchResult[0])
            # 存在しないフォルダが指定されている場合はフォルダを作成する
            if not os.path.isdir(configValue.destRootFolderPath):
                os.makedirs(configValue.destRootFolderPath, exist_ok=True)
            continue

        searchResult = re.findall('EVIDENCE_FOLDER_PREFIX=(.+)', line)
        if not searchResult == []:
            configValue.evidenceFolderPrefix = searchResult[0]
            continue

        if line == 'WAIT_ENTER':
            configValue.waitEnter = True
            continue
            
    return configValue, isExistEvidenceFile