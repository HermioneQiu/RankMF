# --- binary ratings ----
# the item_id == item_index, so it remove the burden of build item_dict and user_dict
import random
from utils.coms import *
import math  
import copy

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
        self.getNegUserBasket()
        
        self.readTestUserBasket()
        
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
#         print "neg:",negUserBasket[0]
        
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
                    
    def train(self):
        learnRate = self.learnRate
        regularRate = self.regularRate
        for iret_i in range(self.max_iretate):
            print "iret_i: ", iret_i
            self.MAP_SGD(learnRate, regularRate)
            train_MAP = self.MAP_for_train()
            print "train error: ", train_MAP
            
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
                    tmp_MAP += math.log( 1 - self.sigmod(predict[user_i][item_j] - predict[user_i][item_i]) )
            tmp_MAP = tmp_MAP/len(pos_items)
            MAP += tmp_MAP
        MAP = MAP/float(userNum)
        return MAP    
                       
#     def MAP_for_test(self):
    
    def abstract_pos(self, List):              
        new_list = []
        for i in List:
            if i == 1:
                new_list.append(i)
        return new_list
            
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
    regularRate = 0.01
    # --- train ---
    lmf = LMF(ftrain, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate)    
    # --- get predict ---
    print "finished"
    
    
        