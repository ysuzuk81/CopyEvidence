import os

import lib_CopyEvidence.File_IO as File_IO
import lib_CopyEvidence.Path as Path

# エビデンスのパスを読み出して、エビデンスが存在するものとしないものを分けて返す
def readEvidencePath(evidencePathFile):
    # エビデンスパスファイルからエビデンスパスを読み出す
    evidencePathList = File_IO.readLines(evidencePathFile)
    # ディレクトリの区切り文字を'/'に変換
    evidencePathList = [Path.convertPathDelimiterToSlash(evidencePath) for evidencePath in evidencePathList]
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
