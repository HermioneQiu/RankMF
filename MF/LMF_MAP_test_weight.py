# --- binary ratings ----
# the item_id == item_index, so it remove the burden of build item_dict and user_dict
import random
from utils.coms import *
import math  
import copy

class LMF:
    
    def __init__(self, ftrain, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate, alpha, beta):
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
        
        self.trainItemBasket = {}
        self.getTrainItemBasket()
        
        self.alpha = alpha
        self.beta = beta
        self.bias_matrix = []
        self.calc_bias()
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
        self.predict = [[random.random() for i in range(itemNum)] for j in range(userNum)]
        self.trainMatrix = [[0 for i in range(itemNum)] for j in range(userNum)]
        
    def getTrainItemBasket(self):  
        trainUserBasket = self.userBasket
        trainItemBasket = self.trainItemBasket
        
        for user_i in trainUserBasket.keys():
            item_list = trainUserBasket[user_i]
            for item_i in item_list:
                if item_i in trainItemBasket.keys():
                    trainItemBasket[item_i].append(user_i)
                else:
                    trainItemBasket[item_i] = [user_i]    
                    
    def calc_bias(self):
        trainItemBasket = self.trainItemBasket
        trainUserBasket = self.userBasket
        bias_matrix = self.bias_matrix
        bias_matrix = [[0 for i in range(self.itemNum)] for j in range(self.userNum)]
        userNum = self.userNum
        itemNum = self.itemNum
        alpha =self.alpha
        beta = self.beta
        
        for user_i in range(self.userNum):
            item_num = 0
            if user_i in trainUserBasket.keys():
                item_num = len(trainUserBasket[user_i])
            for item_i in range(self.itemNum):
                user_num = 0
                if item_i in trainItemBasket.keys():
                    user_num = len(trainItemBasket[item_i])
                tmp = alpha*(float(user_num)/userNum) + beta * (float(item_num)/itemNum)
                
                bias_matrix[user_i][item_i] = self.remove_tail(tmp)
        self.bias_matrix = bias_matrix
            
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
        userBasket = self.userBasket
        bias_matrix = self.bias_matrix
        
        for user_i in range(userNum):
            if user_i not in userBasket.keys():
#                 print "no item for user: ", user_i
                continue
#             print userBasket[user_i]
            oldUserF = copy.deepcopy(userF)
            oldItemF = copy.deepcopy(itemF)
            # 1.update user_vector
            for f_i in range(F):
                user_delta = 0
                pos_items = self.abstract_pos(trainMatrix[user_i])
                neg_items = self.abstract_neg(trainMatrix[user_i])        
#                 print pos_items
                # 1.1 for positive examples
                for item_i in pos_items:
                    p_val_i = self.predictone(user_i, item_i)
                    user_delta += self.sigmoid(-p_val_i)*itemF[item_i][f_i]
                    # for all examples
                    for item_j in range(itemNum):
                        p_val_j = self.predictone(user_i, item_j)
#                         print p_val_i, p_val_j
                        if abs(p_val_i - p_val_j) < 1e-3:
                            continue
                        user_delta += self.sigmoid(p_val_j - p_val_i)*(itemF[item_i][f_i] - itemF[item_j][f_i])
                user_delta -= regularRate*userF[user_i][f_i]
#                 userF[user_i][f_i] += learnRate*user_delta
                userF[user_i][f_i] += ( 1/float(len(userBasket[user_i]) * itemNum) ) * learnRate * user_delta
                
            # 2. update item_vector
            # 2.1 for positive examples
            for item_i in pos_items:
                p_val_i = self.predictone(user_i, item_i)
                for f_i in range(F):
                    item_delta = 0
                    item_delta += self.sigmoid(-p_val_i)*userF[user_i][f_i] 
                    # for positive
                    for item_j in pos_items:
                        p_val_j = self.predictone(user_i, item_j)
                        if abs(p_val_i - p_val_j) < 1e-3:
                            continue
                        item_delta -= self.sigmoid(p_val_j - p_val_i) * oldUserF[user_i][f_i]
                    # for all
                    for item_k in range(itemNum):
                        p_val_k = self.predictone(user_i, item_k)
                        if abs(p_val_i - p_val_k) < 1e-3:
                            continue
                        item_delta += self.sigmoid(p_val_k - p_val_i) * oldUserF[user_i][f_i]
                        
                    item_delta -= regularRate*itemF[item_i][f_i]
                    itemF[item_i][f_i] += ( 1/float(len(userBasket[user_i])) ) * learnRate*item_delta
                     # 0. for weight optimization
                    item_delta = 2 * bias_matrix[user_i][item_i] * self.sigmoid(p_val_i) * self.dsigmoid(p_val_i) * oldUserF[user_i][f_i]
                    itemF[item_i][f_i] += learnRate * item_delta 
                    user_delta = 2 * bias_matrix[user_i][item_i] * self.sigmoid(p_val_i) * self.dsigmoid(p_val_i) * oldItemF[item_i][f_i]
                    userF[user_i][f_i] == learnRate * user_delta
                    
            # 2.2 for negative examples
            for item_i in neg_items:
                p_val_i = self.predictone(user_i, item_i)
                for f_i in range(F):
                    item_delta = 0
                    for item_j in pos_items:
                        p_val_j = self.predictone(user_i, item_j)
                        if abs(p_val_i - p_val_k) < 1e-3:
                            continue
                        item_delta -= self.sigmoid(p_val_j - p_val_i) * oldUserF[user_i][f_i]
                    
                    item_delta -= regularRate*itemF[item_i][f_i]
                    itemF[item_i][f_i] += ( 1/float(itemNum) ) * learnRate*item_delta
                     # 0. for weight optimization
                    item_delta = 2 * bias_matrix[user_i][item_i] * (self.sigmoid(p_val_i)-1) * self.dsigmoid(p_val_i) * oldUserF[user_i][f_i]
                    itemF[item_i][f_i] += learnRate * item_delta 
                    user_delta = 2 * bias_matrix[user_i][item_i] * (self.sigmoid(p_val_i)-1) * self.dsigmoid(p_val_i) * oldItemF[item_i][f_i]
                    userF[user_i][f_i] == learnRate * user_delta
                                     
    # **** functions used by SGD ******
    def sigmoid(self, x):
        return 1/(1+math.exp(-x))
    
    def dsigmoid(self, x):
        return math.exp(-x)/pow(1+math.exp(-x),2)     
                   
    def train(self):
        learnRate = self.learnRate
        regularRate = self.regularRate
        for iret_i in range(self.max_iretate):
            print "iret_i: ", iret_i
            self.MAP_SGD(learnRate, regularRate)
            # update all predict data before calculate errors
            self.predictAll()
            train_MAP = self.MAP_for_train()
            print "train error: ", train_MAP
            
# MAP version 1  
#     def MAP_for_train(self):
#         trainMatrix = self.trainMatrix
#         predict = self.predict
#         userNum = len(predict)
#         itemNum = self.itemNum
#         MAP = 0
#         for user_i in range(userNum):
#             pos_items = self.abstract_pos(trainMatrix[user_i])
#             if len(pos_items) == 0:
#                 userNum -= 1
#                 continue
#             tmp_MAP = 0
#             for item_i in pos_items:
#                 tmp_MAP += math.log(self.sigmoid(predict[user_i][item_i]) )
#                 for item_j in range(itemNum):
#                     tmp_MAP += math.log(self.sigmoid( predict[user_i][item_i]-predict[user_i][item_j] ) )
#             MAP += tmp_MAP
#         MAP = MAP/float(userNum)
#         return MAP
    
# MAP version 2
    def MAP_for_train(self):
        trainMatrix = self.trainMatrix
        predict = self.predict
        userNum = len(predict)
        itemNum = self.itemNum
        MAP = 0
        none_num = 0
        
        tmp_MAP_base = 0
        tmp_MAP_weight = 0
        for user_i in range(userNum):
            pos_items = self.abstract_pos(trainMatrix[user_i])
            neg_items = self.abstract_neg(trainMatrix[user_i])
            if len(pos_items) == 0:
                none_num -= 1
                continue
            # 1. for positive ones
            for item_i in pos_items:
                tmp_MAP_base += math.log( self.sigmoid(predict[user_i][item_i]) )
                for item_j in range(itemNum):
                    tmp_MAP_base += math.log( self.sigmoid(predict[user_i][item_i] - predict[user_i][item_j]) )
                tmp_MAP_weight += self.sigmoid(predict[user_i][item_i])
            # 2. for negative ones
            for item_i in neg_items:
                tmp_MAP_weight += self.sigmoid(1 - predict[user_i][item_i])
        tmp_MAP_base = tmp_MAP_base/(float((userNum - none_num) * (len(pos_items) + itemNum)))
        tmp_MAP_weight = tmp_MAP_weight/(float(userNum*itemNum) )
        MAP = tmp_MAP_base + tmp_MAP_weight
        
        print "map_base: ", tmp_MAP_base     
        print "map_weight:", tmp_MAP_weight
        return MAP               
#     def MAP_for_test(self):
    
    def abstract_pos(self, List):              
        new_list = []
        for l_i in range(len(List)):
            if List[l_i] == 1:
                new_list.append(l_i)
        return new_list
    
    def abstract_neg(self, List):
        new_list = []
        for l_i in range(len(List)):
            if List[l_i] != 1:
                new_list.append(l_i)
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
        
    def remove_tail(self, raw_dat):
        new_dat = float(int(raw_dat * 10000))/10000
        return new_dat   
     
    # cost function to judge iretation process
#     def cost(self):        
        
if __name__ == "__main__":
    froot = "E:\\workspace\\MF\\data\\cross\\"
    ftrain = froot + "train.dat0"
    ftest = froot + "test.dat0"
    userNum = 50
    itemNum = 50
    F = 10
    max_iretate = 20
    learnRate = 0.1
    regularRate = 0.1
    # user aspect
    alpha = 0.2
    # item aspect
    beta = 0.1
    para_str = str(userNum) +"_"+str(F)+"_"+str(max_iretate)+"_"+str(learnRate)+"_"+str(regularRate)
    fpredict = froot + para_str + "_MAP_test_weight_predict.dat0"
    # --- train ---
    lmf = LMF(ftrain, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate, alpha, beta)    
    # --- get predict ---
    print "finished"
    
    
        