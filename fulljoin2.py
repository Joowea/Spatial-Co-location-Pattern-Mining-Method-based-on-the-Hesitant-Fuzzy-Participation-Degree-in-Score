import get_dataplant2 as gd2
import generate_colocation_pattern as gcp
import generate_colocation_tableinstance as gct
import generate_colocation_prevalence_pattern as gcpp
import numpy as np
import pandas as pd
import time
import haversine as hrs
import logging

global N
N = 1564
global K
K = 19

logging.getLogger().setLevel(logging.INFO)

# 调用数据
E = gd2.data_exa_2
EM = gd2.data_mem_2
ET = gd2.data_fea_2


# 输入
min_prev = input("输入最小支持度阈值min_prev:\n")
d = input("输入最小距离d:\n")


# 邻居矩阵 欧氏距离判断：距离<d 矩阵元素为1
distance_dd = np.zeros((N, N))
for i in range(0, N):
    for j in range(i+1, N):
        if E.iloc[i, 1] != E.iloc[j, 1]:
            # di = cmath.sqrt((E.iloc[i, 2] - E.iloc[j, 2])**2 + (E.iloc[i, 3] - E.iloc[j, 3])**2)
            di = hrs.haversine(E.iloc[i, 2], E.iloc[i, 3], E.iloc[j, 2], E.iloc[j, 3])
            aa = di.real - float(d)
            if aa < 0:
                distance_dd[i, j] = 1
                distance_dd[j, i] = 1


instanceInfo = np.zeros((1, N))
for i in range(0, N):
    instanceInfo[0, i] = E.iloc[i, 0]
distance = {'instanceInfo': instanceInfo, 'distanced': distance_dd}


# 存储x坐标 *----------------------------------------暂时无用----------------------------------------
ss1 = np.zeros((N, 1))
for i in range(0, N):
    ss1[1] = E.iloc[i, 2]     # point_x [336x1]


# 储存隶属度
membership = pd.DataFrame(columns=['mem'])
for i in range(0, N):
    membership.loc[i, 'mem'] = EM.iloc[i, 2]


# 产生1-阶co-location模式及表实例
k = 0

pi_1 = np.zeros((K, 1))
for i in range(0, K):
    pi_1[i, 0] = 1
pr_1 = pi_1


C1_pattern = P1_pattern = ET
T1_co_location = pd.DataFrame(columns=['label', 'instance', 'pi', 'pr', 'pattern_instance_count'])
T2_co_location = pd.DataFrame(columns=['label', 'instance', 'pi', 'pr', 'pattern_instance_count'])
T3_co_location = pd.DataFrame(columns=['label', 'instance', 'pi', 'pr', 'pattern_instance_count'])
T4_co_location = pd.DataFrame(columns=['label', 'instance', 'pi', 'pr', 'pattern_instance_count'])

for i in range(0, K):
    ins = list()

    for w in range(0, N):
        T1_co_location.loc[i, 'label'] = C1_pattern.iloc[i, 0]

        if C1_pattern.iloc[i, 0] == E.iloc[w, 1]:
            T1_e = list()
            T1_e.append(E.iloc[w, 0])
            ins.append(T1_e)
    T1_co_location['instance'][i] = ins
    T1_co_location.loc[i, 'pi'] = 1
    T1_co_location.loc[i, 'pr'] = 1


# 记录特征对象实例数 实例总数  用于计算pr pi
f_i_pr = T1_co_location

for i in range(0, K):     # 实例总数    
        count_ins = len(T1_co_location.loc[i, 'instance'])
        T1_co_location.loc[i, 'pattern_instance_count'] = count_ins


# 整合1-阶候选模式 1-阶频繁模式
C1 = {'pattern': ET, 'pattern_pr': pi_1, 'pattern_pi': pi_1,
      'pattern_instance_count': T1_co_location['pattern_instance_count']}
P1 = {'pattern': ET, 'pi': pi_1, 'pattern_pr': pi_1, 'pattern_pi': pi_1,
      'pattern_instance_count': T1_co_location['pattern_instance_count']}


# 显示1-阶co-location模式及其实例
print('1阶co-location模式的频繁模式是：\n%s' % P1['pattern'])

for i in range(0, K):
    a = T1_co_location.loc[i, 'label']
    b = T1_co_location.loc[i, 'instance']
    print('1阶co-location模式{%s}的实例序号为：%s' % (a, b))


# 整合k表 *----------------------------------------临时方法----------------------------------------

C2 = {}; C3 = {}; C4 = {}
C = [C1, C2, C3, C4]

P2 = {}; P3 = {}; P4 = {}
P = [P1, P2, P3, P4]


T_co_location = [T1_co_location, T2_co_location, T3_co_location, T4_co_location]


# *---------------------------------------------二 三阶临时调试---------------------------------------------

# while循环
print('####----开始while循环----####')
while not P[k]['pattern'].empty and k < 2:
    print('----------------------------------------------------------------------------------------------')
    print('%d阶计算结果：' % (k + 2))

    temp_gcp = gcp.generate_co_location_pattern(P, k)
    if temp_gcp.empty:
        break

    C[k + 1]['pattern'] = temp_gcp['pattern']

    print('%d阶co-location的首选模式是：\n%s' % (k + 2, C[k + 1]['pattern']))

    # 生成表实例
    temp_gct = gct.generate_co_location_table_instance(min_prev, C, T_co_location, k, distance, f_i_pr, membership)

    T_co_location[k + 1] = temp_gct[0]

    C[k + 1]['pattern_pr'] = temp_gct[1][k + 1]['pattern_pr']
    C[k + 1]['pattern_pi'] = temp_gct[1][k + 1]['pattern_pi']
    C[k + 1]['pattern_instance_count'] = temp_gct[1][k + 1]['pattern_instance_count']

    # 候选模式及其pr、pi输出
    count_co_t = np.shape(C[k + 1]['pattern'])[0]

    # 循环输出
    for i in range(0, count_co_t):
        pr_all_in_one = []

        if not T_co_location[k + 1].loc[i, 'instance']:  # 判断 空集跳过
            continue

        print('%d阶co-location模式%s的实例序号是：%s'
              % (k + 1 + 1, (C[k + 1])['pattern'].iloc[i], T_co_location[k + 1].loc[i, 'instance']))

        for t_2 in range(0, k + 2):  # 循环获取pr
            print_pr = C[k + 1]['pattern_pr'].iloc[i][t_2][0]
            pr_all_in_one.append(print_pr)

        print('%d阶co-location模式%s的参与率分别是：%s'
              % (k + 1 + 1, (C[k + 1])['pattern'].iloc[i], pr_all_in_one))
        print('%d阶co-location模式%s的参与度为：%s'
              % (k + 1 + 1, (C[k + 1])['pattern'].iloc[i], C[k + 1]['pattern_pi'][i]))
        print('----------------------------------------------------------------------------------------------')

    temp_gc_pp = gcpp.generate_co_location_prevalence_pattern(min_prev, C[k + 1], T_co_location[k + 1], k + 1)

    #  if P empty break

    P[k + 1]['pattern'] = temp_gc_pp.loc[:, 'pattern']
    P[k + 1]['pattern_pi'] = temp_gc_pp.loc[:, 'pattern_pi']
    P[k + 1]['pattern_instance_count'] = temp_gc_pp.loc[:, 'pattern_instance_count']

    print('%d阶co-location的频繁模式为：\n%s' % (k + 1 + 1, P[k + 1]['pattern']))

    k = k + 1

print(time.perf_counter())










