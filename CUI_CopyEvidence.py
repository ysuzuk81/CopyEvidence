import sys

import lib.ExecuteCopyEvidence as ExecuteCopyEvidence

def waitEnter():
    print('Enterキーを押してください')
    input()

if len(sys.argv) == 1:
    print("コマンドライン引数でコンフィグファイルへのパスを指定してください")
    waitEnter()
    exit()

executeResult = ExecuteCopyEvidence.execute(sys.argv[1])
executeResult.output()

if executeResult.isRequireEnter:
    waitEnter()
