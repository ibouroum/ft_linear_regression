import  csv

thetas = []
try :
    with open("thetas.csv", 'r') as csv_file :
        dict_val = csv.reader(csv_file, delimiter = ",")
        for row in dict_val :
            thetas.append(row)
        theta0 = thetas[0][0]
        theta1 = thetas[0][1]
except :
    theta0 = 0
    theta1 = 0

check = False
while check == False :
    mileage = input("Enter mileage: ")
    try :
        mileage = float(mileage) - 0
        if (mileage >= 0) :
            check = True
        else :
            print ("Error: negative mileage? Try again.")
    except :
        print ("Error: not a number, try again.")
price = float(theta0) + (float(theta1) * mileage)
print('The price of this care is :', price, 'euros')
