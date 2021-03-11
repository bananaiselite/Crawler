import requests
from bs4 import BeautifulSoup



def new_movie(page, url):
    url = url
    content = []
    page = page
    kv = {'page': 1}
    for i in range(page):

        resp = requests.get(url, params=kv)

        soup = BeautifulSoup(resp.text, 'lxml')

        rows = soup.find_all('div', class_='release_movie_name')

        for row in rows:
            # 中文名稱
            name = row.find_next('a')
            ch_name = name.string.strip('\n').strip()
            # 英文名稱
            en_name = name.find_next('a')
            en_name = en_name.string.strip('\n').strip()
            # 預告
            trailer = row.find('a')['href']
            # 評分
            rate = row.find_next('span').string
            # 上映時間
            release_time = row.find_next('div', attrs={'class': "release_movie_time"}).string
            release_time = release_time.split('：')[-1].strip()

            c = [ch_name, en_name, trailer, rate, release_time]
            content.append(c)

        kv['page'] += 1
    return content
