import sys
import PySimpleGUI as sg

import lib.ExecuteCopyEvidence as ExecuteCopyEvidence
from lib.LogMsg import LogMsg

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
        executeResult.output()

        outputLogMsg = LogMsg()
        outputLogMsg.println(f'[{executeResult.timestampString}]')
        # 何らかのエラーが発生した場合
        if executeResult.isRaiseError():
            outputLogMsg.println('何らかのエラーが発生しました')
            outputLogMsg.print('シェルの出力を確認してください')

        # 正常終了の場合
        else:
            outputLogMsg.println(executeResult.destEvidenceFolderPath)
            outputLogMsg.print('にエビデンスをコピーしました')

        window[key_LogTextField].update(outputLogMsg)
