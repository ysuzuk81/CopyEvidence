import os

import lib_CopyEvidence.File_IO as File_IO

# エビデンスのパスを読み出して、エビデンスが存在するものとしないものを分けて返す
def readEvidencePath(evidencePathFile):
    evidencePathList = File_IO.readLines(evidencePathFile)
    # パスの重複を削除
    evidencePathList = list(set(evidencePathList))

    # 指定されたエビデンスパスのうち、存在するものとしないものを分ける
    existEvidencePathList = []
    notExistEvidencePathList = []
    for evidencePath in evidencePathList:
        if os.path.exists(evidencePath):
            existEvidencePathList.append(evidencePath)
        else:
            notExistEvidencePathList.append(evidencePath)

    return existEvidencePathList, notExistEvidencePathList
