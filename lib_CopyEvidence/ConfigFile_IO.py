import glob
import natsort
import os
import re

import lib_CopyEvidence.File_IO as File_IO
import lib_CopyEvidence.Path as Path
import lib_CopyEvidence.ValidateEvidencePath as ValidateEvidencePath

class Config:
    def __init__(self):
        self.destRootFolderPath = ''
        self.evidenceFolderPrefix = ''
        self.existEvidencePathList = []
        self.notExistEvidencePathList = []
        self.isRequireEnter = False

# コンフィグ値を読み出す
def readConfig(configFilePath):
    lineList = File_IO.readLines(configFilePath)
    # コメントは削除
    lineList = [line for line in lineList if not line[0] == '#']

    config = Config()
    evidenceSrcPath = ''
    evidencePathList = []
    isEvidencePathBlock = False
    for line in lineList:
        searchResult = re.findall('COPY_DEST_FOLDER_PATH=(.+)', line)
        if not searchResult == []:
            config.destRootFolderPath = Path.convertPathDelimiterToSlash(searchResult[0])
            # 存在しないフォルダが保存先のフォルダに指定されていた場合はフォルダを新規作成する
            if not os.path.isdir(config.destRootFolderPath):
                os.makedirs(config.destRootFolderPath, exist_ok=True)
            continue

        searchResult = re.findall('EVIDENCE_FOLDER_PREFIX=(.+)', line)
        if not searchResult == []:
            config.evidenceFolderPrefix = searchResult[0]
            continue

        if line == 'WAIT_ENTER':
            config.isRequireEnter = True
            continue
        
        searchResult = re.findall('EVIDENCE_SRC_PATH=(.+)', line)
        if not searchResult == []:
            evidenceSrcPath = Path.convertPathDelimiterToSlash(searchResult[0])
            continue
        
        if line == 'EVIDENCE_PATH_START':
            isEvidencePathBlock = True
            continue
        
        if line == 'EVIDENCE_PATH_END':
            isEvidencePathBlock = False
            continue

        if isEvidencePathBlock:
            evidencePathList.append(Path.convertPathDelimiterToSlash(line))
            continue

    config.existEvidencePathList, config.notExistEvidencePathList = ValidateEvidencePath.validate(evidenceSrcPath, evidencePathList)

    return config