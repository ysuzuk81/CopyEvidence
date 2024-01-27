import os
import datetime

import lib_CopyEvidence.ConfigFile_IO as ConfigFile_IO
import lib_CopyEvidence.CopyEvidence as CopyEvidence
import lib_CopyEvidence.ValidateEvidencePath as ValidateEvidencePath
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
        config = ConfigFile_IO.readConfig(configFilePath)

        # エビデンスパスが何も記載されていない場合はコピー処理を行わない
        if (config.existEvidencePathList == []) and (config.notExistEvidencePathList == []):
            executeResult.errorLogMsg += 'EVIDENCE_PATH_START~EVIDENCE_PATH_ENDにエビデンスパスが記載されていません\n'
            break

        # 存在しないエビデンスが指定されていた場合
        if not config.notExistEvidencePathList == []:
            # 存在しないエビデンスのパスをエラーメッセージに出力
            executeResult.errorLogMsg += '下記のエビデンスは存在しませんでした\n'
            for evidencePath in config.notExistEvidencePathList:
                executeResult.errorLogMsg += formatEvidencePathForOutputResult(evidencePath) + '\n'

        # 存在するエビデンスはコピーする
        if not config.existEvidencePathList == []:
            executeResult.destEvidenceFolderPath = CopyEvidence.copyEvidence(config.existEvidencePathList, config.destRootFolderPath, config.evidenceFolderPrefix)
            # コピーしたエビデンスのパスを正常メッセージに出力
            executeResult.successLogMsg += '下記のエビデンスを\n'
            executeResult.successLogMsg += executeResult.destEvidenceFolderPath + '\n' 
            executeResult.successLogMsg += 'にコピーしました\n\n'
            for evidencePath in config.existEvidencePathList:
                executeResult.successLogMsg += formatEvidencePathForOutputResult(evidencePath) + '\n'

        break

    # Enter入力待ちを行うかどうか決める
    # エラーが発生している場合、Enter入力待ちとする
    if executeResult.isRaiseError():
        executeResult.isRequireEnter = True

    # エラーが発生しなかった場合
    else:
        # コンフィグ値でEnter入力待ちが指定されている場合のみ、入力待ちを行う
        executeResult.isRequireEnter = config.isRequireEnter

    return executeResult