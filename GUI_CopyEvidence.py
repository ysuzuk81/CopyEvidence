import sys
import PySimpleGUI as sg

import lib_CopyEvidence.ExecuteCopyEvidence as ExecuteCopyEvidence
import lib_CopyEvidence.ExecuteResult_IO as ExecuteResult_IO

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
        executeResult = ExecuteCopyEvidence.execute(sys.argv)
        ExecuteResult_IO.outputExecuteResult(executeResult)

        outputLogMsg = ''
        outputLogMsg = '[' + executeResult.timestampString + ']\n'
        # 正常終了の場合
        if executeResult.errorMsgList == []:
            outputLogMsg += executeResult.destEvidenceFolderPath + '\n'
            outputLogMsg += 'にエビデンスをコピーしました'

        # 何らかのエラーが発生した場合
        else:
            outputLogMsg += '何らかのエラーが発生しました\n'
            outputLogMsg += 'シェルの出力を確認してください'

        window[key_LogTextField].update(outputLogMsg)
