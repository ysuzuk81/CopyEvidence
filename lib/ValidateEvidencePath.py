import glob
import os
import natsort

import lib.Path as Path

# エビデンスが存在するものとしないものを分けて返す
def validate(evidenceSrcPath, evidencePathList):
    targetEvidencePathList = []
    # エビデンスの検索パスとエビデンスパスを繋げたパスを、コピーするエビデンスとする
    for evidencePath in evidencePathList:
        targetEvidencePathList.append(
            os.path.join(evidenceSrcPath, evidencePath)
        )

    # エビデンスパスのうち、存在するものとしないものを分ける
    existEvidencePathList = []
    notExistEvidencePathList = []

    for targetEvidencePath in targetEvidencePathList:
        # 指定されたエビデンスパスを検索
        searchEvidencePathList = glob.glob(targetEvidencePath)
        print(searchEvidencePathList)
        # エビデンスが存在する場合
        # パス名展開が行われた場合、存在するファイルのみ検索結果に入るはず
        if not searchEvidencePathList == []:
            existEvidencePathList.extend(searchEvidencePathList)

        # エビデンスが存在しなかった場合
        else:
            notExistEvidencePathList.append(targetEvidencePath)

    # ディレクトリの区切り文字を'/'に変換
    existEvidencePathList = [Path.convertPathDelimiterToSlash(evidencePath) for evidencePath in existEvidencePathList]
    notExistEvidencePathList = [Path.convertPathDelimiterToSlash(evidencePath) for evidencePath in notExistEvidencePathList]

    # パス名の重複を削除
    existEvidencePathList = list(set(existEvidencePathList))
    notExistEvidencePathList = list(set(notExistEvidencePathList))

    # ソート
    existEvidencePathList = natsort.natsorted(existEvidencePathList)
    notExistEvidencePathList = natsort.natsorted(notExistEvidencePathList)
    
    return existEvidencePathList, notExistEvidencePathList
