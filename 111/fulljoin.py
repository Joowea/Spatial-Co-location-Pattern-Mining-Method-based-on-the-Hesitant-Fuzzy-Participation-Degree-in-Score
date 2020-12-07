import xlrd
import numpy as np
import cmath

global N
N = 30

global K
K = 7

data_exa = xlrd.open_workbook(r'C:\Users\Joo\Desktop\x_y_shiyan30.xlsx')
data_fea = xlrd.open_workbook(r'C:\Users\Joo\Desktop\name_shiyan.xlsx')

E = data_exa.sheets()[0];
ET = data_fea.sheets()[0];

min_prev = input("输入最小支持度阈值min_prev:\n")
d = input("输入最小距离d:\n")

distancedd = np.zeros((N,N)) #邻居矩阵

for i in range(0,N):
    for j in range(i+1,N):
        if (E.cell(i,1).value != E.cell(j,1).value):
            di = cmath.sqrt((E.cell(i,2).value - E.cell(j,2).value)**2 + (E.cell(i,3).value - E.cell(j,3).value)**2)
            if di.real < float(d):
                distancedd[i,j]=1
                distancedd[j,i]=1




