import os
import re

class PathString(os.PathLike):
    def __init__(self, path):
        # パスの区切り文字を'/'に変換
        self.path = str(path).replace(os.path.sep, '/')

    # 先頭の../を削除する
    def deleteFrontDotDotSlash(self):
        self.path = re.sub(r'^(\.\.\/*)+', '', self.path)
        return self

    def __fspath__(self):
        return self.path

    def __str__(self):
        return self.path
    
    def __lt__(self, other):
        return self.path < other.path