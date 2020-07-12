import requests
from bs4 import BeautifulSoup
import json
from urllib import parse
import re

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}
session.headers = headers

api_key = "4d0d0155cb6affe986cada4d79851189e039fe85"


def getShareText(baseURL, titletype: str):
    soup = BeautifulSoup(baseURL.text, 'lxml')
    for img in soup.select('.item-box'):
        link = img.select('.detail-box a')
        if not link:
            continue
        title = link[0]
        author = link[1]
        if not title['href']:
            return '由未知错误导致搜索失败'

        Author = f"Author:{author['href']}" if author['href'] else ''
        msg = [f"ascii2d {titletype}",
        f"{title.string}/{author.string}",
        f"[CQ:image,file=https://ascii2d.net{str(img.img['src'])}]",
        f"{title['href']}",
        f"{Author}"
                
        ]
        break

    return msg


class SearchMaster(object):

    def __init__(self, url):
        self.url = url


    def saucenao(self):
        url = 'https://saucenao.com/search.php'
        params = {
            'output_type': 2,
            'numers': 1,
            'minsim': '80!',
            'db': 999,
            'api_key': api_key,
            'url': self.url,
            }
        try:
            r = session.get(url=url, params=params)
        except Exception:
            return '由未知错误导致saucenao搜索失败\n自动使用 ascii2d 进行搜索', False

        results = r.json()     
        if int(results['header']['results_returned']) > 0:
            #one or more results were returned
            if float(results['results'][0]['header']['similarity']) > float(results['header']['minimum_similarity']):
                #get vars to use
                service_name = ''
                illust_id = 0
                member_id = -1
                title = ''
                member_name = ''
                thumbnail = ''
                ext_url = ''
                index_id = results['results'][0]['header']['index_id']
                page_string = ''
                page_match = re.search('(_p[\d]+)\.', results['results'][0]['header']['thumbnail'])
                if page_match:
                    page_string = page_match.group(1)

                if index_id == 5 or index_id == 6:
                    #5->pixiv 6->pixiv historical
                    service_name = 'pixiv'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['pixiv_id']
                    title = results['results'][0]['data']['title']
                    member_name = results['results'][0]['data']['member_name']
                    thumbnail = results['results'][0]['header']['thumbnail']
                    ext_url = results['results'][0]['data']['ext_urls'][0]
                elif index_id == 8:
                    #8->nico nico seiga
                    service_name = 'seiga'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['seiga_id']
                    thumbnail = results['results'][0]['header']['thumbnail']
                    ext_url = results['results'][0]['data']['ext_urls'][0]
                elif index_id == 10:
                    #10->drawr
                    service_name = 'drawr'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['drawr_id']
                    thumbnail = results['results'][0]['header']['thumbnail']
                    ext_url = results['results'][0]['data']['ext_urls'][0]						
                elif index_id == 11:
                    #11->nijie
                    service_name = 'nijie'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['nijie_id']
                    thumbnail = results['results'][0]['header']['thumbnail']
                    ext_url = results['results'][0]['data']['ext_urls'][0]
                elif index_id == 34:
                    #34->da
                    service_name = 'da'
                    illust_id = results['results'][0]['data']['da_id']
                    thumbnail = results['results'][0]['header']['thumbnail']
                    ext_url = results['results'][0]['data']['ext_urls'][0]
                else:
                    #unknown
                    return '很抱歉，该功能还在摸鱼制作中_(:3」」', False

                if index_id == 5 or index_id == 6:
                    msg = [f"SauceNAO [{results['results'][0]['header']['similarity']}%] {service_name}",
                    f"{title}/{member_name}",
                    f"[CQ:image,file={thumbnail}]",
                    f"{ext_url}",
                    f"https://pixiv.net/u/{member_id}"
                    ]
                else:
                    msg = [f"SauceNAO [{results['results'][0]['header']['similarity']}%] {service_name}",
                    f"[CQ:image,file={thumbnail}]",
                    f"{ext_url}",
                    ]
                return '\n'.join(msg), True

            else:
                return f"相似度{results['results'][0]['header']['similarity']}%过低，如果这不是你要找的图，那么可能：确实找不到此图/图为原图的局部图/图清晰度太低/搜索引擎尚未同步新图\n自动使用 ascii2d 进行搜索", False
                
        else:
            return '没有查询到相似图片……\n自动使用 ascii2d 进行搜索', False


    def ascii2d(self):
        imgURL = parse.quote_plus(self.url)
        url = f'https://ascii2d.net/search/url/{imgURL}'
        r = session.get(url=url)

        colorURL = r.url
        bovwURL = colorURL.replace('/color/', '/bovw/')
        b = session.get(url=bovwURL)

        color = '\n'.join(getShareText(r, '色合検索'))
        bovw = '\n'.join(getShareText(b, '特徴検索'))
        return color, bovw