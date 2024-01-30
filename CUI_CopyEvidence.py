import sys

import lib.ExecuteCopyEvidence as ExecuteCopyEvidence

executeResult = ExecuteCopyEvidence.execute(sys.argv)
executeResult.output()

if executeResult.isRequireEnter:
    print('Enterキーを押してください')
    input()
