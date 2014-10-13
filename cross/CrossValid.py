# ---dataset epinions social networks----
# --- binary ratings ----
import random
import math

from utils.coms import *
#************attention*****************
# --- for calculation's convenience, userId and itemId are all integer
#**************************************
class CrossValid:
    
    def __init__(self, frate,ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate):
        self.frate = frate
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
#         self.userBase = []
#         self.itemBase = []
        self.predict = []
        # 1. intial all parameters.
        self.initial()
        # 2. read all userRates// can be different according to the file format of train files.
        # get userRate
        self.userRate = {}
        self.readUserRate()
        # 2.1 read testUserRates // 
        self.testUserRate = {}
        self.readTestUserRate()
        # ---train---
        # 3.train by the choose (k-1) set.
        self.trainCost, self.testCost = self.train()
        # ---get predict---
#         self.predict(user_i, item_i)
        # 4. predict according to train result.
        self.predictAll()
        self.savePredict(fpredict)
        
    def initial(self):
        userNum = self.userNum
        itemNum = self.itemNum
        self.userF = [[random.random() for i in range(self.F)] for i in range(userNum)]
        self.itemF = [[random.random() for f_i in range(self.F)] for i in range(itemNum)]
        self.predict = [[0 for i in range(itemNum)] for j in range(userNum)]
        
    # read dict file: user_id\t item_id, item_id. item_id...
    def readTestUserRate(self):   
        testUserRate = self.testUserRate
        Ftest = open(self.ftest, "r")
        for line in Ftest:
            userId, itemIds = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemIds.split(",")
            itemIds = [int(t) for t in itemIds]
            testUserRate[userId] = itemIds
        Ftest.close()    
        
    # read dict file: user_id\t item_id, item_id, item_id...
    def readUserRate(self):
        userRate = self.userRate
        Frate = open(self.frate, "r")
        for line in Frate:
            userId, itemIds = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemIds.split(",")
            itemIds = [int(t) for t in itemIds]
            userRate[userId] = itemIds
        Frate.close()
        
    def train(self):
        userRate = self.userRate
        testUserRate = self.testUserRate
        trainCost = []
        testCost = []
        learnRate = self.learnRate
        regularRate = self.regularRate
        for iret_i in range(self.max_iretate):
            if iret_i%20 == 0:
                print "iret_i: ", iret_i
            self.SGD(learnRate, regularRate)
            self.learnRate *= 0.95
            tmp_train = self.costFunction(userRate)
            tmp_test = self.costFunction(testUserRate)
            tmp_str = "train: "+ str(tmp_train)+ ", test: "+str(tmp_test)
            print tmp_str
            trainCost.append(tmp_train)
            testCost.append(tmp_test)
        return trainCost, testCost
    
    def costFunction(self, Dict): 
        self.predictAll()
        predict = self.predict
        err = 0
        num = 0
        for userId in Dict.keys():
            itemIds = Dict[userId]
            num += len(itemIds)
            for itemId in itemIds:
#                 print userId, itemId
#                 print len(predict), len(predict[0])
                err += math.sqrt(abs(predict[userId][itemId]-1))
        return err/num
        
    def SGD(self, learnRate, regularRate):
        userRate = self.userRate
        userF = self.userF
        itemF = self.itemF
        for user_i in userRate.keys():
            items = userRate[user_i]
            for item_i in items:
                err = 1 - self.predictone(user_i, item_i)
                for f_i in range(self.F):
                    oldUserF = userF[user_i][f_i]
                    userF[user_i][f_i] += learnRate * (2*err*itemF[item_i][f_i] - regularRate*userF[user_i][f_i]) 
                    itemF[item_i][f_i] += learnRate * (2*err*oldUserF - regularRate*itemF[item_i][f_i])
                    
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

# if __name__ == "__main__":
#     froot = "E:\\workspace\\MF\\data\\cross\\"
#     frate = froot + "train.dat0"
#     fpredict = froot + "predict\\predict.dat"
#     userNum = 500
#     itemNum = 500
#     F = 50
#     max_iretate = 100
#     learnRate = 0.01
#     regularRate = 0.01
#     # K fold cross validate
#     K = 5
#     # --- train ---
#     lmf = CrossValid(frate, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate)    
#     # --- get predict ---
#     print "finished"
#     
        