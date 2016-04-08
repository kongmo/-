# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 10:13:04 2016

@author: aa
"""
import numpy as np
import random


def sign(x):
    if x<=0:
        return -1
    return 1


def LoadData(filename):
    data=np.loadtxt(filename)
    m=data.shape[0]
    X=data[:,:-1]
    X=np.hstack((np.ones((m,1)),X))
    y=data[:,-1]
    return (X,y)
    
def PAC(X,y,rand,factor,iterNum):
    m=X.shape[0]
    n=X.shape[1]
    TotalCount = list()
    for j in range(iterNum):
        idx=range(m)
        if rand:
            idx=random.sample(idx,m)
        count=0
        w=np.zeros(n)
        while True:
            flag = 1
            for k in range(m):
                i=idx[k]
                g=sign(np.dot(X[i],w))
                if g == y[i]:
                    continue
                w=w+factor*y[i]*X[i]
                count =count+1
                flag=0
            if flag:
                break  
        TotalCount.append(count)

    TotalCount=np.array(TotalCount,dtype=int)
    print  TotalCount.mean()
    return TotalCount.mean()

def pocket(X,y,Xtest,ytest,upNum,iterNum,flag):
    m=X.shape[0]
    n=X.shape[1]
    TotalError=np.zeros(iterNum)
    for i in range(iterNum):
        w=np.zeros(n)
        error=testPocket(X,y,w)
        Bestw=w
        for j in range(upNum):
            idx=random.sample(range(m),m)
            for k in idx:
                if sign(np.dot(X[k],w)) !=y[k]:
                    w=w+y[k]*X[k]
                    e=testPocket(X,y,w)
                    if e < error:
                        Bestw=w
                        error=e    
                    break      
        if flag:
            Bestw=w
        TotalError[i]=testPocket(Xtest,ytest,Bestw)
    print TotalError.mean()  
    return TotalError.mean()
  
 
        
def testPocket(Xtest,ytest,w):
    num=Xtest.shape[0]
    count=sum(1 for i in range(num) if sign(np.dot(Xtest[i],w)) != ytest[i])
    return count/float(num)

def main():
    X,y=LoadData('SessionOne.txt')
    Xt,yt=LoadData('SessionTwo.txt')
    Xtest,ytest=LoadData('SessionTwoTest.txt')
    titleNum=int(input('Please Enter the title num(15|16|17|18|19|20)\n'))
    if titleNum == 15:
        PAC(X,y,rand=False,factor=1,iterNum=1)
    if titleNum == 16:
        PAC(X,y,rand=True,factor=1,iterNum=2000)
    if titleNum == 17:
        PAC(X,y,rand=True,factor=0.5,iterNum=2000)
    if titleNum == 18:
        pocket(Xt,yt,Xtest,ytest,50,2000,False)
    if titleNum == 19:
        pocket(Xt,yt,Xtest,ytest,50,2000,True)
    if titleNum == 20:
        pocket(Xt,yt,Xtest,ytest,50,2000,False)
        

if __name__=='__main__':
    main()
