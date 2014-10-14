# in_file : user_id: item_id, item_id, item_id ...
# out_file1: train -- user_id\t item_id, item_id, item_id...
# out_file2: test -- user_id\t item_id, item_id, item_id...

class CrossInput:
    def __init__(self, ftrain, K):
        self.ftrain = ftrain
        
    def divide(self, K, rootDir):
        Ftrain = open(self.ftrain, 'r')
        #1. read all data for train
        userDict = dict()
        for line in Ftrain:
            userId, itemIds = line.strip().split("\t")
            itemIds = itemIds.split(",")
            userDict[userId] = itemIds
        # 2.divide data and got testList for K test
        testList = [dict() for i in range(K)]
        for userId in userDict.keys():
            testItems = []
            items = userDict[userId]
            # 2.1. if less than K, then all put into trainK.dat, so do nothing to testList
            # 2.2. else more than K, then get 1/K out for testK.dat, and rest as trainK.dat
            if(len(items)>K):
                dividNum = len(items)/K
                for i in range(K-1):
                    tmpItems = items[dividNum*i:dividNum*(i+1)]
                    testItems.append(tmpItems)
                tmpItems = items[dividNum*i+1:]
                testItems.append(tmpItems)
            else:
                testItems = [[] for i in range(K)]
#             print "testItems: ", len(testItems) 
            for i in range(len(testItems)):
                testList[i][userId] = testItems[i]
        # 3. got train and test data, and save
        for k in range(K):
            testDict = testList[k]
            Ftrain = open(rootDir+"train.dat"+str(k), 'w')
            Ftest = open(rootDir +"test.dat"+str(k), 'w')
            trainDict = dict()
            # 3.1 got trainDict
            for userId in userDict.keys():
                if userId in testDict.keys():
                    testItems = testDict[userId]
                    allItems = userDict[userId]
                    trainItems = self.setSub(allItems, testItems)
                else:
                    trainItems = userDict[userId]
                    testItems = []
                # 3.2 save userId\t item_id... into train(test)k
                line = userId + "\t"+",".join(trainItems)+"\n"
                Ftrain.write(line)
                if len(testItems)!=0:
                    line = userId +"\t"+",".join(testItems)+"\n"
                    Ftest.write(line)
            Ftrain.close()
            Ftest.close()
            
    def setSub(self, List1, List2):           
        tmpList = []
        for l in List1:
            if l not in List2:
                tmpList.append(l)
        return tmpList
    
if __name__  == "__main__":
    rootDir = "E:\\workspace\\MF\\data\\cross\\"
    ftrain = rootDir + "train.dat"
    K = 4
    crossInput = CrossInput(ftrain, K)
    crossInput.divide(K, rootDir)
    print "cross finished"
    
    
    