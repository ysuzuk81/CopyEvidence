import os
import re

import lib_CopyEvidence.CopyCommand as CopyCommand
import lib_CopyEvidence.Path as Path

# 既存のエビデンスフォルダのうち最大のフォルダ番号を取得
def getMaxEvidenceFolderNumber(configValue):
    maxEvidenceFolderNum = 0
    for name in os.listdir(configValue.destRootFolderPath):
        if os.path.isdir(os.path.join(configValue.destRootFolderPath, name)):
            searchResult = re.findall('^' + configValue.evidenceFolderPrefix + '([0-9]+)', name)
            if not searchResult == []:
                evidenceFolderNum = int(searchResult[0])
                maxEvidenceFolderNum = max(maxEvidenceFolderNum, evidenceFolderNum)

    return maxEvidenceFolderNum

# 指定したエビデンス番号のエビデンスフォルダを作成し、パスを返す
def makeDesEvidenceFolder(makeDesEvidenceFolderNum, configValue):
    # 作成するエビデンスフォルダ名とフォルダパス
    evidenceFolderName = configValue.evidenceFolderPrefix + str(makeDesEvidenceFolderNum)
    destEvidenceFolderPath = Path.convertPathDelimiterToSlash(os.path.join(configValue.destRootFolderPath, evidenceFolderName))
    # エビデンスフォルダを作成
    os.makedirs(destEvidenceFolderPath)
    # 作成したフォルダのパスを返す
    return destEvidenceFolderPath

# エビデンスをコピーして、コピー先のフォルダパスを返す
def copyEvidence(existEvidencePathList, configValue):
    # 既存のエビデンスフォルダのうち最大のフォルダ番号を取得
    maxEvidenceFolderNum = getMaxEvidenceFolderNumber(configValue)
    # 新規で作成するコピー先のエビデンスフォルダの番号は最大番号+1
    makeDesEvidenceFolderNum = maxEvidenceFolderNum + 1
    # コピー先のエビデンスフォルダを作成
    destEvidenceFolderPath = makeDesEvidenceFolder(makeDesEvidenceFolderNum, configValue)

    # エビデンスをコピーする
    for evidencePath in existEvidencePathList:
        CopyCommand.copy(evidencePath, destEvidenceFolderPath)

    # 読み込んだエビデンスパスと、コピー先のフォルダパスを返す
    return destEvidenceFolderPath
