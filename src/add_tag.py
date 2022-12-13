import sys
import src.grabOne as grabOne
import time
import pandas as pd
from pandas import DataFrame as df
import random


def tag():
    ct = 0
    sys.path.append("..")
    t = pd.DataFrame()
    # 惊悚 剧情
    li = ['惊悚']
    table = []

    for i in li:
        path = "../clean_data/" + i + ".csv"
        table.append(df(pd.read_csv(path)))
    tp = zip(li, table)
    for label, item in tp:
        for i in range(2, 10):
            index = 'rd' + str(i)
            s = pd.Series(item[index])
            # rd(i) url list
            col = 16 + i * 3
            url_list = s.str.extract(", '(.*?)'", expand=True).values.tolist()
            info_list = {'genre0': [], 'genre1': [], 'director0': [], 'ReleaseDate': [], 'region0': []}
            for url in url_list:
                ct += 1
                print('数量: ', ct)
                res = grabOne.grabOne(url=url[0])
                time.sleep(1)
                if 'genre0' in res.keys():
                    info_list['genre0'].append(res['genre0'])
                else:
                    info_list['genre1'].append('unknown')

                if 'genre1' in res.keys():
                    info_list['genre1'].append(res['genre1'])
                else:
                    info_list['genre1'].append('unknown')
                if 'director0' in res.keys():
                    info_list['director0'].append(res['director0'])
                else:
                    info_list['director0'].append('director0')
                if 'ReleaseDate' in res.keys():
                    info_list['ReleaseDate'].append(res['ReleaseDate'])
                else:
                    info_list['ReleaseDate'].append('ReleaseDate')
                if 'director0' in res.keys():
                    info_list['region0'].append(res['region0'])
                else:
                    info_list['region0'].append('region0')

            pd.DataFrame(info_list).to_csv('../clean_data/惊悚_rd/' + label + '_' + index + '.csv',
                                           encoding='utf-8-sig')


if __name__ == "__main__":
    tag()
