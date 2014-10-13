# ---dataset epinions social networks----
# --- binary ratings ----
import random
from utils.coms import *

class LMF:
    
    def __init__(self, frate,fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate):
        self.frate = frate
        self.F = F
        self.max_iretate = max_iretate
        self.learnRate = learnRate
        self.regularRate = regularRate
        # read userDict, and itemDict
        # Dict{userId, user_i}
#         self.userDict = {}
#         self.itemDict = {}
#         self.revUserDict = {}
#         self.revItemDict = {}
#         self.readDict()
#         self.userNum = len(self.userDict)
#         self.itemNum = len(self.itemDict)
        self.userNum = userNum
        self.itemNum = itemNum
        # initial userF and itemF
        self.userF = []
        self.itemF = []
        # no rating, only binary, so no bias
#         self.userBase = []
#         self.itemBase = []
        self.predict = []
        self.initial()
        # get userRate
        self.userRate = {}
        self.readUserRate()
        # ---train---
        self.train()
        # ---get predict---
#         self.predict(user_i, item_i)
        self.predictAll()
        self.savePredict(fpredict)
        
    def initial(self):
        userNum = self.userNum
        itemNum = self.itemNum
        self.userF = [[random.random() for i in range(self.F)] for i in range(userNum)]
        self.itemF = [[random.random() for f_i in range(self.F)] for i in range(itemNum)]
        self.predict = [[0 for i in range(itemNum)] for j in range(userNum)]
        
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
            print "user_i: ",user_i
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
    froot = "E:\\workspace\\MF\\data\\"
    frate = froot + "train.dat"
    fpredict = froot + "MFpredict.dat"
    userNum = 500
    itemNum = 500
    F = 50
    max_iretate = 100
    learnRate = 0.01
    regularRate = 0.6
    # --- train ---
    lmf = LMF(frate, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate)    
    # --- get predict ---
    print "finished"
    
        