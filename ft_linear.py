import  csv
import  sys
import  os.path
from pandas import DataFrame
import matplotlib.pyplot as plt

class linear_regression:
    def __init__(self):
        self.data = self.read_data()
        self.x = self.data[0]
        self.y = self.data[1]
        self.M = len(self.x)
        self.deltaX = max(self.x) - min(self.x)
        self.deltaY = max(self.y) - min(self.y)
        self.dfX = DataFrame(self.normalisation(self.x), columns=['km'])
        self.dfY = DataFrame(self.normalisation(self.y), columns=['price'])
        self.Xn = self.normalisation(self.x)
        self.Yn = self.normalisation(self.y)
        self.theta_0 = 0.0
        self.theta_1 = 0.0
        self.tmp_theta_0 = 1.0
        self.tmp_theta_1 = 1.0
        self.prev_mse = 0.0
        self.cur_mse = self.CostFuncMSE()
        self.delta_mse = self.cur_mse
        self.learningRate = 0.1
        self.modelTrainnig()


        self.figure, self.axis = plt.subplots(2,2,figsize=(10, 10))
       
        self.plot_Ori_data()
        self.plot_Nor_data()
        self.plot_Linear()
        self.plot_show()
        
    def plot_Ori_data(self):
        p1 = self.axis[0, 0]
        p1.plot(self.x, self.y, 'ro', label='data')
        p1.set_ylabel('Price (in euro)')
        p1.set_xlabel('Mileage (in km)')
        p1.set_title('Original Data Plot')

    def plot_Nor_data(self):
        p1 = self.axis[0, 1]
        p1.plot(self.Xn, self.Yn, 'ro', label='data')
        p1.set_ylabel('Price (in euro)')
        p1.set_xlabel('Mileage (in km)')
        p1.set_title('Normalised Data Plot')

    def plot_Linear(self):
        p1 = self.axis[1, 0]
        p1.plot(self.x, self.y, 'ro', label='data')
        x_estim = self.x
        y_estim = [self.theta_0 + self.theta_1 * _  for _ in self.x]
        p1.plot(x_estim, y_estim, 'g-', label='Estimation')
        p1.set_ylabel('Price (in euro)')
        p1.set_xlabel('Mileage (in km)')
        p1.set_title('Linear Regression Plot')

    def plot_show(self):
        imgname = f'./Plots.png'
        plt.savefig(imgname)
        plt.close()

    def read_data(self) :
        self.data = []
        mileages = []
        prices = []
        if len(sys.argv) != 2 :
             sys.exit("Error: Syntax Error")
        else :
            self.name = sys.argv[1]

        if (os.path.isfile(self.name) == False) :
            sys.exit("Error: File " + self.name + " doesn't exist")

        if (os.access(self.name, os.R_OK) == False) :
           sys.exit("Error: Access denied for " + self.name)

        with open(self.name, 'r') as csv_file:
            try:
                dict_val = csv.reader(csv_file, delimiter = ",")
                for row in dict_val:
                    mileages.append(row[0])
                    prices.append(row[1])

                mileages.pop(0)
                prices.pop(0)
                for i in range(len(mileages)):
                    mileages[i] = eval(mileages[i])
                    prices[i] = eval(prices[i])
                return (mileages, prices)
                
            except:
                sys.exit("Error: File" + self.name +  "cannot be read")

    def normalisation(self,s):
        return [((_ - min(s)) / (max(s) - min(s))) for _ in s]

    def estimatePrice(self, mileage) :
        return ((self.tmp_theta_0 + (self.tmp_theta_1 * mileage)))
        

    def CostFuncMSE(self):
        return ((self.estimatePrice(self.dfX['km'] ) - self.dfY['price']) ** 2).sum() / self.M

    def calculateTheta0(self) :
        sumResidual = (self.estimatePrice(self.dfX['km']) - self.dfY['price']).sum()
        return (self.learningRate * sumResidual / (self.M))
    
    def calculateTheta1(self) :
        sumResidual = ((self.estimatePrice(self.dfX['km']) - self.dfY['price']) \
                    * self.dfX['km']).sum()
        return (self.learningRate * (sumResidual / (self.M)))

    def save_thetas(self) :
        f = open("thetas.csv", "w+")
        f.write("%f, %f" %(self.theta_0, self.theta_1))
        f.close()

    def modelTrainnig(self) :
        while self.delta_mse > 0.0000001 or self.delta_mse < -0.0000001 :
            self.theta_0 = self.tmp_theta_0
            self.theta_1 = self.tmp_theta_1
            self.tmp_theta_0 -= self.calculateTheta0()
            self.tmp_theta_1 -= self.calculateTheta1()
            self.prev_mse = self.cur_mse
            self.cur_mse = self.CostFuncMSE()
            self.delta_mse = self.cur_mse - self.prev_mse
        self.theta_1 = self.deltaY * self.theta_1 / self.deltaX
        self.theta_0 = (self.deltaY * self.theta_0) + min(self.y) + self.theta_1 * (1 - min(self.x))
        self.save_thetas()
linear_regression()