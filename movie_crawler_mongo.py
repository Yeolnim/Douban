import pymongo
import urllib.request as urlrequest

from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost', 27017)
film250 = client['film250']
item_detail = film250['item_detail']

top250_url = "https://movie.douban.com/top250?start={}&filter="

for i in range(10):
    start = i * 25
    url_visit = top250_url.format(start)
    crawl_content = urlrequest.urlopen(url_visit).read()
    http_content = crawl_content.decode('utf8')
    soup = BeautifulSoup(http_content, 'html.parser')
    all_item_divs = soup.find_all(class_='item')

    for each_item_div in all_item_divs:
        pic_div = each_item_div.find(class_='pic')
        num = pic_div.find('em').get_text()  # 排名
        # href = pic_div.find('a')['href']  # 电影链接
        title = pic_div.find('img')['alt']  # 电影名称
        bd_div = each_item_div.find(class_='bd')
        infos = bd_div.find('p').get_text().strip().split('\n')
        infos_1 = infos[0].split('\xa0\xa0\xa0')
        # director = infos_1[0][4:].rstrip('...').rstrip('/').split('/')[0]  # 导演
        # role = str(infos_1[1:])[6:].split('/')[0]  # 主演
        infos_2 = infos[1].lstrip().split('\xa0/\xa0')
        year = infos_2[0]  # 上映时间
        # area = infos_2[1]  # 国家/地区
        # genre = infos_2[2:]  # 电影类型
        star_div = each_item_div.find(class_='star')
        rating_num = star_div.find(class_='rating_num').get_text()  # 评分
        comment_num = star_div.find_all('span')[3].get_text()[:-3]  # 评价数量
        # quote = each_item_div.find(class_='quote')
        # inq = quote.find(class_='inq').get_text()  # 一句话评价

        print(num)
        print(title)
        print(year)
        print(rating_num)
        print(comment_num)

        item_detail.insert_one({
            'num': num,
            'title': title,
            'year': year,
            'rating_num': rating_num,
            'comment_num': comment_num,
        })
