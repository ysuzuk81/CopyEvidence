import glob
import os

import lib_CopyEvidence.File_IO as File_IO
import lib_CopyEvidence.Path as Path
from natsort import natsorted

# エビデンスのパスを読み出して、エビデンスが存在するものとしないものを分けて返す
def readEvidencePath(evidencePathFile):
    # エビデンスパスファイルからエビデンスパスを読み出す
    evidencePathList = File_IO.readLines(evidencePathFile)

    # 指定されたエビデンスパスのうち、存在するものとしないものを分ける
    existEvidencePathList = []
    notExistEvidencePathList = []

    for evidencePath in evidencePathList:
        # 指定されたエビデンスパスを検索
        searchEvidencePathList = glob.glob(evidencePath)

        # エビデンスが存在する場合
        # パス名展開が行われた場合、存在するファイルのみ検索結果に入るはず
        if not searchEvidencePathList == []:
            existEvidencePathList.extend(searchEvidencePathList)

        # エビデンスが存在しなかった場合
        else:
            notExistEvidencePathList.append(evidencePath)

    # ディレクトリの区切り文字を'/'に変換
    existEvidencePathList = [Path.convertPathDelimiterToSlash(evidencePath) for evidencePath in existEvidencePathList]
    notExistEvidencePathList = [Path.convertPathDelimiterToSlash(evidencePath) for evidencePath in notExistEvidencePathList]

    # パスの重複を削除
    existEvidencePathList = list(set(existEvidencePathList))
    notExistEvidencePathList = list(set(notExistEvidencePathList))

    # ソート
    existEvidencePathList = natsorted(existEvidencePathList)
    notExistEvidencePathList = natsorted(notExistEvidencePathList)
    
    return existEvidencePathList, notExistEvidencePathList
