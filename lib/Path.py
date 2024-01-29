import os
import re

# パスの区切り文字を'/'に変換
def convertPathDelimiterToSlash(path):
    return path.replace(os.path.sep, '/')

# 先頭の../を削除する
def deleteFrontDotDotSlash(path):
    return re.sub(r'^(\.\.\/*)+', '', path)
