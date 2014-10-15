import random
from utils.coms import *
import math  
import copy

class iMF:
    def __init__(self, ftrain, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate):
        self.train = ftrain
        self.test = ftest
        self.fpredcit = fpredict
        self.userNum = userNum
        self.itemNum = itemNum
        self.F = F
        self.max_iretate = max_iretate
        self.regularRate = regularRate
        self.learnRate = learnRate
        # 0. initial parameters
        self.userF = []
        self.itemF = []
        self.predict = []
        self.trainMatrix = []
        self.initial()
                
        # 1. read trainMatrix
        self.readTrainMatrix()
        
        # 2. train
        self.train()
        self.predictAll()
        self.savePredict(fpredict)
        # 3. evaluate
        self.userBasket = {}
        self.testUserBasket = {}
        self.negUserBasket = {}
        # 3.1 read userBasket
        
        # 3.2 read testUserBasket
        
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
#         print "origin: ",userBasket[0]
    def readTestUserBasket(self):
        Ftest = open(self.ftest, 'r')
        testUserBasket = self.testUserBasket
        for line in Ftest:
            userId, itemId_str = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemId_str.strip().split(",")
            itemIds = [int(itemId) for itemId in itemIds]
            testUserBasket[userId] = itemIds
        Ftest.close()
#         print "test: ", testUserBasket[0]
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
            
    def train(self):
        learnRate = self.learnRate
        regularRate = self.regularRate
        for iret_i in range(self.max_iretate):
            print "iret_i: ", iret_i
            self.RMSE_SGD(learnRate, regularRate)
            # update all predict data before calculate errors
            self.predictAll()
            train_MAP = self.MAP_for_train()
            print "train MAP error: ", train_MAP
            train_RMSE = self.RMSE_for_train()
            print "train RMSE error: ", train_RMSE
            
#     def RMSE_SGD(self):
        
    def MAP_for_train(self):
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
                tmp_MAP += math.log( self.sigmod(predict[user_i][item_i]) )
                for item_j in range(itemNum):
                    tmp_MAP += math.log( 2 - self.sigmod(predict[user_i][item_j] - predict[user_i][item_i]) )
            MAP += tmp_MAP
        MAP = MAP/float(userNum)
        return MAP    
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
                
    def saveModel(self, fUserF, fItemF):
        saveMatrix(fUserF, self.userF)
        saveMatrix(fItemF, self.itemF)    
                
    def savePredict(self, fresult):
        Fresult = open(fresult, "w")
        predict = self.predict
        for user_i in range(self.userNum):
            userRate = predict[user_i]
            userRate = [str(u) for u in userRate]
            lineStr = ",".join(userRate)+"\n"
            Fresult.write(lineStr)
        Fresult.close()   
        
    