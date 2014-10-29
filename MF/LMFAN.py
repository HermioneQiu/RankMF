# --- binary ratings ----
# the item_id == item_index, so it remove the burden of build item_dict and user_dict
import random
from utils.coms import *
import math

class LMF:
    
    def __init__(self, ftrain, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate):
        self.ftrain = ftrain
        self.ftest = ftest
        self.F = F
        self.max_iretate = max_iretate
        self.learnRate = learnRate
        self.regularRate = regularRate
        self.userNum = userNum
        self.itemNum = itemNum
        # initial userF and itemF
        self.userF = []
        self.itemF = []
        # no rating, only binary, so no bias
        self.predict = []
        self.trainMatrix = []
        self.initial()
        
        self.userBasket = {}
        self.testUserBasket = {}
        self.negUserBasket = {}
        
        self.readTrainMatrix()
        
        self.readUserBasket()
        self.readTestUserBasket()
        self.getNegUserBasket()
        
#         self.OCCF_user()
        
        # ---train---
        self.train()
        # ---get predict---
        self.predictAll()
        self.savePredict(fpredict)
        
    def initial(self):
        userNum = self.userNum
        itemNum = self.itemNum
        F = self.F
        self.userF = [[random.random()/math.sqrt(F) for i in range(self.F)] for i in range(userNum)]
        self.itemF = [[random.random()/math.sqrt(F) for f_i in range(self.F)] for i in range(itemNum)]
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
                
    def readUserBasket(self):
        userBasket = self.userBasket
        Ftrain = open(self.ftrain, "r")
        line = Ftrain.readline()
        while line:
            userId, itemId_str = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemId_str.strip().split(",")
            itemIds = [int(itemId) for itemId in itemIds]
            userBasket[userId] = itemIds
            line = Ftrain.readline()
        Ftrain.close()
        
    def OCCF_user(self):
        trainMatrix = self.trainMatrix
        userBasket = self.userBasket
        userNum = self.userNum
        itemNum = self.itemNum
        for user_i in range(userNum):
            if user_i in userBasket.keys():
                num_item = len(userBasket[user_i])
                # need to be redefined ***
                weight_user = 1 - float(num_item)/itemNum
                for item_i in range(itemNum):
                    if trainMatrix[user_i][item_i] == 0:
                        trainMatrix[user_i][item_i] = weight_user
                    
    def train(self):
        learnRate = self.learnRate
        regularRate = self.regularRate
        for iret_i in range(self.max_iretate):
            print "iret_i: ", iret_i
            self.SGD(learnRate, regularRate)
            trainMRSE = self.MRSE_function()
            print "train error: ", trainMRSE
            test_posMRSE = self.MRSE_for_test_pos()
            print "test_pos error: ", test_posMRSE
            test_negMRSE = self.MRSE_for_test_neg()
            print "test_neg error:", test_negMRSE
            
    def MRSE_function(self):   
        MRSE = 0
        userNum = self.userNum
        itemNum = self.itemNum
        trainMatrix = self.trainMatrix
        for user_i in range(userNum):
            for item_i in range(itemNum):
                tmp = math.sqrt(math.pow((trainMatrix[user_i][item_i]- self.predict[user_i][item_i]), 2))
#                 print tmp, ":",trainMatrix[user_i][item_i], ":",self.predictone(user_i, item_i)
                MRSE += tmp
        return MRSE/(userNum * itemNum)
    
    def SGD(self, learnRate, regularRate):
        trainMatrix = self.trainMatrix
        predict = self.predict
        userF = self.userF
        itemF = self.itemF
        userNum = len(trainMatrix)
        itemNum = len(trainMatrix[0])
        for user_i in range(userNum):
#             pos_items = self.abstract_pos(trainMatrix[user_i])
            for item_i in range(itemNum):
                predict[user_i][item_i] = self.predictone(user_i, item_i)
                err = trainMatrix[user_i][item_i] - self.predict[user_i][item_i]
                for f_i in range(self.F):
                    oldUserF = userF[user_i][f_i]
                    userF[user_i][f_i] += learnRate * (2*err*itemF[item_i][f_i] - regularRate*userF[user_i][f_i]) 
                    itemF[item_i][f_i] += learnRate * (2*err*oldUserF - regularRate*itemF[item_i][f_i])
                    
    def readTestUserBasket(self):
        Ftest = open(self.ftest, 'r')
        testUserBasket = self.testUserBasket
        for line in Ftest:
            userId, itemId_str = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemId_str.strip().split(",")
            itemIds = [int(itemId) for itemId in itemIds]
            testUserBasket[userId] = itemIds
            
    def MRSE_for_test_pos(self):
        MRSE = 0
        testUserBasket = self.testUserBasket
        item_num = 0
        for user_i  in testUserBasket.keys():
            item_ids = testUserBasket[user_i]
            item_num += len(item_ids)
            for item_i in item_ids:
                MRSE += math.sqrt(math.pow((1 - self.predict[user_i][item_i]), 2))
        return MRSE/item_num
    
    def MRSE_for_test_neg(self):  
        MRSE = 0          
        negUserBasket = self.negUserBasket
        item_num = 0
        for user_i in negUserBasket.keys():
            n_items = negUserBasket[user_i]
            item_num += len(n_items)
            for item_i in n_items:
                MRSE += math.sqrt(math.pow((self.predict[user_i][item_i]), 2))
        return MRSE/item_num
                
    def getNegUserBasket(self):
        trainUserBasket = self.userBasket
        testUserBasket = self.testUserBasket
        userNum = self.userNum
        itemNum = self.itemNum
        negUserBasket = self.negUserBasket
        for user_i in range(userNum):
            n_items = []
            t_items = []
            if user_i in trainUserBasket.keys():
                tr_items = trainUserBasket[user_i]
            te_items = []
            if user_i in testUserBasket.keys():
                te_items = testUserBasket[user_i]  
                
            for item_i in range(itemNum):
                if (item_i not in te_items ) & (item_i not in tr_items):
                    n_items.append(item_i)
            negUserBasket[user_i] = n_items
                
    def abstract_pos(self, List):              
        new_list = []
        for i in List:
            if i == 1:
                new_list.append(i)
        return new_list
            
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
    
#     def batchGD(self):
#     def predict(self, userId): 
        # sort and get K result
    def predictAll(self):
        predict = self.predict
        for user_i in range(self.userNum):
#             print "user_i: ",user_i
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
    userNum = 200
    itemNum = 200
    F = 20
    max_iretate = 20
    learnRate = 0.01
    regularRate = 0.1
    fpredict = froot +str(userNum)+ "_AN_LMF_predict.dat0"
    # --- train ---
    lmf = LMF(ftrain, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate)    
    # --- get predict ---
    print "finished"
    
        