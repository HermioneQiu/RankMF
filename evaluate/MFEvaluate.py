import math

class MFPR:
    def __init__(self, fprobe, ftest):
        self.fprobe = fprobe
        self.ftest = ftest
        self.testUserDict = dict()
        self.probeUserDict = dict()
        self.readTestDict()
        self.readProbeDict()
        self.pr()
        
    def readTestDict(self):
        Ftest = open(self.ftest,"r")
        testUserDict = self.testUserDict
        for line in Ftest:
            start, end = line.strip().split("\t")
            start = int(start)
            end = int(end)
            if start not in testUserDict.keys():
                testUserDict[start] = [end]
            else:
                testUserDict[start].append(end)
        Ftest.close()
    
    def readProbeDict(self):
        Fprobe = open(self.fprobe, "r")
        probeUserDict = self.probeUserDict
        for line in Fprobe:
            start, ends = line.strip().split("\t")
            start = int(start)
            ends = ends.strip().split(",")
            ends = [int(e) for e in ends]
            probeUserDict[start] = ends
        Fprobe.close()
        
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

class MFRSME:
    def __init__(self, fpredict, ftrain):
        self.fpredict = fpredict
        self.ftrain = ftrain
        self.predictUserDict = dict()
        self.trainUserDict = dict()
        self.readTrainDict()
        self.readPredictDict()
        self.rsme()
        
    def readTrainDict(self):
        Ftrain = open(self.ftrain,"r")
        trainUserDict = self.trainUserDict
        for line in Ftrain:
            start, end = line.strip().split("\t")
            start = int(start)
            end = int(end)
            if start not in trainUserDict.keys():
                trainUserDict[start] = [end]
            else:
                trainUserDict[start].append(end)
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
    
if __name__ == "__main__":
    rootDir = "E:\\workspace\\MF\\data\\"
    fprobe = rootDir +  "MFrecommend.dat"
    ftest = rootDir + "test.dat"
    mfEvaluate = MFPR(fprobe, ftest)
    fpredict = rootDir + "MFpredict.dat"
    ftrain = rootDir + "train.dat"
    mfRSME = MFRSME(fpredict, ftrain)
    
        
    
  
            
            
        