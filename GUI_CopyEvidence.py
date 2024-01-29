import sys
import PySimpleGUI as sg

import lib.ExecuteCopyEvidence as ExecuteCopyEvidence
from lib.ExecuteCopyEvidence import LogMsg 
import lib.OutputExecuteResult as OutputExecuteResult

key_CopyButton = 'key_CopyButton'
key_LogTextField = 'key_LogTextField'

widget_CopyButton = sg.Button(
    'エビデンスをコピー', 
    key=key_CopyButton,
    size=(19, 3))

widget_LogTextField = sg.Multiline(
    key=key_LogTextField,
    size=(30, 3),
    disabled=True,
    no_scrollbar=True
)

layout = [
    [widget_CopyButton],
    [widget_LogTextField]
]

window = sg.Window('', layout,
    element_justification='center')

while True:
    event, values = window.read()

    # ウィンドウを閉じるボタンが押された
    if event == None:
        exit()

    if event == key_CopyButton:
        try:
            executeResult = ExecuteCopyEvidence.execute(sys.argv)
            OutputExecuteResult.execute(executeResult)
        except Exception as err:
            # エラーが発生したらシェルに出力する
            print(err)
        finally:
            outputLogMsg = LogMsg()
            outputLogMsg.println('[' + executeResult.timestampString + ']')
            # 何らかのエラーが発生した場合
            if executeResult.isRaiseError():
                outputLogMsg.println('何らかのエラーが発生しました')
                outputLogMsg.print('シェルの出力を確認してください')

            # 正常終了の場合
            else:
                outputLogMsg.println(str(executeResult.destEvidenceFolderPath))
                outputLogMsg.print('にエビデンスをコピーしました')

            window[key_LogTextField].update(outputLogMsg)
        
