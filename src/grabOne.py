from bs4 import BeautifulSoup
import requests
import re


def grabOne(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/107.0.0.0 Safari/537.36 '
    }
    try:
        response = requests.get(url=url, headers=headers)
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
    url = 'https://movie.douban.com/subject/1293181/'
    info = grabOne(url=url)
    print(info)
