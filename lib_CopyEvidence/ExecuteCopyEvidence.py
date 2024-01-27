import os
import datetime

import lib_CopyEvidence.ConfigFile_IO as ConfigFile_IO
import lib_CopyEvidence.CopyEvidence as CopyEvidence
import lib_CopyEvidence.EvidenceFile_IO as EvidenceFile_IO
import lib_CopyEvidence.Path as Path

class Result:
    def __init__(self):
        self.timestampString = datetime.datetime.now().strftime('%m/%d %H:%M:%S')
        self.errorLogMsg = ''
        self.successLogMsg = ''
        self.destEvidenceFolderPath = ''
        self.isRequireEnter = True
    
    def isRaiseError(self):
        return self.errorLogMsg != ''

def formatEvidencePathForOutputResult(evidencePath):
    outputResult = ' ' + evidencePath
    normEvidencePath = Path.convertPathDelimiterToSlash(os.path.normpath(evidencePath))
    if evidencePath != normEvidencePath:
        outputResult += ' (' + normEvidencePath + ')'
    return outputResult

# エビデンスのコピー処理を行い、実行結果を返す
# コマンドライン引数をそのまま受け取る
def execute(commandLineArgv):
    executeResult = Result()

    while(True):
        # コマンドライン引数でコンフィグファイルが指定されていなければエラー
        if len(commandLineArgv) == 1:
            executeResult.errorLogMsg += 'コマンドライン引数でコンフィグファイルのパスを指定してください\n'
            break

        configFilePath = commandLineArgv[1]
        # コンフィグファイルが存在しなければエラー
        if not os.path.isfile(configFilePath):
            executeResult.errorLogMsg += 'コンフィグファイル' + configFilePath + '\n'
            executeResult.errorLogMsg += 'が存在しません\n'
            break

        # コンフィグファイルからコンフィグ値を読み出す
        configValue, isExistEvidenceFile = ConfigFile_IO.readConfigValue(configFilePath)
        # エビデンスパスファイルが存在しなければエラー
        if not isExistEvidenceFile:
            executeResult.errorLogMsg += 'EVIDENCE_FILE_PATH=' + configValue.evidenceFilePath + '\n'
            executeResult.errorLogMsg += 'が存在しません\n'
            break

        # エビデンスパスファイルからエビデンスパスを読み出す
        existEvidencePathList, notExistEvidencePathList = EvidenceFile_IO.readEvidencePath(configValue.evidenceFilePath)

        # エビデンスパスファイルにエビデンスパスが何も記載されていない場合はコピー処理を行わない
        if (existEvidencePathList == []) and (notExistEvidencePathList == []):
            executeResult.errorLogMsg += 'EVIDENCE_FILE_PATH=' + configValue.evidenceFilePath + '\n'
            executeResult.errorLogMsg += 'にエビデンスパスが記載されていません\n'

        # 存在しないエビデンスが指定されていた場合
        if not notExistEvidencePathList == []:
            # 存在しないエビデンスのパスをエラーメッセージに出力
            executeResult.errorLogMsg += '下記のエビデンスは存在しませんでした\n'
            for evidencePath in notExistEvidencePathList:
                executeResult.errorLogMsg += formatEvidencePathForOutputResult(evidencePath) + '\n'

        # 存在するエビデンスはコピーする
        if not existEvidencePathList == []:
            executeResult.destEvidenceFolderPath = CopyEvidence.copyEvidence(existEvidencePathList, configValue)
            # コピーしたエビデンスのパスを正常メッセージに出力
            executeResult.successLogMsg += '下記のエビデンスを\n'
            executeResult.successLogMsg += executeResult.destEvidenceFolderPath + '\n' 
            executeResult.successLogMsg += 'にコピーしました\n\n'
            for evidencePath in existEvidencePathList:
                executeResult.successLogMsg += formatEvidencePathForOutputResult(evidencePath) + '\n'

        # Enter入力待ちを行うかどうか決める
        # エラーが発生している場合、Enter入力待ちとする
        if not executeResult.errorLogMsg == []:
            executeResult.isRequireEnter = True

        # エラーが発生しなかった場合
        else:
            # コンフィグ値でEnter入力待ちが指定されている場合のみ、入力待ちを行う
            executeResult.isRequireEnter = configValue.isRequireEnter

        break

    return executeResult