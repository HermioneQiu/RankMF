class Precise:
    
    def __init__(self, ftest, ftrain, frank, frank_new):
        self.ftest = ftest
        self.frank = frank
        self.ftrain = ftrain
        self.frank_new = frank_new
        self.testUserBasket = dict()
        self.read_testUserBasket()
        self.trainUserBasket = dict()
        self.read_trainUserBasket()
#         print self.trainUserBasket[0]
        self.rank = []
        self.read_rank()
#         print self.rank[0]
        self.rank = self.remove_train()
        self.save_new_rank()
#         print "new_rank: ", self.rank[0]
        precise_at_5 = self.Precise_at_five()
        print precise_at_5
        
    def read_trainUserBasket(self):
        Ftrain = open(self.ftrain, 'r')
        trainUserBasket = self.trainUserBasket
        for line in Ftrain:
            userId, itemId_str = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemId_str.strip().split(",")
            itemIds = [int(itemId) for itemId in itemIds]
            trainUserBasket[userId] = itemIds
        Ftrain.close()
                
    def read_testUserBasket(self):
        Ftest = open(self.ftest, 'r')
        testUserBasket = self.testUserBasket
        for line in Ftest:
            userId, itemId_str = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemId_str.strip().split(",")
            itemIds = [int(itemId) for itemId in itemIds]
            testUserBasket[userId] = itemIds
        Ftest.close()
    
    def read_rank(self):
        Frank = open(self.frank, 'r')
        rank = self.rank
        for line in Frank:
            indexs_str = line.strip().split(",")
            indexs = [int(r) for r in indexs_str]
            rank.append(indexs)
        Frank.close()
        
    def remove_train(self):   
        rank = self.rank
        new_rank = [[] for user_i in range(len(rank))]
        trainUserBasket = self.trainUserBasket
        for user_i in trainUserBasket.keys():
            train_list = trainUserBasket[user_i]
            rank_list = rank[user_i]
            tmp_rank_list = []
            for r in rank_list:
                if r not in train_list:
                    tmp_rank_list.append(r)
            new_rank[user_i] = tmp_rank_list
        return new_rank
    def save_new_rank(self):   
        rank = self.rank
        frank_new = open(self.frank_new, 'w')
        for rank_list in rank:
            rank_list = [str(r) for r in rank_list]
            rank_str = ",".join(rank_list)
            line = rank_str + "\n"
            frank_new.write(line)
        frank_new.close()
            
    def Precise_at_five(self):
        rank = self.rank
        testUserBasket = self.testUserBasket
        userNum = len(testUserBasket)
        precise = 0
        for user_i in testUserBasket.keys():
            cor_num = 0
            basket_items = testUserBasket[user_i]
            rank_items = rank[user_i]
            for i in range(10):
                if rank_items[i] in basket_items:
                    cor_num += 1
            tmp_precise = cor_num/float(len(basket_items))
            precise += tmp_precise
        precise = precise/userNum
        return precise
        
if __name__ == "__main__":
    froot = "E:\\workspace\\MF\\data\\cross\\"
    ftest = froot + "test.dat0"
    ftrain = froot + "train.dat0"
    frank =froot + "MAPRank.dat0"
    frank_new = froot + "Rank_new.dat0"
    precise = Precise(ftest, ftrain, frank, frank_new)
    