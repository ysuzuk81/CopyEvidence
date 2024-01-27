import sys

import lib_CopyEvidence.ExecuteCopyEvidence as ExecuteCopyEvidence
import lib_CopyEvidence.OutputExecuteResult as OutputExecuteResult

executeResult = ExecuteCopyEvidence.execute(sys.argv)
OutputExecuteResult.outputExecuteResult(executeResult)