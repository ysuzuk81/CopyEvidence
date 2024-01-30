class NotExistPath(Exception):
    def __init__(self, path):
        self.path = path
    
    def __str__(self):
        return str(self.path) + "が存在しません"

class NotSetConfigFilePath(Exception):
    def __str__(self):
        return "コンフィグファイルへのパスが指定されていません"
