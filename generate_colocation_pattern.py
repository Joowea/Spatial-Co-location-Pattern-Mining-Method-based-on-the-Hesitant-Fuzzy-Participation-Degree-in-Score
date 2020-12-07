import numpy as np
import pandas as pd
import copy as cp


def generate_co_location_pattern(p, k):  # 产生候选模式的方法

    # cc：产生候选模式的方法中候选模式表 用于生成、保存c(k+1)
    # cc_sub：形式同cc 用于对比 通过对比结果修改cc表 生成c(k+1)
    cc = pd.DataFrame(columns=['pattern'])
    cc_sub = pd.DataFrame(columns=['pattern'])

    # count
    count = np.shape(p[k]['pattern'])
    count_co = count[0]

    if count_co == 1:
        return cc

    x = 1

    # 一阶特征种类两两配对
    if k == 0:
        f_pattern = list()
        for i in range(0, count_co):
            for j in range(i+1, count_co):

                f_pattern.append((p[k])['pattern'].iloc[i, 0])
                f_pattern.append(p[k]['pattern'].iloc[j, 0])
                cc.loc[x, 'pattern'] = f_pattern
                f_pattern = []
                x = x + 1

    # 特征连接
    else:
        for i in range(0, count_co-1):
            for j in range(i+1, count_co):
                cc_pattern = []
                find_w = 0

                for w in range(0, k+1):
                    a = p[k]['pattern'].loc[i][w]
                    b = p[k]['pattern'].loc[j][w]
                    if a != b:
                        find_w = w
                        break

                if find_w == k:
                    for wa in range(0, k+1):
                        cc_pattern.append(p[k]['pattern'].loc[i][wa])
                    cc_pattern.append(p[k]['pattern'].loc[j][k])
                    cc.loc[x, 'pattern'] = cc_pattern
                    x = x + 1

    if cc['pattern'].empty:
        return cc

    count = np.shape(cc['pattern'])
    count_co_cc = count[0]

    # 连接后判断是否关联
    if k == 1:
        i = 1
        while i <= count_co_cc:
            find_bg = 0
            sub_pattern = cp.copy(cc['pattern'][i])
            del sub_pattern[0]
            cc_sub.loc[i, 'pattern'] = sub_pattern

            for j in range(0, count_co):

                if cc_sub.loc[i, 'pattern'] == p[k]['pattern'].loc[j]:  # 若关联 bg=1

                    find_bg = 1
                    break

            if find_bg == 0:  # 不关联 清除
                cc.drop([i], inplace=True)
            i = i+1

    cc.reset_index(drop=True, inplace=True)

    return cc










