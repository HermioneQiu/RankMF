class Input:
    def __init__(self, finput, fpart, ftrain, ftest, personNum, trainNum):
        
        self.finput = finput
        self.fpart = fpart
        self.ftrain = ftrain
        self.ftest = ftest
        self.getPart(personNum)
        self.getTrain(trainNum)
        
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
    def getTrain(self, trainNum):
        Fpart  = open(self.fpart, "r")
        Ftrain = open(self.ftrain, "w")
        Ftest = open(self.ftest,"w")
        userList = []
        tmpStart = ""
        for line in Fpart:
            start,end = line.strip().split("\t")
            if (start == tmpStart):
               userList.append(start)
               if (len(userList) <= trainNum):
                   Ftrain.write(line)
               else:
                   Ftest.write(line)
            else:
                userList = []
                tmpStart = start
                userList.append(start)
                Ftrain.write(line)
        Fpart.close()
        Ftest.close()
        Ftrain.close()
        
if __name__ == "__main__":
    rootDir = "E:\\workspace\\MF\\data\\"
    finput = rootDir+"raw.dat"
    fpart = rootDir+"part.dat"
    ftrain = rootDir+"train.dat"
    ftest = rootDir +"test.dat"
    personNum= 500
    trainNum = 30
    input = Input(finput, fpart, ftrain, ftest,personNum, trainNum)
    print "finished"
    
                
                
            
            
                
                
                