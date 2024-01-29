def execute(executeResult):
    print()
    print('<===========')
    print()
    print('[実行日時]')
    print(executeResult.timestampString)
    print()

    # 正常メッセージが存在すれば全て出力
    if executeResult.successLogMsg.exists():
        print('[実行結果]')
        print(executeResult.successLogMsg)
        print()

    # エラーメッセージが存在すれば全て出力
    if executeResult.errorLogMsg.exists():
        print('[発生したエラー]')
        print(executeResult.errorLogMsg)
        print()

    print('===========>')
    print()
    
def waitEnter(executeResult):
    if executeResult.isRequireEnter:
        print('Enterキーを入力してください')
        input()