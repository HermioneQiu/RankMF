from evaluate.DictEvaluate import *

class CrossRecommend:
    def __init__(self, fpredict, ftrain, frecommend, K):
        self.fpredict = fpredict
        self.ftrain = ftrain
        self.frecommend = frecommend
        self.trainDict = dict()
        self.readTrain()
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
        
    def readTrain(self):
        trainDict = self.trainDict
        Ftrain = open(self.ftrain, "r")
        for line in Ftrain:
            userId, itemIds = line.strip().split("\t")
            userId = int(userId)
            itemIds = itemIds.split(",")
            itemIds = [int(t) for t in itemIds]
            trainDict[userId] = itemIds
    
    def removeTrainK(self, List, userId, K):
        tmpList = []
        trainDict = self.trainDict
        if userId in trainDict.keys():
            
            itemIds = trainDict[userId]
            for l in List:
                if (l not in itemIds)&(len(tmpList)<K):
                    tmpList.append(l)
        return tmpList
    
    def removeTrain(self, List, userId):
        tmpList = []
        trainDict = self.trainDict
        if userId in trainDict.keys():
            
            itemIds = trainDict[userId]
            for l in List:
                if (l not in itemIds):
                    tmpList.append(l)
        return tmpList
        
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
            tmpRecommend, tmpScore = self.getSort(userList)
#             print str(user_i)+": "+str(len(tmpRecommend))
            tmpRecommend = self.removeTrainK(tmpRecommend, user_i, K)
#             print tmpRecommend
#             print tmpRecommend
            recommend.append(tmpRecommend)
            self.score.append(tmpScore)
        if (len(recommend) != self.userNum):
            print "len of recommend is: ", len(recommend)
            return 1
                
    def getSort(self, List):
        recommend = []
        score = []
#         ListBak = copy.deepcopy(List)
        sortList = sorted(List, reverse=True)
        if (len(List) != len(sortList)):
            print "len of sorted list is: ",len(sortList)
            return 1;
        for l in sortList:
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
    rootDir = "E:\\workspace\\MF\\data\\cross\\"
    K = 1
    for k in range(K):
        fpredict = rootDir + "\\predict\\predict.dat"+str(k)
        frecommend = rootDir +  "result\\recommend.dat"+str(k)
        ftrain = rootDir + "train.dat"+str(k)
        ftest = rootDir + "test.dat" +str(k)
        recommend_num = 100
        mf = CrossRecommend(fpredict, ftrain, frecommend, recommend_num)
        fscore = rootDir + "score.dat"+str(k)
        mf.saveScoreRecommend(fscore)   
        pr = PR(frecommend, ftest)