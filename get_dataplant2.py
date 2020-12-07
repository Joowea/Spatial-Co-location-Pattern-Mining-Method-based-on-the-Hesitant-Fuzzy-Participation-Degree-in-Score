import pandas as pd

# excel数据导入
data_xy = pd.DataFrame(pd.read_excel
                     (r'C:\Users\Joo\Desktop\毕设\实验数据\实验数据-澳门03072\aomen_x_y.xlsx'))
data_name = pd.DataFrame(pd.read_excel
                         (r'C:\Users\Joo\Desktop\毕设\实验数据\实验数据-澳门03072\aomen_name.xlsx'))
# data_xy = pd.DataFrame(pd.read_excel
#                        (r'C:\Users\Joo\Desktop\毕设\实验数据\实验数据-测试\实验2.0\x_y_shiyan30 _pandas_2.0.xlsx'))
# data_name = pd.DataFrame(pd.read_excel
#                          (r'C:\Users\Joo\Desktop\毕设\实验数据\实验数据-测试\实验2.0\name_shiyan_pandas_2.0.xlsx'))

data_exa_2 = pd.DataFrame(columns=['实例序号', '实例名', 'point_x', 'point_y'])
data_mem_2 = pd.DataFrame(columns=['实例序号', '实例名', '犹豫模糊隶属度'])
data_fea_2 = pd.DataFrame(columns=['特征名'])


# 循环存储
for i in range(0, 1564):
    data_exa_2.loc[i, '实例序号'] = data_xy.iloc[i, 0]
    data_exa_2.loc[i, 'point_x'] = data_xy.iloc[i, 4]
    data_exa_2.loc[i, 'point_y'] = data_xy.iloc[i, 5]
    data_exa_2.loc[i, '实例名'] = data_name.iloc[i, 0]


for i in range(0, 1564):
    data_mem_2.loc[i, '实例序号'] = data_xy.iloc[i, 0]
    data_mem_2.loc[i, '实例名'] = data_name.iloc[i, 0]
    data_mem_2.loc[i, '犹豫模糊隶属度'] = data_xy.iloc[i, 8]


for i in range(0, 19):
    data_fea_2.loc[i, '特征名'] = data_name.iloc[i, 1]

