import sys

import lib_CopyEvidence.ExecuteCopyEvidence as ExecuteCopyEvidence
import lib_CopyEvidence.ExecuteResult_IO as ExecuteResult_IO

executeResult = ExecuteCopyEvidence.execute(sys.argv)
ExecuteResult_IO.outputExecuteResult(executeResult)