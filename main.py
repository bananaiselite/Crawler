import crawler
import os
import datetime
import pandas as pd


def list_to_csv(url, page):
    columns = ['中文名稱', '英文名稱', '預告片網址', '評分', '上映時間']
    newmovie_list = crawler.new_movie(page=page, url=url)

    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    timestamp = timestamp[:4] + '-' + timestamp[4:6] + '-' + timestamp[6:9]

    df = pd.DataFrame(newmovie_list, columns=columns)
    filename = 'new movie list' + timestamp + '.csv'
    df.to_csv(filename, index=False)
    print(f'文件{filename}已成功保存至{os.getcwd()}')


if __name__ == '__main__':
    url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
    list_to_csv(url, 2)
