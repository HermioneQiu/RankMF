# --- binary ratings ----
# the item_id == item_index, so it remove the burden of build item_dict and user_dict
import random
from utils.coms import *
import math

class LMF:
    
    def __init__(self, ftrain,fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate):
        self.ftrain = ftrain
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
        
        self.readTrainMatrix()
        
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
                
    def OCCF(self):
        trainMatrix = self.trainMatrix
        
        
    def readUserRate(self):
        userRate = self.userRate
        Frate = open(self.frate, "r")
        line = Frate.readline()
        while line:
            userId, itemId = line.strip().split("\t")
            userId = int(userId)
            itemId = int(itemId)
            if userId not in userRate.keys():
                userRate[userId] = [itemId] 
            else:
                # the relationships in the dataset has no replicated.
                userRate[userId].append(itemId)
            line = Frate.readline()
        Frate.close()
        
    def train(self):
        learnRate = self.learnRate
        regularRate = self.regularRate
        for iret_i in range(self.max_iretate):
            print "iret_i: ", iret_i
            self.SGD(learnRate, regularRate)
            MRSE = self.MRSE_function()
            print "error: ", MRSE
            
    def MRSE_function(self):   
        MRSE = 0
        userNum = self.userNum
        itemNum = self.itemNum
        trainMatrix = self.trainMatrix
        for user_i in range(userNum):
            for item_i in range(itemNum):
                tmp = math.sqrt(math.pow((trainMatrix[user_i][item_i]- self.predictone(user_i, item_i)), 2))
#                 print tmp, ":",trainMatrix[user_i][item_i], ":",self.predictone(user_i, item_i)
                MRSE += tmp
        return MRSE/(userNum * itemNum)
    
    def SGD(self, learnRate, regularRate):
        trainMatrix = self.trainMatrix
        userF = self.userF
        itemF = self.itemF
        userNum = len(trainMatrix)
        itemNum = len(trainMatrix[0])
        for user_i in range(userNum):
#             pos_items = self.abstract_pos(trainMatrix[user_i])
            for item_i in range(itemNum):
                err = trainMatrix[user_i][item_i] - self.predictone(user_i, item_i)
                for f_i in range(self.F):
                    oldUserF = userF[user_i][f_i]
                    userF[user_i][f_i] += learnRate * (2*err*itemF[item_i][f_i] - regularRate*userF[user_i][f_i]) 
                    itemF[item_i][f_i] += learnRate * (2*err*oldUserF - regularRate*itemF[item_i][f_i])
                    
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
    fpredict = froot + "MFpredict.dat0"
    userNum = 200
    itemNum = 200
    F = 50
    max_iretate = 100
    learnRate = 0.001
    regularRate = 0.6
    # --- train ---
    lmf = LMF(ftrain, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate)    
    # --- get predict ---
    print "finished"
    
        