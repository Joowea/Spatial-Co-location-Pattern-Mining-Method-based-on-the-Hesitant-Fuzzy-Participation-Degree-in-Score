import xlrd

data_exa = xlrd.open_workbook(r'C:\Users\Joo\Desktop\x_y_shiyan30.xlsx')
data_fea = xlrd.open_workbook(r'C:\Users\Joo\Desktop\name_shiyan.xlsx')

Data_sheet = data_exa.sheets()[0];
Data_sheet = data_fea.sheets()[0];

#rows = Data_sheet.row_values(0) #获取第一行内容
#cols = Data_sheet.col_values(3) #获取第四列内容
#cell_A1 = Data_sheet.cell(0,0).value # 第一行第一列坐标A1的单元格数据
#cell_C1 = Data_sheet.cell(0,2).value # 第一行第三列坐标C1的单元格数据

