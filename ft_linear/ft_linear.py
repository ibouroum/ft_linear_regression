import sys

class linear_regression:
    def __init__(self):
        self.theta0 = 0
        self.theta1 = 0
        self.file = ''
        input = sys.argv
        if(len(input) != 2):
            print('Syntax Error')
            return 
        else:
            self.file = sys.argv[1]

    def readData(self):
        file = open(self.file,'r')
        f = file.readlines()
        print(f)

obj = linear_regression()
obj.readData()