import os
import re
import shutil

import lib.Error as Error
from lib.PathLib import PathLib

class CopyEvidence:
    # エビデンスをコピーして、コピー先のフォルダパスを返す
    @classmethod
    def copy(cls, existEvidencePathList, destRootFolderPath, evidenceFolderPrefix):
        if not os.path.isdir(destRootFolderPath):
            os.makedirs(destRootFolderPath, exist_ok=True)

        # 既存のエビデンスフォルダのうち最大のフォルダ番号を取得
        evidenceFolderMaxNum = CopyEvidence.__getEvidenceFolderMaxNumber(destRootFolderPath, evidenceFolderPrefix)
        # 新規で作成するコピー先のエビデンスフォルダの番号は最大番号+1
        makeDestEvidenceFolderNum = evidenceFolderMaxNum + 1
        # コピー先のエビデンスフォルダを作成
        destEvidenceFolderPath = CopyEvidence.__makeDestEvidenceFolder(makeDestEvidenceFolderNum, destRootFolderPath, evidenceFolderPrefix)

        # エビデンスをコピーする
        for evidencePath in existEvidencePathList:
            if os.path.isfile(evidencePath):
                CopyEvidence.__copyFile(evidencePath, destEvidenceFolderPath)

            elif os.path.isdir(evidencePath):
                CopyEvidence.__copyFolder(evidencePath, destEvidenceFolderPath)

            else:
                raise Error.Error__NotExistPath(evidencePath)

        # コピー先のフォルダパスを返す
        return destEvidenceFolderPath

    @classmethod
    # 既存のエビデンスフォルダのうち最大のフォルダ番号を取得
    def __getEvidenceFolderMaxNumber(cls, destRootFolderPath, evidenceFolderPrefix):
        evidenceFolderMaxNum = 0
        for name in os.listdir(destRootFolderPath):
            if os.path.isdir(os.path.join(destRootFolderPath, name)):
                searchResult = re.findall('^' + evidenceFolderPrefix + '([0-9]+)', name)
                if not searchResult == []:
                    evidenceFolderNum = int(searchResult[0])
                    evidenceFolderMaxNum = max(evidenceFolderMaxNum, evidenceFolderNum)

        return evidenceFolderMaxNum

    @classmethod
    # 指定したエビデンス番号のエビデンスフォルダを作成し、パスを返す
    def __makeDestEvidenceFolder(cls, makeDestEvidenceFolderNum, destRootFolderPath, evidenceFolderPrefix):
        # 作成するエビデンスフォルダ名とフォルダパス
        evidenceFolderName = evidenceFolderPrefix + str(makeDestEvidenceFolderNum)
        destEvidenceFolderPath = PathLib.toSlashDelimiter(os.path.join(destRootFolderPath, evidenceFolderName))
        # エビデンスフォルダを作成
        os.makedirs(destEvidenceFolderPath)
        # 作成したフォルダのパスを返す
        return destEvidenceFolderPath

    @classmethod
    # 引数のルートフォルダー直下に、ディレクトリ構造ごとファイルをコピーする
    def __copyFile(cls, srcFilePath, destRootFolderPath):
        # コピー対象のディレクトリパスとファイル名を取得
        srcFolderPath = PathLib.toSlashDelimiter(os.path.dirname(srcFilePath))
        srcFileName   = os.path.basename(srcFilePath)
        # コピー先のディレクトリパスを生成
        # コピー対象のディレクトリ構造をそのままコピーするので単純に連結させる
        desFolderPath = CopyEvidence.__makeDesFolderPath(destRootFolderPath, srcFolderPath)
        # コピー先のファイル名を生成
        # ファイル名はコピー対象のファイル名から変更しないのでそのまま
        desFileName = srcFileName
        # コピー先のファイルパスを生成
        desFilePath = PathLib.toSlashDelimiter(os.path.join(desFolderPath, desFileName))

        # ファイルコピーは直上のディレクトリが存在する必要があるため、コピー先のディレクトリを作成
        os.makedirs(desFolderPath, exist_ok=True)
        # ファイルをコピー
        shutil.copy(srcFilePath, desFilePath)

    @classmethod
    def __makeDesFolderPath(cls, destRootFolderPath, srcFolderPath):
        # 先頭の../を削除する
        formatSrcFolderPath = PathLib.deleteFrontDotDotSlash(PathLib.toSlashDelimiter(srcFolderPath))
        # 先頭以外の../に対しては正規化する
        formatSrcFolderPath = os.path.normpath(formatSrcFolderPath)

        desFolderPath = PathLib.toSlashDelimiter(os.path.join(destRootFolderPath, formatSrcFolderPath))
        return desFolderPath

    @classmethod
    # 引数のルートフォルダー直下に、ディレクトリ構造ごとフォルダをコピーする
    def __copyFolder(cls, srcFolderPath, destRootFolderPath):
        desFolderPath = CopyEvidence.__makeDesFolderPath(destRootFolderPath, srcFolderPath)
        shutil.copytree(srcFolderPath, desFolderPath, dirs_exist_ok=True)


