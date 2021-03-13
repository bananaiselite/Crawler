from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
import datetime

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
headers = {'cookie': 'over18=1'}

def getHtml(url):
    try:
        headers = {'cookie': 'over18=1'}
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        resp.raise_for_status()

        return resp.text
    except:
        return '獲取Html訊息失敗'



def getmsg(url, pages, data_csv=False, keyword=''):
    '''
    :param url: 字串 --> 網址
    :param  keyword: 字串 --> 關鍵字搜尋,預設返回全部
    :param  data_csv: 布林值-->是否輸出成表格
    :return:
    '''
    content = []
    pages = pages
    for page in range(pages):
        soup = BeautifulSoup(getHtml(url), 'lxml')
        rows = soup.find_all('div', class_='title')

        for row in rows:
            article_url = get_article_href(row, keyword)
            article_soup = BeautifulSoup(getHtml(article_url), 'lxml')
            article_info = article_soup.select('span.article-meta-value')

            if article_info:
                print(f'作者：{article_info[0].string}')
                print(f'標題：{article_info[2].string}')
                print(f'時間：{article_info[3].string}')
                print()

                if data_csv:
                    c = [article_info[0].string, article_info[2].string, article_info[3].string]
                    content.append(c)
        url = nextpage(url)

    if data_csv:
        csvmsg(content)


def nextpage(url):
    soup = BeautifulSoup(getHtml(url), 'lxml')
    link = soup.find_all('a', class_='btn wide')[1]['href']
    link = 'https://www.ptt.cc' + link

    return link


def get_article_href(row, keyword=''):
    wordcheck = row.find('a', text= re.compile(keyword))
    if wordcheck:
        address = wordcheck['href']
        article_url = 'https://www.ptt.cc' + address
        return article_url


def csvmsg(content):
    columns = ['作者', '標題', '發佈時間']
    df = pd.DataFrame(content, columns=columns)

    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    timestamp = timestamp[:4] + '-' + timestamp[4:6] + '-' + timestamp[6:9]

    filename = 'ptt gossip ' + timestamp+'.csv'
    df.to_csv(filename, index=False)
    print(f'文件{filename}已成功保存至{os.getcwd()}')


if __name__ == '__main__':
    getmsg(url, 1, True, '')
