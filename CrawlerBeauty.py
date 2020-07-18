# Load Package
import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup as Soup


# Setting Crawler
my_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
           'Chrome/83.0.4103.116 Mobile Safari/537.36'
headers = {'user-agent': my_agent}
cookies = {'over18': '1'}


def crawler_web(url, stop_time=5):
    time.sleep(stop_time)
    return requests.get(url=url, headers=headers, cookies=cookies)


# crawler list for focus page
def crawler_list(beauty_url):
    web_url = 'https://www.ptt.cc' + beauty_url
    web_res = crawler_web(web_url)
    web_suop = Soup(web_res.text, 'html.parser')

    # 是否有上頁, 如果為[], 代表到首頁
    pre_page = [item['href'] for item in web_suop.find_all(class_='btn wide') if '上頁' in item.text]
    if re.findall('index\.html', web_url + beauty_url) != []:
        the_page = int(re.findall(r'(?<=index)\d+(?=\.html)', pre_page[0])[0]) + 1
    else:
        the_page = int(re.findall(r'(?<=index)\d+(?=\.html)', web_url + beauty_url)[0])
    print(f'Start Crawler Page {the_page}')
    focus_soups = web_suop.find_all(class_='r-ent')
    focus_soups = [item for item in focus_soups if not '[公告]' in item.find(class_='title').text]
    focus_soups = [item for item in focus_soups if not '刪除' in item.find(class_='title').text]
    focus_soups = [item for item in focus_soups if not '退文' in item.find(class_='title').text]
    # 頁面資訊
    page_data = []
    for focus_soup in focus_soups:
        paper_data = dict(
            title=focus_soup.find(class_='title').text.strip('\n'),
            author=focus_soup.find(class_='author').text,
            date=focus_soup.find(class_='date').text.replace(' ', ''),
            link=focus_soup.find(class_='title').find('a')['href']
        )
        page_data.append(paper_data)
    return {'pre_page': pre_page, 'page_data': page_data}


# crawler paper data
def crawler_paper(paper_url):
    web_url = 'https://www.ptt.cc' + paper_url
    paper_web = crawler_web(web_url)
    focus_soup = re.findall(re.compile('(?<=href\=")https:\/\/i\.+.+?(?=")'), paper_web.text)
    return focus_soup


# file write
def file_write(datas):
    import os
    # 給定位置
    data_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(data_path, 'static/beauty_data.json')
    # 資料不存在處理
    if not os.path.exists('static/beauty_data.json'):
        with open(data_path, 'w', encoding='UTF-8') as f:
            json.dump([], f, indent=4)
    # 讀取資料
    with open(data_path, 'r', encoding='UTF-8') as f:
        org_data = json.loads(f.read())
    # 放入資料
    for data in datas:
        org_data.append(data)
    # 寫入資料
    with open(data_path, 'w', encoding='UTF-8') as f:
        json.dump(org_data, f, indent=4, ensure_ascii=False)


def main():
    beauty_url = '/bbs/Beauty/index.html'

    # 爬取 首頁
    # res = crawler_list(beauty_url)
    # page_datas = res['page_data']
    # for paper_data in page_datas:
    #     paper_data['paper_data'] = crawler_paper(paper_data['link'])
    # file_write(page_datas)
    # print(page_datas)
    # print(type(page_datas))
    # print("Crawler Page End!")

    # 爬取3頁
    for _ in range(3):
        res = crawler_list(beauty_url)
        page_datas = res['page_data']
        for paper_data in page_datas:
            paper_data['paper_data'] = crawler_paper(paper_data['link'])
        file_write(page_datas)
        if res['pre_page'] != []:
            beauty_url = res['pre_page'][0]
        print("Crawler Page End!")
    print("Crawler All End")


if __name__ == '__main__':
    main()