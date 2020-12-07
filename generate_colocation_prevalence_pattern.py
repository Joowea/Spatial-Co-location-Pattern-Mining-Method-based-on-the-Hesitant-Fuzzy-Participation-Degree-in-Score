import numpy as np
import pandas as pd


def generate_co_location_prevalence_pattern(min_prev, cc_k1, tt_k1, k1):
    cc_p = pd.DataFrame(columns=['pattern', 'pattern_pr', 'pattern_pi', 'pattern_instance_count'])
    count = np.shape(cc_k1['pattern'])
    count_co_c = count[0]  # 特征对数
    a_cc = 0

    for i in range(0, count_co_c):

        if cc_k1['pattern_pi'].iloc[i] - float(min_prev) >= 0:

            cc_p.loc[a_cc, 'pattern'] = cc_k1['pattern'].iloc[i]
            cc_p.loc[a_cc, 'pattern_pr'] = cc_k1['pattern_pr'].iloc[i]
            cc_p.loc[a_cc, 'pattern_pi'] = cc_k1['pattern_pi'].iloc[i]
            cc_p.loc[a_cc, 'pattern_instance_count'] = cc_k1['pattern_instance_count'][i]
            a_cc = a_cc+1

    return cc_p


