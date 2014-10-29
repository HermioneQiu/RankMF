class KNN:
    def __init__(self, ftrain, userNum, itemNum, K, fsimi, frecommend):
        self.ftrain = ftrain
        self.userNum = userNum
        self.itemNum = itemNum   
        self.K = K     
        self.fsimi = fsimi
        self.frecommend = frecommend
        
        self.userBasket = {}
        self.read_userBasket()
        print "get userBasket"
        self.itemBasket = {}
        self.get_itemBasket()
        print "get itemBasket"

        self.simi = []
        self.simi_rank_K = []
        self.simi_rank_K_val = {}
        # init simi
        self.init()
        self.get_simi()
        print "set simi"
        self.get_simi_rank_K()
        print "get rank K of simi"

        self.recommend = {}
        self.get_recommend()
        print "get recommend"
#         self.save_recommend()
        
    def read_userBasket(self):
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
        
    def get_itemBasket(self):
        userBasket = self.userBasket
        itemBasket = self.itemBasket
        for user_i in userBasket.keys():
            item_set = userBasket[user_i]
            for item_i in item_set:
                if item_i in itemBasket.keys():
                    itemBasket[item_i].append(user_i)
                else:
                    itemBasket[item_i] = [user_i]
                    
    def init(self):
        self.simi = [[0 for i in range(self.itemNum)] for j in range(self.itemNum)]
        
    def get_simi(self):  
        simi = self.simi
        print len(simi)
        print len(simi[0])
        itemBasket = self.itemBasket
        for item_i in itemBasket.keys():
            for item_j in itemBasket.keys():
                user_set_i = itemBasket[item_i]
                user_set_j = itemBasket[item_j]
                cor_num = self.cal_simi(user_set_i, user_set_j)
                simi[item_i][item_j] = cor_num
                simi[item_j][item_i] = cor_num
                
    def cal_simi(self, user_set_i,user_set_j):
        cor_num = 0
        for user_i in user_set_i:
            if user_i in user_set_j:
                cor_num += 1
        return cor_num
        
    def get_recommend(self):
        K = self.K
        recommend = self.recommend
        simi_rank_K = self.simi_rank_K
        simi_rank_K_val = self.simi_rank_K_val
        for user_i in self.userBasket.keys():
            print "user_i: ",user_i
            tmp_recommend = {}
            item_list = self.userBasket[user_i]
            print item_list
            for item_i in item_list:
                simi_items = simi_rank_K[item_i]
                simi_items_val = simi_rank_K_val[item_i]
#                 print "simi old: ", simi_items
                simi_items = self.remove_dul(simi_items, item_list)
#                 print "simi new: ",simi_items
                for item_j in simi_items:
                    if item_j not in tmp_recommend.keys():
                        tmp_recommend[item_j] = simi_items_val[item_j]
            recommend[user_i] = tmp_recommend
            if user_i >= 10:
                break
            print recommend[user_i]
            
    def remove_dul(self, r_list, ref_list):
        n_list = []
        for l in r_list:
            if l not in ref_list:
                n_list.append(l)
        return n_list  
         
    def get_simi_rank_K(self):   
        K = self.K
        simi = self.simi
        simi_rank_K = self.simi_rank_K
        simi_rank_K_val = self.simi_rank_K_val
        
        for item_i in range(self.itemNum):
            tmp_simi_rank_K_val = {}
            simi_list = simi[item_i]
            simi_rank_index, simi_rank_vals = self.rank_index(simi_list)
            tmp_simi_rank_K = simi_rank_index[0:K]
            for i in range(K):
                tmp_simi_rank_K_val[simi_rank_index[i]] = simi_rank_vals[i]
            simi_rank_K.append(tmp_simi_rank_K)
            simi_rank_K_val[item_i]=tmp_simi_rank_K_val
            
    def rank_index(self, List):
        rank_list = []
        rank_vals = []
        sort_list = sorted(set(List), reverse=True)
        for val in sort_list:
            for r_i in range(len(List)):
                if List[r_i] == val:
                    rank_list.append(r_i)
                    rank_vals.append(val)
        return rank_list, rank_vals
    
    def save_recommend(self):
        Frecommend = open(self.frecommend, 'w')
        recommend = self.recommend
        for user_i in self.userBasket.keys():
            List = recommend[user_i]
            list_str = [str(item_i) for item_i in List]
            line_str = str(user_i) + "\t" + ','.join(list_str) + "\n"
            Frecommend.write(line_str)
        Frecommend.close()
            
if __name__ == "__main__":
    froot = "E:\\workspace\\MF\\data\\cross\\"
    ftrain = froot + "train.dat0"
    ftest = froot + "test.dat0"
    userNum = 200
    itemNum = 200
    K = 5
    fsimi = froot + "cf_simi.dat"
    frecommend = froot + "cf_recommend.dat"
    knn = KNN(ftrain, userNum, itemNum, K, fsimi, frecommend)
         
         
        
        