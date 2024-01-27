import os
import shutil

import lib_CopyEvidence.Path as Path

def makeDesFolderPath(desRootFolderPath, srcFolderPath):
    # 先頭の../を削除する
    formatSrcFolderPath = Path.deleteFrontDotDotSlash(srcFolderPath)
    # 先頭以外の../に対しては正規化する
    formatSrcFolderPath = os.path.normpath(formatSrcFolderPath)

    desFolderPath = Path.convertPathDelimiterToSlash(os.path.join(desRootFolderPath, formatSrcFolderPath))
    return desFolderPath

# 引数のルートフォルダー直下に、ディレクトリ構造ごとファイルをコピーする
def copyFile(srcFilePath, desRootFolderPath):
    # コピー対象のディレクトリパスとファイル名を取得
    srcFolderPath = Path.convertPathDelimiterToSlash(os.path.dirname(srcFilePath))
    srcFileName   = os.path.basename(srcFilePath)
    # コピー先のディレクトリパスを生成
    # コピー対象のディレクトリ構造をそのままコピーするので単純に連結させる
    desFolderPath = makeDesFolderPath(desRootFolderPath, srcFolderPath)
    # コピー先のファイル名を生成
    # ファイル名はコピー対象のファイル名から変更しないのでそのまま
    desFileName = srcFileName
    # コピー先のファイルパスを生成
    desFilePath = Path.convertPathDelimiterToSlash(os.path.join(desFolderPath, desFileName))

    # ファイルコピーは直上のディレクトリが存在する必要があるため、コピー先のディレクトリを作成
    os.makedirs(desFolderPath, exist_ok=True)
    # ファイルをコピー
    shutil.copy(srcFilePath, desFilePath)

# 引数のルートフォルダー直下に、ディレクトリ構造ごとフォルダをコピーする
def copyFolder(srcFolderPath, desRootFolderPath):
    desFolderPath = makeDesFolderPath(desRootFolderPath, srcFolderPath)
    shutil.copytree(srcFolderPath, desFolderPath, dirs_exist_ok=True)

# ファイル・ディレクトリ問わず、引数のルートフォルダー直下にディレクトリ構造ごとコピーする
def copy(srcPath, desRootFolderPath):
    # コピー対象がファイル
    if os.path.isfile(srcPath):
        copyFile(srcPath, desRootFolderPath)

    # コピー対象がディレクトリ
    elif os.path.isdir(srcPath):
        copyFolder(srcPath, desRootFolderPath)

    else:
        # 引数異常
        assert(False)