import os
import re

class PathLib:
    @classmethod
    # パスの区切り文字を'/'に変換
    def toSlashDelimiter(cls, path):
        return path.replace(os.path.sep, '/')

    @classmethod
    # 先頭の../を削除する
    def deleteFrontDotDotSlash(cls, path):
        return re.sub(r'^(\.\.\/*)+', '', path)