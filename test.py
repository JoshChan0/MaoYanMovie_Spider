# -*- coding:utf-8 -*-
#用Beautifulsoup实现爬取猫眼电影T100

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import time


def get_page(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def spider(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all(name='dd')
    for item in items:
        yield {
            '排名:': item.find(name='i', class_='board-index').string,
            '电影名:': item.find(name='p', class_='name').string,
            '主演:': item.find(name='p', class_='star').string.strip()[3:],
            '上映时间:': item.find(name='p', class_='releasetime').string.strip()[5:],
            '评分:': item.find(name='i', class_='integer').string + item.find(name='i', class_='fraction').string
        }


def main(offset):
    url = "https://maoyan.com/board/4?offset="+str(offset)
    html = get_page(url)
    for item in spider(html):
        print(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        time.sleep(3)
