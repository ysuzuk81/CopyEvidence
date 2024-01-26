import os
import datetime

import lib_CopyEvidence.ConfigFile_IO as ConfigFile_IO
import lib_CopyEvidence.CopyEvidence as CopyEvidence
import lib_CopyEvidence.EvidenceFile_IO as EvidenceFile_IO

class Result:
    def __init__(self):
        self.timestampString = datetime.datetime.now().strftime('%m/%d %H:%M:%S')
        self.errorMsgList = []
        self.successMsgList = []
        self.destEvidenceFolderPath = ''
        self.isRequireEnter = True

# エビデンスのコピー処理を行い、実行結果を返す
# コマンドライン引数をそのまま受け取る
def execute(commandLineArgv):
    executeResult = Result()

    while(True):
        # コマンドライン引数でコンフィグファイルが指定されていなければエラー
        if len(commandLineArgv) == 1:
            executeResult.errorMsgList.append('コマンドライン引数でコンフィグファイルのパスを指定してください')
            break

        configFilePath = commandLineArgv[1]
        # コンフィグファイルが存在しなければエラー
        if not os.path.isfile(configFilePath):
            executeResult.errorMsgList.append('コンフィグファイル' + configFilePath + 'が存在しません')
            break

        # コンフィグファイルからコンフィグ値を読み出す
        configValue, isExistEvidenceFile = ConfigFile_IO.readConfigValue(configFilePath)
        # エビデンスパスファイルが存在しなければエラー
        if not isExistEvidenceFile:
            executeResult.errorMsgList.append('EVIDENCE_FILE_PATH=' + configValue.evidenceFilePath + 'が存在しません')
            break

        # エビデンスパスファイルからエビデンスパスを読み出す
        existEvidencePathList, notExistEvidencePathList = EvidenceFile_IO.readEvidencePath(configValue.evidenceFilePath)

        # 存在しないエビデンスが指定されていた場合
        if not notExistEvidencePathList == []:
            # 存在しないエビデンスのパスをエラーメッセージに出力
            executeResult.errorMsgList.append('下記のエビデンスは存在しませんでした')
            for evidencePath in notExistEvidencePathList:
                executeResult.errorMsgList.append(' ' + evidencePath)

        # 存在するエビデンスはコピーする
        if not existEvidencePathList == []:
            executeResult.destEvidenceFolderPath = CopyEvidence.copyEvidence(existEvidencePathList, configValue)
            # コピーしたエビデンスのパスを正常メッセージに出力
            executeResult.successMsgList.append('下記のエビデンスを\n ' + executeResult.destEvidenceFolderPath + '\nにコピーしました\n')
            for evidencePath in existEvidencePathList:
                executeResult.successMsgList.append(' ' + evidencePath)

        # Enter入力待ちを行うかどうか決める
        # エラーが発生している場合、Enter入力待ちとする
        if not executeResult.errorMsgList == []:
            executeResult.isRequireEnter = True

        # エラーが発生しなかった場合
        else:
            # コンフィグ値でEnter入力待ちが指定されている場合のみ、入力待ちを行う
            executeResult.isRequireEnter = configValue.isRequireEnter

        break

    return executeResult