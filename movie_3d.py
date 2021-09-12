import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import mpl_toolkits.mplot3d

matplotlib.rcParams['font.family'] = 'SimHei'  # 配置中文字体
matplotlib.rcParams['font.size'] = 10  # 更改默认字体大小

df_1 = pd.read_csv("top250_f1.csv", sep="#", encoding='utf8')
df = df_1[['num', 'title', 'init_year', 'area', 'genre', 'rating_num', 'comment_num']]

x = df['num']
y = df['rating_num']
z = df['comment_num']

ax = plt.subplot(projection='3d')
for xx, yy, zz in zip(x, y, z):
    ax.scatter(xx, yy, zz)

ax.set_xlabel('排名')
ax.set_ylabel('评分')
ax.set_zlabel('人数')

print("排名和评分的相关系数为：", df['num'].corr(df['rating_num']))
print("排名和评价人数的相关系数为：", df['num'].corr(df['comment_num']))
print("评分和评价人数的相关系数为：", df['rating_num'].corr(df['comment_num']))
plt.show()
