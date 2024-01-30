class LogMsg:
    def __init__(self):
        self.logMsg = ''
    
    def print(self, logMsg = ''):
        self.logMsg += str(logMsg)
    
    def println(self, logMsg = ''):
        self.print(logMsg)
        self.logMsg += '\n'

    def exists(self):
        return not self.logMsg == ''
    
    def __str__(self):
        return self.logMsg