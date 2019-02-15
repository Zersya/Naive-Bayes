import csv

attributes = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[]]]
model_arrays_train = []
index_b = [0,0,0,0,0,0,0,0]
temp_50K = []
b_bawah = [0,0]
models_test = []

def importTrain():
    with open('res/TrainsetTugas1ML.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in spamreader:
            if line_count == 0:
                line_count += 1
            else:
                model_arrays_train.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]) # untuk permudah index
                line_count += 1
    for model in model_arrays_train:
        setAttribute(0,model[1])
        setAttribute(1,model[2])
        setAttribute(2,model[3])
        setAttribute(3,model[4])
        setAttribute(4,model[5])
        setAttribute(5,model[6])
        setAttribute(6,model[7])
        setAttribute(7,model[8])

def importTest():
    with open('res/TestsetTugas1ML.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in spamreader:
            calculation_p_more50  = []
            calculation_p_less50  = []
            if line_count == 0:
                line_count += 1
            else:
                for i in range(1, 8):
                    for j in range(0,3):
                        if(row[i] == attributes[i-1][j][0]):
                            # print(row[0], row[i], attributes[i-1][j][0])

                            calculation_p_more50.append(attributes[i-1][j][1])
                            calculation_p_less50.append(attributes[i-1][j][2])
                            
                calculation_p_less50.append(attributes[7][1][1])
                calculation_p_more50.append(attributes[7][0][1])

                multiPmore = multiplyList(calculation_p_more50)
                multiPless = multiplyList(calculation_p_less50)

                if(multiPless > multiPmore):
                    models_test.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], '<=50k'])
                else:
                    models_test.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], '>50k'])

                line_count += 1

def csv_writer():
    with open('TebakanTugas1ML.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'age', 'workclass', 'education', 'marital-status', 'occupation', 'relationship', 'hours-per-week'])
        for test in models_test:
            writer.writerow([test[0], test[1], test[2], test[3], test[4], test[5], test[6], test[7], test[8]])

def setAttribute(index, model):
    isAppend = True
    k = index_b[index]
    if(index_b[index] > 2): k = 2

    for attribute in attributes[index]:
        for att in attribute:
            if(att == model):
                isAppend = False
                break
    if(isAppend):
        attributes[index][k].append(model)
        index_b[index] += 1

def getProbs(l, k):
    maxK = 2
    if(k > 2): getProbs(l+1, 0)
    if(l > 7): return
    if(l == 7): maxK = 1
    if(k > maxK): return
    sizeData = [0, 0]
    
    if(l != 7):
        for model in model_arrays_train:
            if((model[l+1] == attributes[l][k][0]) and (model[8] == attributes[7][0][0])): # >50k
                sizeData[0]+=1
            elif((model[l+1] == attributes[l][k][0]) and (model[8] == attributes[7][1][0])): # <=50k
                sizeData[1]+=1
        attributes[l][k].append(round(float(float(sizeData[0])/float(b_bawah[0])),2))
        attributes[l][k].append(round(float(float(sizeData[1])/float(b_bawah[1])),2))
        
    else:
        if(k == 1):
            attributes[l][k-1].append(float(b_bawah[0])/float(b_bawah[0]+b_bawah[1]))
            attributes[l][k].append(float(b_bawah[1])/float(b_bawah[0]+b_bawah[1]))
            
    getProbs(l, k+1)

def getProbsBawah():
    for model in model_arrays_train:
        if(model[8] == attributes[7][0][0]): # >50k
            b_bawah[0]+=1
        elif(model[8] == attributes[7][1][0]): # <=50k
            b_bawah[1]+=1

# https://www.geeksforgeeks.org/python-multiply-numbers-list-3-different
def multiplyList(myList) : 
    result = 1
    for x in myList: 
         result = result * x  
    return result  

def main():
    importTrain()
    getProbsBawah()
    getProbs(0, 0)
    importTest()
    csv_writer()
    # print(attributes[7][0][1])
    # for attribute in attributes:
    #     print(attribute)        

if __name__ == "__main__":
    main()
