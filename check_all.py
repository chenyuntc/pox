import numpy as np
from gradient import *
#def check_all():
#if __name__ == '__main__':
matrixs=[]
matrixs.append(np.random.random([4,2]))
matrixs.append(np.random.random([1,4]))
bb=[1,1]
datas=[([1,2.0],1),([100,100],0)]
a_s=forward_spread(datas[0][0],matrixs)
delta=cal_last_layer(datas[0][1],a_s[-1])
delta_s=cal_hidden_layer(a,delta,matrixs)
update_wb(matrixs,bb,0.1,delta_s,a_s)