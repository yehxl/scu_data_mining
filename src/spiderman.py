from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
import csv


class SpiderMan:

    def __init__(self, choice_num, interval=100):
        # print(choice_num)
        # 豆瓣电影排行榜页面列出的所有类型
        self.type_list = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画',
                          '悬疑', '惊悚', '恐怖', '纪录片', '短片', '情色',
                          '音乐', '歌舞', '家庭', '儿童', '传记', '历史',
                          '历史', '战争', '犯罪', '西部', '奇幻', '冒险',
                          '灾难', '武侠', '古装', '运动', '黑色电影']
        # 选择爬取的电影类型
        self.choice_list = []

        for i in range(len(choice_num)):
            _type = self.type_list[choice_num[i]]
            if choice_num[i] >= len(self.type_list):
                choice_num.pop(choice_num[i])
                continue
            self.choice_list.append(_type)

        if interval > 100 or interval < 10:
            if interval > 100:
                self.interval = 100
            else:
                self.interval = 10

        self.url = 'https://movie.douban.com/chart'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/107.0.0.0 Safari/537.36 '
        }

    def get_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(e)
            return None

    def grab_urls(self):
        url_list = []
        validHtml = self.get_html(self.url)
        if validHtml is None:
            return url_list

        soup = BeautifulSoup(validHtml, 'html.parser')
        for link in soup.find_all('a', href=re.compile("/typerank?")):
            raw_href = link.get('href')
            left_pos = raw_href.find('type_name=') + len('type_name=')
            right_pos = raw_href.find('&')
            if raw_href[left_pos: right_pos] in self.choice_list:
                url_list.append(raw_href)

        return url_list

    def get_movie_detail(self, url, center=True):
        info_list = []
        validHtml = self.get_html(url)
        if validHtml is None:
            return info_list

        soup = BeautifulSoup(validHtml, 'html.parser')

        # 爬电影名
        title = soup.find_all('span', property="v:itemreviewed")[0]
        p = re.compile(r'<span property="v:itemreviewed">(.*)</span>', re.S)
        if len(title) == 0:
            info_list.append({'title': 'unknown'})
        else:
            title = re.findall(p, str(title))[0]
            info_list.append({'title': title})
        # 爬导演，没有导演则标记unknown
        directors = soup.find_all('a', rel="v:directedBy")[0]
        if len(directors) == 0:
            info_list.append({'director0': 'unknown'})
        else:
            idx = 0
            # 可能存在多个导演的情况，以director1，director2做'key'
            for director in directors:
                director = str(director)
                _l = director.find('>') + 1
                _r = director.find('</a>')
                director = director[_l: _r]

                info_list.append({'director' + str(idx): director})
                idx = idx + 1

        # 爬主演，选择前三个
        try:
            info = soup.find_all('a', rel="v:starring")
            if len(info) == 0:
                info_list.append({'attr1': 'unknown'})
            elif len(info) < 3:
                for i in range(len(info)):
                    s = str(info[i])
                    d = re.search('>(.*)<', s)
                    d = d.group()[1: d.group().find('<')]
                    info_list.append({'attr' + str(i): d})
            else:
                for i in range(3):
                    s = str(info[i])
                    d = re.search('>(.*)<', s)
                    d = d.group()[1: d.group().find('<')]
                    info_list.append({'attr' + str(i): d})
        except Exception as e:
            print('actor' + str(e))
            # info_list.append({'actor0': 'unknown'})

        # 爬类型
        # 正则表达式pattern
        p = re.compile(r'<span property="v:genre">(.*)</span>', re.S)
        try:
            # info = soup.select('#info')[0]
            genres = soup.find_all('span', property="v:genre")
            if len(genres) == 0:
                info_list.append({'genre0': 'unknown'})
            else:
                for i in range(len(genres)):
                    genre = re.findall(p, str(genres[i]))[0]
                    info_list.append({'genre' + str(i): genre})
        except Exception as e:
            print('genre' + str(e))
            # info_list.append({'genre0': 'unknown'})

        # 爬制片国家/地区
        try:
            info = soup.select('#info')[0]
            regions = re.findall(r'(?<=制片国家/地区: ).+?(?=\n)', info.text)[0]
            idx = 0
            for region in regions.split('/'):
                info_list.append({'region' + str(idx): region.strip(' ')})
                idx = idx + 1
        except Exception as e:
            print('region' + str(e))
            # info_list.append({'region0': 'unknown'})

            # 爬语言
            try:
                info = soup.select('#info')[0]
                languages = re.findall(r'(?<=语言: ).+?(?=\n)', info.text)[0]
                idx = 0
                for language in languages.split('/'):
                    info_list.append({'lang' + str(idx): language.strip(' ')})
                    idx = idx + 1
            except Exception as e:
                print(e)
                # info_list.append({'language0': 'unknown'})

        # 爬上映时间，目前暂定为确定最早的年份
        try:
            # info = soup.select('#info')[0]
            release_dates = soup.find_all('span', property="v:initialReleaseDate")
            if len(release_dates) == 0:
                info_list.append({'ReleaseDate': 'unknown'})
            else:
                y = 3000
                for i in range(len(release_dates)):
                    release_date = str(release_dates[i])
                    temp_year = re.search('\d{4}', release_date)
                    if temp_year:
                        temp_year = temp_year.group()
                        if temp_year.isdigit() and int(temp_year) < y:
                            y = int(temp_year)

                if y == 3000:
                    info_list.append({'ReleaseDate': 'unknown'})
                else:
                    info_list.append({'ReleaseDate': y})
        except Exception as e:
            print('release date' + str(e))
            # info_list.append({'ReleaseDate': 'unknown'})

        # 爬推荐的十个电影
        # center表示为是否是因为某个电影而被推荐的电影
        # 如果不是则只爬内容，不爬下面推荐的十个电影
        # 如果不是则要爬下面推荐的十个电影
        if center:
            idx = 0
            try:
                items = soup.find_all('dd')
                for item in items:
                    item = str(item)
                    link = re.search('href=\"(.*?)\"', item)
                    if link:
                        link = link.group()
                        link = link[6: len(link) - 1]
                    else:
                        link = 'unknown'
                    title = re.search('>(.*?)<', item)
                    if title:
                        title = title.group()
                        title = title[1: len(title) - 1]
                    else:
                        title = 'unknown'
                    info_list.append({'rd' + str(idx): [title, link]})
                    idx = idx + 1
            except Exception as e:
                print('Recommend' + str(e))
        else:
            pass

        return info_list

    def grab_movies(self, url):
        fixed_url = "https://movie.douban.com"
        _url = fixed_url + url
        grab_num = 500
        _top = []

        browser = webdriver.Chrome()
        browser.get(_url)
        for i in range(int(grab_num / 20)):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)

        validHtml = browser.page_source
        soup = BeautifulSoup(validHtml, 'html.parser')
        if validHtml is None:
            print("error in getting html")
            exit()

        items = soup.find_all('span', class_="movie-name-text")
        for i in range(grab_num):
            item = str(items[i])
            link = re.search('href=\"(.*?)\"', item)
            if link:
                link = link.group()
                link = link[6: len(link) - 1]
            else:
                link = 'unknown'
            # title = re.search('>(.*?)<', item)
            # if title:
            #     title = title.group()
            #     title = title[1: len(title) - 1]
            # else:
            #     title = 'unknown'

            _top.append(link)

        return _top

    def store(self):
        # urls中链接如下，是类型的页面
        # https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=
        urls = self.grab_urls()
        for url in urls:
            # 得到某种类型top100的链接
            _top = self.grab_movies(url)
            _type = re.search('type=(.*?)&', url)
            if _type:
                _type = _type.group()
                _type = _type[5: len(_type) - 1]
            else:
                _type = 'default'
            filename = './' + _type + '.csv'
            f = open(file=filename, mode="a", newline="", encoding="utf-8-sig")
            writer = csv.writer(f)
            writer.writerow(('link', 'title', 'director0', 'director1', 'director2', 'attr0', 'attr1', 'attr2',
                             'genre0', 'genre1', 'genre2', 'genre3', 'region0', 'region1', 'region2',
                             'lang0', 'lang1', 'lang2', 'ReleaseDate',
                             'rd0', 'rd1', 'rd2', 'rd3', 'rd4', 'rd5', 'rd6', 'rd7', 'rd8', 'rd9'))
            cols_name = ['link', 'title', 'director0', 'director1', 'director2', 'attr0', 'attr1', 'attr2',
                         'genre0', 'genre1', 'genre2', 'genre3', 'region0', 'region1', 'region2',
                         'lang0', 'lang1', 'lang2', 'ReleaseDate',
                         'rd0', 'rd1', 'rd2', 'rd3', 'rd4', 'rd5', 'rd6', 'rd7', 'rd8', 'rd9']
            for t in _top:
                # 目前都作为中心电影，也就是要找推荐的10个电影
                infos = self.get_movie_detail(t, center=True)
                row = [t]
                # i = 1
                for col in cols_name:
                    if col == 'link':
                        continue
                    for info in infos:
                        isFind = False
                        if col in info:
                            row.append(info[col])
                            isFind = True
                            break
                    if not isFind:
                        row.append('unknown')
                    # i = i + 1
                writer.writerow(row)
                # time.sleep(2)

            time.sleep(2)
            f.close()
