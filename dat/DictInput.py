class DictInput:
    def __init__(self, finput, fpart, ftrain, ftest, personNum, trainRate):
        self.finput = finput
        # confine the number of user below personNum
        self.fpart = fpart
        self.ftrain = ftrain
        self.ftest = ftest
        self.getPart(personNum)
        # for part user
        self.userDict = dict()
        self.getUserDict()
        
        self.getTrain(trainRate)
        
    def getPart(self, personNum):
        Finput = open(self.finput, "r")
        Fpart = open(self.fpart, "w")
        for line in Finput:
            start, end = line.strip().split("\t")
            start = int(start)
            end = int(end)
            if (start < personNum) & (end < personNum):
                Fpart.write(line)
        Finput.close()
        Fpart.close()
        
    def getUserDict(self):  
        userDict = self.userDict 
        Fpart = open(self.fpart,"r")
        for line in Fpart:
            start, end = line.strip().split("\t")
            if start not in userDict.keys():
                userDict[start] = [end]
            else:
                userDict[start].append(end)
        Fpart.close()
        
    def getTrain(self, trainRate):
        userDict = self.userDict
        trainUserDict = dict()
        testUserDict = dict()
        # 1. got trainRate*len(userDict[user]) into trainUserDict[user]
        for user in userDict.keys():
            trainLen = int(round(trainRate * len(userDict[user])))
            items = userDict[user]
            trainItems = items[0:trainLen]
            testItems = items[trainLen:]
            trainUserDict[user] = trainItems
            testUserDict[user] = testItems
        # 2. save remaining infos into testUserDict[user]
        Ftrain = open(self.ftrain, "w")
        Ftest = open(self.ftest,"w")
        for user in trainUserDict.keys():
            if (len(trainUserDict[user])>0):
                line = user+ "\t"+",".join(trainUserDict[user]) + "\n"
            Ftrain.write(line)
        for user in testUserDict.keys():
            if (len(testUserDict[user]) > 0):
                line = user +"\t"+",".join(testUserDict[user])+"\n"
            Ftest.write(line)
        Ftest.close()
        Ftrain.close()
        
if __name__ == "__main__":
    rootDir = "E:\\workspace\\MF\\data\\cross\\"
    finput = rootDir+"raw.dat"
    fpart = rootDir+"part.dat"
    ftrain = rootDir+"train.dat"
    ftest = rootDir +"test.dat"
    personNum= 500
    trainRate = 0.9
    input = DictInput(finput, fpart, ftrain, ftest,personNum, trainRate)
    print "finished"
    
                
                
            
            
                
                
                
        