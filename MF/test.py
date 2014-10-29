from math import exp, log
import copy

def test(list):
    cost = 0
    p_list = list[0:4]
    print p_list
    n_list = list[4:]
    print n_list
    for i in range(4):
        l = list[i]
        tmp_cost = g(l)
        for t_l in p_list:
            tmp_cost *= 1- g(t_l - l)
        for t_l in n_list:
            tmp_cost *= g(l - t_l)
        cost += tmp_cost
    return cost

def g(x):
    return 1/(1+exp(-x)) 
def dg(x):
    return exp(x)/(1+exp(x))**2

if __name__ == "__main__":
    list = [4, 0.5, 4, 2, 2, 0.5]
    cost = test(list)
    print cost
    list = [4, 2, 4, 2, 0.5, 0.5]
    cost = test(list)
    print cost  
    x = 1
    print g(x)
    print 1 - g(-x) 
    