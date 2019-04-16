# -*- coding: UTF-8 -*-
import pymongo
from pyecharts import Bar,Pie,Line,WordCloud,Page

# 数据库
client = pymongo.MongoClient('localhost',27017)
book = client['Book']
film = client['douban1']

# 表
bookurl_list = book['url_list']
bookitem_detail = book['item_detail']

filmurl_list = film['url_list1']
filmitem_detail = film['item_detail1']

# 获取评分
def getAllScore():
    # 获取数据库中的全部评分
    filmscore_list = []
    for i in filmitem_detail.find():
        filmscore_list.append(i['score'])
    # 将全部评分放入set中去重，得到一个评分列表
    filmscore_index = list(set(filmscore_list))
    filmscore_index.sort(reverse=True)  # 评分列表降序排列

    # 统计每个评分的数量，得到一个评分数量列表
    filmscore_times = []
    for index in filmscore_index:
        filmscore_times.append(filmscore_list.count(index))

    print(filmscore_index)
    print(filmscore_times)

    bookscore_list = []
    for i in bookitem_detail.find():
        bookscore_list.append(i['score'])
    # 将全部评分放入set中去重，得到一个评分列表
    bookscore_index = list(set(bookscore_list))
    bookscore_index.sort(reverse=True) # 评分列表降序排列

    # 统计每个评分的数量，得到一个评分数量列表
    bookscore_times = []
    for index in bookscore_index:
        bookscore_times.append(bookscore_list.count(index))

    print(bookscore_index)
    print(bookscore_times)


    bar = Bar("豆瓣电影图书TOP250", "评分的可视化分析",title_pos="12%")# 柱形统计图
    bar.add("各评分的电影数量", filmscore_index, filmscore_times, is_stack=True,legend_pos="60%")
    bar.add("各评分的图书数量", bookscore_index, bookscore_times, is_stack=True,legend_pos="60%",
            xaxis_name="评分", xaxis_name_pos="end", xaxis_name_gap="2",
            yaxis_name="数量", yaxis_name_pos="end", yaxis_name_gap="12")

    return bar

# 获取国家
def getAllCountry():

    country_list = []
    for i in filmitem_detail.find():
        country_list.append(i['country'])

    for i in bookitem_detail.find():
        country_list.append(i['country'])

    a = {'美': '美国','中':'中国大陆','日':'日本','英':'英国',
         '法':'法国','意':'意大利','德':'德国','澳':'澳大利亚'} # 字典
    country_list = [a[i] if i in a else i for i in country_list] # 替换国家名称
    country_index = list(set(country_list))

    country_times = []
    for index in country_index:
        country_times.append(country_list.count(index))

    print(country_index)
    print(country_times)

    pie = Pie("豆瓣电影图书TOP250", "国家的可视化分析",title_pos="12%")# 饼图
    pie.add("各国家的电影图书数量", country_index, country_times,
            is_legend_show=False, is_label_show=True)  # 不显示图例

    return pie

# 获取年份
def getAllYear():
    filmyear_list = []
    for i in filmitem_detail.find():
        filmyear_list.append(i['year'])
    filmyear_index = list(set(filmyear_list))
    filmyear_index.sort()  # 年份升序排列

    filmyear_times = []
    for index in filmyear_index:
        filmyear_times.append(filmyear_list.count(index))

    print(filmyear_index)
    print(filmyear_times)

    bookyear_list = []
    for i in bookitem_detail.find():
        bookyear_list.append(i['year'])
    bookyear_index = list(set(bookyear_list))
    bookyear_index.sort()# 年份升序排列

    bookyear_times = []
    for index in bookyear_index:
        bookyear_times.append(bookyear_list.count(index))

    print(bookyear_index)
    print(bookyear_times)

    line = Line("豆瓣电影图书TOP250", "年份的可视化分析",title_pos="12%")# 折线统计图
    line.add("各年份电影数量", filmyear_index, filmyear_times)
    line.add("各年份图书数量", bookyear_index, bookyear_times,legend_pos="60%",
             xaxis_name="年份", xaxis_name_pos="end", xaxis_name_gap="2",
             yaxis_name="数量", yaxis_name_pos="end", yaxis_name_gap="12")

    return line

# 获取导演及作者
def getallAuthor():
    author_list = []
    for i in filmitem_detail.find():
        author_list.append(i['director'])
    for i in bookitem_detail.find():
        author_list.append(i['author'])
    author_index = list(set(author_list))

    author_times = []
    for index in author_index:
        author_times.append(author_list.count(index))

    print(author_index)
    print(author_times)

    wordcloud = WordCloud("豆瓣电影图书TOP250", "导演及作者的可视化分析",title_pos="12%")# 词云
    wordcloud.add("各导演及作者的作品数量", author_index, author_times)

    return wordcloud

def main(bar,pie,line,wordcloud):
    # 一个网页显示多张图
    page=Page()
    page.add(bar)
    page.add(pie)
    page.add(line)
    page.add(wordcloud)
    page.render("豆瓣电影图书TOP250.html")# 渲染网页，生成本地HTML文件

bar=getAllScore()
pie=getAllCountry()
line=getAllYear()
wordcloud=getallAuthor()

main(bar,pie,line,wordcloud)