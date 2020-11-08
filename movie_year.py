import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import mpl_toolkits.mplot3d

df_1 = pd.read_csv("top250_f1.csv",sep = "#", encoding = 'utf8')
df = df_1[['num','title','init_year','area','genre','rating_num','comment_num']]

matplotlib.rcParams['font.family'] = 'SimHei' #配置中文字体
matplotlib.rcParams['font.size'] =  15   # 更改默认字体大小


plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
plt.scatter(df['init_year'], df['num'])
plt.xlabel('年份')
plt.ylabel('排名')

plt.gca().invert_yaxis()
plt.show()
print("年份和排名的相关系数为：",df['init_year'].corr(df['num']))
