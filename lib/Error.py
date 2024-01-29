class Error__NotExistPath(Exception):
    def __init__(self, path):
        self.path = path
    
    def __str__(self):
        return str(self.path) + "が存在しません"

class Error__NotExistCommandLineArgument(Exception):
    def __str__(self):
        return "コマンドライン引数が指定されていません"
