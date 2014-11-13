import copy

class Rank:
    
    def __init__(self, fpredict, frank):
        self.fpredict = fpredict
        self.frank = frank
        self.predict = []
        self.read_predict()
        self.userNum = len(self.predict)
        self.itemNum = len(self.predict[0])
        self.rank = []
        self.get_rank()
        self.save_rank()
        
    def read_predict(self):
        Fpredict = open(self.fpredict, 'r')
        predict = self.predict
        for line in Fpredict:
            scores = line.strip().split(",")
            scores = [float(s) for s in scores]
            predict.append(scores)
        Fpredict.close()
        
    def get_rank(self):
        predict = self.predict
        for user_i in range(self.userNum):
            tmp_predict = predict[user_i]
            tmp_rank, tmp_vals = self.rank_index(tmp_predict)
            self.rank.append(tmp_rank)
    
    def rank_index(self, predict_list):
        rank_list = []
        rank_vals = []
        sort_list = sorted(set(predict_list), reverse=True)
        for val in sort_list:
            for r_i in range(len(predict_list)):
                if predict_list[r_i] == val:
                    rank_list.append(r_i)
                    rank_vals.append(val)
        return rank_list, rank_vals
    
    def save_rank(self):
        Frank = open(self.frank, 'w')
        rank = self.rank
        for rank_list in rank:
            rank_list_str = [str(r) for r in rank_list] 
            rank_str = ",".join(rank_list_str)
            line = rank_str + "\n"
            Frank.write(line)
        Frank.close()
    
if __name__ == "__main__":
    froot =  "E:\\workspace\\MF\\data\\cross\\"
    fpredict = froot + "300_30_20_0.1_0.1_MAP_test_predict.dat0"
    frank = froot + "MAPRank.dat0"
    rank = Rank(fpredict, frank)
    print "finished"
        