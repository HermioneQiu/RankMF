import random
from utils.coms import *
from math import *
import copy

def g(x):
    """sigmoid function"""
    return 1/(1+exp(-x))

def dg(x):
    """derivative of sigmoid function"""
    return exp(x)/(1+exp(x))**2

# ---dataset epinions social networks----
# --- binary ratings ----

class CLIMF:
    
    def __init__(self, ftrain, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate):
        self.ftrain = ftrain
        self.ftest = ftest
        self.F = F
        self.max_iretate = max_iretate
        self.learnRate = learnRate
        self.regularRate = regularRate
        # read userDict, and itemDict
        self.userNum = userNum
        self.itemNum = itemNum
        # initial userF and itemF
        self.userF = []
        self.itemF = []
        # no rating, only binary, so no bias
        self.predict = []
        self.trainMatrix = []
        
        self.initial()
        
        self.readTrainMatrix()
        # *** weighted train matrix ****

        # ---train---
        self.train()
        # ---get predict---
#         self.predict(user_i, item_i)
        self.predictAll()
        self.savePredict(fpredict)
        
    def initial(self):
        userNum = self.userNum
        itemNum = self.itemNum
        F = self.F
        self.userF = [[random.random()/sqrt(F) for f_i in range(self.F)] for i in range(userNum)]
        self.itemF = [[random.random()/sqrt(F) for f_i in range(self.F)] for i in range(itemNum)]
        self.predict = [[0 for i in range(itemNum)] for j in range(userNum)]
        self.trainMatrix = [[0 for i in range(itemNum)] for j in range(userNum)]
        
    # complete train matrix
    def readTrainMatrix(self):
        # 0 for missing examples
        trainMatrix = self.trainMatrix
        Ftrain = open(self.ftrain, 'r')
        for line in Ftrain:
            userId, itemId_str = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemId_str.strip().split(",")
            itemIds = [int(itemId) for itemId in itemIds]
            for itemId in itemIds:
                trainMatrix[userId][itemId] = 1
        
    def train(self):
        learnRate = self.learnRate
        regularRate = self.regularRate
        for iret_i in range(self.max_iretate):
            print "iret_i: ", iret_i
            self.MAP_SGD(learnRate, regularRate)
            self.predictAll()
            MAP = self.train_MAP()
            print "MAP: ", MAP
        
    def train_MAP(self):
        trainMatrix = self.trainMatrix
        predict = self.predict
        userNum = len(predict)
        itemNum = self.itemNum
        MAP = 0
        for user_i in range(userNum):
            pos_items = self.abstract_pos(trainMatrix[user_i])
            if len(pos_items) == 0:
                userNum -= 1
                continue
            tmp_MAP = 0
            for item_i in pos_items:
                tmp_MAP += log( self.sigmod(predict[user_i][item_i]) )
                for item_j in range(itemNum):
                    tmp_MAP += log( 1 - self.sigmod(predict[user_i][item_j] - predict[user_i][item_i]) )
            tmp_MAP = tmp_MAP/len(pos_items)
            MAP += tmp_MAP
        MAP = MAP/float(userNum)
        return MAP
    
#     def test_MAP_function(self):
    def MAP_SGD(self, learnRate, regularRate):
        trainMatrix = self.trainMatrix
        userNum = len(trainMatrix)
        itemNum = len(trainMatrix[0])
        userF = self.userF
        itemF = self.itemF
        F = self.F
        

        for user_i in range(userNum):
            oldUserF = copy.deepcopy(userF)
            # 1.update user_vector
            for f_i in range(F):
                user_delta = 0
                pos_items = self.abstract_pos(trainMatrix[user_i])
                for item_i in pos_items:
                    p_val_i = self.predictone(user_i, item_i)
                    user_delta += self.sigmod(-p_val_i)*itemF[item_i][f_i]
                    for item_j in pos_items:
                        p_val_j = self.predictone(user_i, item_j)
                        user_delta += self.dsigmod(p_val_j - p_val_i)*(itemF[item_i][f_i] - itemF[item_j][f_i])/(1-self.sigmod(p_val_j - p_val_i))
                user_delta -= regularRate*userF[user_i][f_i]
                userF[user_i][f_i] += learnRate*user_delta
            
            for item_i in pos_items:
                p_val_i = self.predictone(user_i, item_i)
                # 2. update item_vector
                for f_i in range(F):
                    item_delta = 0
                    item_delta += self.sigmod(-p_val_i)*userF[user_i][f_i] 
                    for item_j in pos_items:
                        p_val_j = self.predictone(user_i, item_j)
                        item_delta += ( self.dsigmod(p_val_i - p_val_j)*( 1/(1-self.sigmod(p_val_j - p_val_i)) - 1/(1-self.sigmod(p_val_i - p_val_j)) ) )*userF[user_i][f_i]
                    item_delta -= regularRate*itemF[item_i][f_i]
                    itemF[item_i][f_i] += learnRate*item_delta
                    
    def abstract_pos(self, List):  
        new_list = []                  
        for i in List:
            if i == 1:
                new_list.append(i)
        return new_list
    
    # **** functions used by SGD ******
    def sigmod(self, x):
        return 1/(1+exp(-x))
    def dsigmod(self, x):
        return exp(-x)/pow(1+exp(-x),2)
    
    # **** ********************* ******               
    def saveModel(self, fUserF, fItemF):
        saveMatrix(fUserF, self.userF)
        saveMatrix(fItemF, self.itemF)
        
    def predictone(self, user_i ,item_i):
        userF = self.userF
        itemF = self.itemF
        rate = 0
        for f_i in range(self.F):
            rate += userF[user_i][f_i]*itemF[item_i][f_i]
        return rate
    
    def predictAll(self):
        predict = self.predict
        for user_i in range(self.userNum):
            for item_i in range(self.itemNum):
                predict[user_i][item_i] = self.predictone(user_i, item_i) 
                
    def savePredict(self, fresult):
        Fresult = open(fresult, "w")
        predict = self.predict
        for user_i in range(self.userNum):
            userRate = predict[user_i]
            userRate = [str(u) for u in userRate]
            lineStr = ",".join(userRate)+"\n"
            Fresult.write(lineStr)
        Fresult.close()
    # cost function to judge iretation process
#     def cost(self):        
        
if __name__ == "__main__":
    froot = "E:\\workspace\\MF\\data\\cross\\"
    ftrain = froot + "train.dat0"
    ftest = froot + "test.dat0"
    fpredict = froot + "MFpredict.dat0"
    userNum = 200
    itemNum = 200
    F = 50
    max_iretate = 20
    learnRate = 0.001
    regularRate = 0.1
    # --- train ---
    lmf = CLIMF(ftrain , ftest,fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate)    
    # --- get predict ---
    print "finished"
    
             