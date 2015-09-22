#coding:utf8

'''
@auther : chenyun
@time: 2015/09/08
@refer http://ufldl.stanford.edu/wiki/index.php/%E5%8F%8D%E5%90%91%E4%BC%A0%E5%AF%BC%E7%AE%97%E6%B3%95
             http://ufldl.stanford.edu/wiki/index.php/%E8%87%AA%E7%BC%96%E7%A0%81%E7%AE%97%E6%B3%95%E4%B8%8E%E7%A8%80%E7%96%8F%E6%80%A7

'''
import numpy as np
from numpy import array,random
from scipy import optimize as opt
from numpy import dot,transpose
import scipy
from scipy.misc import imshow,imread

def sigmoid(x):
    return 1/(1+np.exp(-x))
def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))
def  KL_div(rho,rho_hat):
    KL=rho*np.log(rho/rho_hat)+(1-rho)*np.log((1-rho)/(1-rho_hat))
    #print rho*np.log(rho/rho_hat),(1-rho)*np.log((1-rho)/(1-rho_hat))
    #print 'kl_sum',sum(KL.reshape([len(rho),1]))[0]
    return sum(KL)
    
def sparse_autodecoder_cost(theta,data,input_len,hidden_len,beta,lambda_,sparsity_para):
    x=np.array(data ).reshape([input_len,-1])
    data=x
    #隐藏层的计算
    W0=np.array(theta[0:input_len*hidden_len]).reshape(hidden_len,input_len)
    b0=np.array(theta[input_len*hidden_len:hidden_len+input_len*hidden_len] ).reshape([hidden_len,1])
    z1= W0.dot(x)+b0 
    hidden_units=sigmoid(z1)
    # 输出层的计算
    tmp=input_len*hidden_len+hidden_len
    W1=np.array(theta[tmp:tmp+input_len*hidden_len]).reshape([input_len,hidden_len])
    b1=np.array(theta[tmp+input_len*hidden_len:]).reshape([input_len,1])
    z2= W1.dot(hidden_units)+b1
    output_units=(z2)
    
    m = data.shape[1]
    ## attentions np.sum
    rho_hat = np.sum(hidden_units,axis=1)
    
    print hidden_units.reshape([10,-1])
    # cost
    cost1=  np.sum(output_units- x)**2/(2*data.shape[1]) 
    cost2= np.sum(W1**2)+np.sum(W0**2)*0.5*lambda_ ### attention for +
    cost3= beta*KL_div(sparsity_para,rho_hat)
    
    J = cost1+cost2+cost3
    
    # 反向传播
    
    delta2 = -(data - output_units)* sigmoid_prime(z2)
    delta1 = ((W1.T.dot(delta2))+ beta*( (1-sparsity_para)/(1-rho_hat).reshape([100,1]) -sparsity_para/rho_hat.reshape([100,1])  ))*sigmoid_prime(z1)## attention for reshape
    
    gradW1 = delta2.dot(hidden_units.T)
    #print delta1.shape,delta2.shape,data.shape,hidden_units.shape,output_units.shape
    gradW0 = delta1.dot(data.T)
    
    gradb0 = delta1
    gradb1 = delta2
    
    #attention for shape
    grad = np.concatenate((gradW0.reshape(hidden_len*input_len),gradb0.reshape(hidden_len),gradW1.reshape(hidden_len*input_len),gradb1.reshape(input_len)))

    #imshow(data.reshape([100,100])*200)
    #imshow(output_units.reshape([100,100])*200)
    #imshow(hidden_units.reshape([10,10])*200)
    return J,grad
    
    
    
    
    
    
    
    
data=imread('b.png',True)
data=data[150:250,150:250].reshape([-1,1])# shape
data=data/200# attention
print data
hidden_len = 100
J = lambda theta: sparse_autodecoder_cost(theta,data,data.shape[0],hidden_len,1,0.1,0.05)

theta_len = data.shape[0]*hidden_len*2 + data.shape[0] + hidden_len
result= opt.minimize(J,random.randn(theta_len)*0.01,method='L-BFGS-B',jac=True,options={'disp':True,'maxiter':10})  
print result.x
#imshow(result.x.reshape([10,10])*200)
