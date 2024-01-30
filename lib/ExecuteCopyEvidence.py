import os
import datetime

from lib.ConfigValue import ConfigValue
from lib.CopyEvidence import CopyEvidence
import lib.Error as Error
from lib.PathLib import PathLib
from lib.LogMsg import LogMsg

class ExecuteResult:
    def __init__(self):
        self.timestampString = datetime.datetime.now().strftime('%m/%d %H:%M:%S')
        self.errorLogMsg = LogMsg()
        self.successLogMsg = LogMsg()
        self.destEvidenceFolderPath = ''
        self.isRequireEnter = True
    
    def isRaiseError(self):
        return self.errorLogMsg.exists()
    
    def output(self):
        print()
        print('<===========')
        print()
        print('[実行日時]')
        print(self.timestampString)
        print()

        # 正常メッセージが存在すれば全て出力
        if self.successLogMsg.exists():
            print('[実行結果]')
            print(self.successLogMsg)
            print()

        # エラーメッセージが存在すれば全て出力
        if self.errorLogMsg.exists():
            print('[発生したエラー]')
            print(self.errorLogMsg)
            print()

        print('===========>')
        print()

def formatEvidencePath(evidencePath):
    tempEvidencePath = str(evidencePath)
    outputResult = ' ' + tempEvidencePath
    normEvidencePath = PathLib.toSlashDelimiter(os.path.normpath(tempEvidencePath))
    if not tempEvidencePath == normEvidencePath:
        outputResult += f' ({normEvidencePath})'
    return outputResult

# エビデンスのコピー処理を行い、実行結果を返す
# コマンドライン引数をそのまま受け取る
def execute(configFilePath):
    executeResult = ExecuteResult()
    try:
        # 指定されたコンフィグファイルが存在しなければエラー
        if not os.path.isfile(configFilePath):
            raise Error.NotExistPath(configFilePath)
        
        # コンフィグファイルからコンフィグ値を読み出す
        configValue = ConfigValue(configFilePath)

        # エビデンスパスが何も記載されていない場合はコピー処理を行わない
        if configValue.isNotSetEvidencePath():
            executeResult.errorLogMsg.println('EVIDENCE_PATH_START~EVIDENCE_PATH_ENDにエビデンスパスが記載されていません')
        
        # 存在しないエビデンスが指定されていた場合
        if not configValue.notExistEvidencePathList == []:
            # 存在しないエビデンスのパスをエラーメッセージに出力
            executeResult.errorLogMsg.println('下記のエビデンスは存在しませんでした')
            for evidencePath in configValue.notExistEvidencePathList:
                executeResult.errorLogMsg.println(formatEvidencePath(evidencePath))

        # 存在するエビデンスはコピーする
        if not configValue.existEvidencePathList == []:
            executeResult.destEvidenceFolderPath = CopyEvidence.copy(configValue.existEvidencePathList, configValue.destRootFolderPath, configValue.evidenceFolderPrefix)
            # コピーしたエビデンスのパスを正常メッセージに出力
            executeResult.successLogMsg.println('下記のエビデンスを')
            executeResult.successLogMsg.println(executeResult.destEvidenceFolderPath)
            executeResult.successLogMsg.println('にコピーしました')
            executeResult.successLogMsg.println()
            for evidencePath in configValue.existEvidencePathList:
                executeResult.successLogMsg.println(formatEvidencePath(evidencePath))

    except Exception as err:
        executeResult.errorLogMsg.println(err)

    finally:
        # Enter入力待ちを行うかどうか決める
        # エラーが発生している場合、Enter入力待ちとする
        if executeResult.isRaiseError():
            executeResult.isRequireEnter = True

        # エラーが発生しなかった場合
        else:
            # コンフィグ値でEnter入力待ちが指定されている場合のみ、入力待ちを行う
            executeResult.isRequireEnter = configValue.isRequireEnter

        return executeResult