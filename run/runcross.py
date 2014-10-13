from cross.CrossValid import *
from evaluate.DictEvaluate import *
from utils.logge import *

if __name__ == "__main__":
    froot = "E:\\workspace\\MF\\data\\cross\\"
    # K fold cross validate
    K = 1
    for i in range(K):
        frate = froot + "train.dat" + str(i)
        fpredict = froot + "predict\\predict.dat" + str(i)
        ftest = froot + "test.dat" + str(i)
        flog = froot + "log\\log"
        flog_cost = froot + "log\\log"+str(i)
        logge = Logge(flog)
        logge_cost = Logge(flog_cost)
        userNum = 500
        itemNum = 500
        F = 50
        max_iretate = 100
        learnRate = 0.01
        regularRate = 0.6
        paras = [userNum, itemNum, F, max_iretate, learnRate, regularRate, "train"+str(i)]
        logge.logParas(paras)
        # --- train ---
        lmf = CrossValid(frate, ftest, fpredict, userNum, itemNum, F, max_iretate, learnRate, regularRate)  
        trainCost = lmf.trainCost
        testCost = lmf.testCost
        for c_i in range(len(trainCost)):
            tmp = [trainCost[c_i], testCost[c_i]]
            logge_cost.logList("train, test", tmp)  
        # --- get predict ---
        print "finished train: ", i, "begin to evaluate"
        ftrain = frate
        trainMFRSME = RSME(fpredict, ftrain)
        trainError = trainMFRSME.rsme()
        logge.logNum("trainMSE: ", trainError)
        testMFRSME = RSME(fpredict, ftest)
        testError = testMFRSME.rsme()
        logge.logNum("testMSE: ", testError)
        