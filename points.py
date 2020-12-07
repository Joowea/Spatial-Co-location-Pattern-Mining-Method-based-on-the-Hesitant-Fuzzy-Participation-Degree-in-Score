import matplotlib.pyplot as plt
import pandas as pd
import Basemap


plt.title("I'm a scatter diagram.")
plt.xlim(xmax=80, xmin=0)
plt.ylim(ymax=80, ymin=0)

N = 30

data_exa = pd.DataFrame(pd.read_excel(r'C:\Users\Joo\Desktop\毕设\实验数据\实验数据-测试\实验2.0\x_y_shiyan30 _pandas_2.0.xlsx'))

E = data_exa

for i in range(0, N):
    plt.plot(E.iloc[i, 1], E.iloc[i, 2], 'ro')

plt.show()

