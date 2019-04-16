# -*- coding: UTF-8 -*-
import pymongo
from pyecharts import Bar,Pie,Line,WordCloud,Page

# 数据库
client = pymongo.MongoClient('localhost',27017)
douban = client['Book']
# 表
url_list = douban['url_list']
item_detail = douban['item_detail']

# 获取评分
def getAllScore():
    # 获取数据库中的全部评分
    score_list = []
    for i in item_detail.find():
        score_list.append(i['score'])
    # 将全部评分放入set中去重，得到一个评分列表
    score_index = list(set(score_list))
    score_index.sort(reverse=True) # 评分列表降序排列

    # 统计每个评分的数量，得到一个评分数量列表
    score_times = []
    for index in score_index:
        score_times.append(score_list.count(index))

    print(score_index)
    print(score_times)

    bar = Bar("豆瓣图书TOP250", "评分的可视化分析",title_pos="12%")# 柱形统计图
    bar.add("各评分的图书数量", score_index, score_times,legend_pos="60%",# 图例
            xaxis_name="评分",xaxis_name_pos="end",xaxis_name_gap="2",
            yaxis_name="数量", yaxis_name_pos="end", yaxis_name_gap="12")
    return bar

# 获取国家
def getAllCountry():
    country_list = []
    for i in item_detail.find():
        country_list.append(i['country'])
    country_index = list(set(country_list))

    country_times = []
    for index in country_index:
        country_times.append(country_list.count(index))

    print(country_index)
    print(country_times)

    pie = Pie("豆瓣图书TOP250", "国家的可视化分析",title_pos="12%")# 饼图
    pie.add("各国家的图书数量", country_index, country_times
            ,is_legend_show=False, is_label_show=True)# 不显示图例
    return pie

# 获取年份
def getAllYear():
    year_list = []
    for i in item_detail.find():
        year_list.append(i['year'])
    year_index = list(set(year_list))
    year_index.sort()# 年份升序排列

    year_times = []
    for index in year_index:
        year_times.append(year_list.count(index))

    print(year_index)
    print(year_times)

    line = Line("豆瓣图书TOP250", "年份的可视化分析",title_pos="12%")# 折线统计图
    line.add("各年份图书数量", year_index, year_times,legend_pos="60%",
             xaxis_name="年份", xaxis_name_pos="end", xaxis_name_gap="2",
             yaxis_name="数量", yaxis_name_pos="end", yaxis_name_gap="12")
    return line

# 获取导演
def getallAuthor():
    author_list = []
    for i in item_detail.find():
        author_list.append(i['author'])
    author_index = list(set(author_list))

    author_times = []
    for index in author_index:
        author_times.append(author_list.count(index))

    print(author_index)
    print(author_times)

    wordcloud = WordCloud("豆瓣图书TOP250", "作者的可视化分析",title_pos="12%")# 词云
    wordcloud.add("各作者图书数量", author_index, author_times)

    return wordcloud

def main(bar,pie,line,wordcloud):
    # 一个网页显示多张图
    page=Page()
    page.add(bar)
    page.add(pie)
    page.add(line)
    page.add(wordcloud)
    page.render("豆瓣图书TOP250.html")# 渲染网页，生成本地HTML文件

bar=getAllScore()
pie=getAllCountry()
line=getAllYear()
wordcloud=getallAuthor()

main(bar,pie,line,wordcloud)