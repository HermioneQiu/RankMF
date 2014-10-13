from math import exp, log
import copy
def test(list):
    cost = 0
    for l in list:
        tmp_list = copy.deepcopy(list)
        tmp_list.remove(l)
        for t_l in tmp_list:
            cost += g(l)*(1-g(t_l))
    return cost

def g(x):
    return 1/(1+exp(-x)) 
def dg(x):
    return exp(x)/(1+exp(x))**2

if __name__ == "__main__":
    list = [1, 1, 3, 4]
    cost = test(list)
    print cost
    list = [1, 1, 1, 1]
    cost = test(list)
    print cost
    list = [4, 3, 1, 1]
    cost = test(list)
    print cost   
    list = [4, 4, 4, 4]
    cost = test(list)
    print cost    
    