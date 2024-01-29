import sys

import lib.ExecuteCopyEvidence as ExecuteCopyEvidence
import lib.OutputExecuteResult as OutputExecuteResult

try:
    executeResult = ExecuteCopyEvidence.execute(sys.argv)
    OutputExecuteResult.execute(executeResult)
    if executeResult.isRequireEnter:
        print('Enterキーを押してください')
        input()
except Exception as err:
    print(err)
