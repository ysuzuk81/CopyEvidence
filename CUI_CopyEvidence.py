import sys

import lib.ExecuteCopyEvidence as ExecuteCopyEvidence
import lib.OutputExecuteResult as OutputExecuteResult

executeResult = ExecuteCopyEvidence.execute(sys.argv)
OutputExecuteResult.outputExecuteResult(executeResult)