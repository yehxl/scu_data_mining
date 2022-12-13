from bs4 import BeautifulSoup
import requests
import re
import random

user_agent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]

def grabOne(url):
    headers = {
        'User-Agent': random.choice(user_agent)
    }
    html = ''
    try:
        response = requests.get(url=url, headers=headers)
        response.close()
        print(response.status_code)
        if response.status_code == 200:
            html = response.text
    except Exception as e:
        print(e)
        print('未获取到html文本')
        return

    infodict = {}
    soup = BeautifulSoup(html, 'html.parser')

    try:
        directors = soup.find_all('a', rel="v:directedBy")[0]
        if len(directors) == 0:
            infodict['director0'] = 'unknown'
        else:
            idx = 0
            # 可能存在多个导演的情况，以director1，director2做'key'
            for director in directors:
                director = str(director)
                _l = director.find('>') + 1
                _r = director.find('</a>')
                director = director[_l: _r]

                infodict['director' + str(idx)] = director
                idx = idx + 1
    except Exception as e:
        print(e)
        print('获取导演信息有问题...已将导演置为unknown')
        infodict['director0'] = 'unknown'

    try:
        info = soup.find_all('a', rel="v:starring")
        if len(info) == 0:
            infodict['attr1'] = 'unknown'
        elif len(info) < 3:
            for i in range(len(info)):
                s = str(info[i])
                d = re.search('>(.*)<', s)
                d = d.group()[1: d.group().find('<')]
                infodict['attr' + str(i)] = d
        else:
            for i in range(3):
                s = str(info[i])
                d = re.search('>(.*)<', s)
                d = d.group()[1: d.group().find('<')]
                infodict['attr' + str(i)] = d
    except Exception as e:
        print('actor' + str(e))
        infodict['attr1'] = 'unknown'

    p = re.compile(r'<span property="v:genre">(.*)</span>', re.S)
    try:
        genres = soup.find_all('span', property="v:genre")
        if len(genres) == 0:
            infodict['genre0'] = 'unknown'
        else:
            for i in range(len(genres)):
                genre = re.findall(p, str(genres[i]))[0]
                infodict['genre' + str(i)] = genre
    except Exception as e:
        print('genre' + str(e))
        infodict['genre0'] = 'unknown'

    try:
        info = soup.select('#info')[0]
        regions = re.findall(r'(?<=制片国家/地区: ).+?(?=\n)', info.text)[0]
        idx = 0
        for region in regions.split('/'):
            infodict['region' + str(idx)] = region.strip(' ')
            idx = idx + 1
    except Exception as e:
        print('region' + str(e))

    try:
        info=soup.select('#info')[0]
        # languages=re.findall(r'<span class="pl">语言:</span>(.*)<',info.text)[0]
        languages = re.findall(r'(?<=语言:).+?(?=\n)', info.text)[0]
        idx = 0
        for language in languages.split('/'):
            infodict['lang' + str(idx)] = language.strip(' ')
            idx = idx + 1
    except Exception as e:
        print(e)

    try:
        release_dates = soup.find_all('span', property="v:initialReleaseDate")
        if len(release_dates) == 0:
            infodict['ReleaseDate'] = 'unknown'
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
                infodict['ReleaseDate'] = 'unknown'
            else:
                infodict['ReleaseDate'] = y
    except Exception as e:
        print('release date' + str(e))

    return infodict


if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/1292679/?from=subject-page'
    info = grabOne(url=url)
    print(info)
