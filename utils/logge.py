class Logge:
    def __init__(self, flog):
        self.flog = flog 
    
    def logParas(self, paras):
        Flog = open(self.flog, "a")
        paras = [str(p) for p in paras]
        line = ",".join(paras) 
        Flog.write(line +"\n")
        Flog.close()
        
    def logList(self, name, List):
        Flog = open(self.flog, "a")
        List = [str(l) for l in List]
        line = name+"\t"+",".join(List) + "\n"
        Flog.write(line)
        Flog.close()
        
    def logNum(self, name, num):
        Flog = open(self.flog, "a") 
        num = str(num)
        line= name +"\t"+num+"\n"
        Flog.write(line)
        Flog.close()
        
    def clear(self):
        Flog = open(self.flog, "w")
        Flog.close()
        
        
        
        
        