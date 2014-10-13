import copy

class MFRecommend:
    def __init__(self, fpredict, frecommend, K):
        self.fpredict = fpredict
        self.frecommend = frecommend
        self.predict = [] 
        self.readPredict()
        self.recommend = []
        # for test
        self.score = []
        self.userNum = len(self.predict)
        self.itemNum = len(self.predict[0])
        # recommend and save if result is right
        # 1. recommend
        ret = self.recommendAll(K)
        # 2. remove items in the userBasket
        if (ret == 1):
            print "recommend process error"
            return
        self.saveRecommend()
        
    def readPredict(self):
        predict = self.predict
        Fpredict = open(self.fpredict, "r")
        for line in Fpredict:
            parts = line.strip().split(",")
            parts = [float(p) for p in parts]
            predict.append(parts)
        Fpredict.close()
    
    def recommendAll(self, K):
        recommend = self.recommend
        predict = self.predict
        for user_i in range(len(predict)):
            userList = predict[user_i]
            # getTopK
            tmpRecommend, tmpScore = self.getTopK(userList, K)
#             print tmpRecommend
            if(tmpRecommend != 1):
                recommend.append(tmpRecommend)
                self.score.append(tmpScore)
        if (len(recommend) != self.userNum):
            print "len of recommend is: ", len(recommend)
            return 1
                
    def getTopK(self, List, K):
        recommend = []
        score = []
#         ListBak = copy.deepcopy(List)
        sortList = sorted(List, reverse=True)
        if (len(List) != len(sortList)):
            print "len of sorted list is: ",len(sortList)
            return 1;
        for l in sortList[:K]:
            pos = List.index(l)
            List[pos] = -1
            recommend.append(pos)   
            score.append(str(pos)+":"+str(l))
        return recommend, score

    def saveRecommend(self):
        Frecommend = open(self.frecommend, 'w')
        recommend = self.recommend
        for user_i in range(len(recommend)):
            line = recommend[user_i]
            line = [str(l) for l in line]
            lineStr = str(user_i)+"\t"+",".join(line) + "\n"
            Frecommend.write(lineStr)
        Frecommend.close()
    # for recommend result test
    
    def saveScoreRecommend(self, fscore):
        Fscore = open(fscore, 'w')
        score = self.score
        for user_i in range(len(score)):
            line = score[user_i]
            line = [str(l) for l in line]
            lineStr = str(user_i)+"\t"+",".join(line) + "\n"
            Fscore.write(lineStr)
        Fscore.close()
if __name__ == "__main__":
    rootDir = "E:\\workspace\\MF\\data\\"
    fpredict = rootDir + "predict.dat"
    frecommend = rootDir +  "MFrecommend.dat"
    K = 15
    mf = MFRecommend(fpredict, frecommend, K)
    fscore = rootDir + "MFscore.dat"
    mf.saveScoreRecommend(fscore)   
        
            
        