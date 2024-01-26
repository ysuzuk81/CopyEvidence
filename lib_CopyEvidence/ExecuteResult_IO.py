def outputExecuteResult(executeResult):
    print()
    print('<===========')
    print()
    print('[実行日時]')
    print(executeResult.timestampString)
    print()

    # 正常メッセージが存在すれば全て出力
    if not executeResult.successMsgList == []:
        print('[実行結果]')
        for msg in executeResult.successMsgList:
            print(msg)
        print()

    # エラーメッセージが存在すれば全て出力
    if not executeResult.errorMsgList == []:
        print('[発生したエラー]')
        for msg in executeResult.errorMsgList:
            print(msg)
        print()

    print('===========>')
    print()
    
def waitEnter(executeResult):
    if executeResult.isRequireEnter:
        print('Enterキーを入力してください')
        input()