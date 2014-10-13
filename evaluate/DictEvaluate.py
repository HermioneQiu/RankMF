import math

class RSME:
    def __init__(self, fpredict, ftrain):
        self.fpredict = fpredict
        self.ftrain = ftrain
        self.predictUserDict = dict()
        self.trainUserDict = dict()
        self.readTrainDict()
        self.readPredictDict()
        
    def readTrainDict(self):
        Ftrain = open(self.ftrain,"r")
        trainUserDict = self.trainUserDict
        for line in Ftrain:
            user, items = line.strip().split("\t")
            user = int(user)
            items = items.split(",")
            items = [int(t) for t in items]
            trainUserDict[user] = items
        Ftrain.close()
        
    def readPredictDict(self):
        Fpredict = open(self.fpredict, "r")
        predictUserDict = self.predictUserDict
        for line in Fpredict:
            p_len = len(predictUserDict)
            line = line.strip().split(",")
            line = [float(l) for l in line]
            predictUserDict[p_len] = line
        Fpredict.close()
    
    def rsme(self):
        predictUserDict = self.predictUserDict
        trainUserDict = self.trainUserDict
        rsme = 0
        num = 0
        for user_i in trainUserDict.keys():
            for item_i in trainUserDict[user_i]:
                o_score = 1
                p_score = predictUserDict[user_i][item_i]
                rsme += math.sqrt(abs(p_score - o_score))
            num += len(trainUserDict[user_i])
        rsme = rsme/num
        print rsme
        return rsme
    
class PR:
    def __init__(self, fprobe, ftest):
        self.fprobe = fprobe
        self.ftest = ftest
        self.testUserDict = self.readDict(ftest)
        self.probeUserDict = self.readDict(fprobe)
        self.pr()
        
    def readDict(self,fname):
        Fname = open(fname, "r")
        Dict = {}
        for line in Fname:
            start, ends = line.strip().split("\t")
            start = int(start)
            ends = ends.strip().split(",")
            ends = [int(e) for e in ends]
            Dict[start] = ends
        Fname.close()
        return Dict
    
    def pr(self):
        testUserDict = self.testUserDict
        probeUserDict = self.probeUserDict
        preciseNum = 0
        correctNum = 0
        recallNum = 0
        for user_i in testUserDict.keys():
            recallNum += len(testUserDict[user_i])
            if user_i in probeUserDict.keys():
                testSet = testUserDict[user_i]
                probeSet = probeUserDict[user_i]
                for item in probeSet:
                    if item in testSet:
                        correctNum += 1
        for user_i in probeUserDict.keys():
            preciseNum += len(probeUserDict[user_i])
        preciseRate = float(correctNum)/preciseNum
        recallRate = float(correctNum)/recallNum
        print preciseRate, recallRate
        return preciseRate, recallRate
