# coding=gbk
import pandas as pd
from pandas import DataFrame as df
import Apriori2
from efficient_apriori import apriori
import math

# class_list = ['爱情', '动作', '短片','犯罪', '惊悚', '剧情', '科幻', '悬疑']
class_list = ['动作', '惊悚', '剧情','悬疑']
regions_2 = ['east','west','美国', '日韩', '中国', '法国', '英国']
regions_3 = ['美国', '日韩', '中国', '法国', '英国']
col_list = ['title', 'rd0','rd1','rd2','rd3','rd4','rd5','rd6','rd7','rd8','rd9']
years = ['1979年及以前', '1980-1999','2000年及以后']
CLASS_LAYER = [0.2, 0.7]
YEAR_LAYER = [0.3, 0.7]

"""
integrated the data in the list
:param path_list: data path
:return: data which had been integated
"""


def integrate_data(path_list: list):
    frames = []
    for i in path_list:
        frames.append(pd.read_csv(i))
    result = pd.concat(frames)
    return result


def split(data: df, layer: str = 'year') -> list:
    res = []
    tag = []
    # get the maxmum and minimum data
    if layer == 'year':
        data_min = data.loc[:, "ReleaseDate"].min()
        data_max = data.loc[:, "ReleaseDate"].max()
        data_min = data_min - data_min % 10
        data_max = data_max + 15
        # split by every ten year
        for i in range(data_min, data_max, 15):
            t = data[(data['ReleaseDate'] >= i) & (data['ReleaseDate'] < i + 15)].drop('ReleaseDate', axis=1)
            t = t.drop(t.columns[[0]], axis=1)
            if t is not None:
                res.append(t)
                tag.append(i)
    elif layer == 'class':
        for i in class_list:
            res.append(data[(data['genre0'] == i) | (data['genre1'] == i)])
    return res, tag


def layer_mining(data_list: list, name:list, layer: str = 'year'):
    # set
    min_sup = 1
    min_conf = 1
    if layer == 'year':
        min_sup, min_conf = YEAR_LAYER
    else:
        min_sup, min_conf = CLASS_LAYER
    
    ct2 = 0
    for d in data_list:
        # write the res to the file
        if layer == 'year':
            filename = "D:\\projects\\scu_data_mining\\Algorithm\\year_layer\\" + str(name[ct2]) + "_year.txt"
            temp = d[col_list]
        else:
            filename = "D:\\projects\\scu_data_mining\\Algorithm\\class_layer\\" + str(name[0]) + '_' + class_list[ct2] + "_class.txt"
            col_s = ['title']
            series_list = []
            for index, row in d.iterrows():
                if row['rd0_genre0'] == class_list[ct2] or row['rd0_genre1'] == class_list[ct2]:
                    col_s.append('rd0')
                if row['rd1_genre0'] == class_list[ct2] or row['rd1_genre1'] == class_list[ct2]:
                    col_s.append('rd1')
                if row['rd2_genre0'] == class_list[ct2] or row['rd2_genre1'] == class_list[ct2]:
                    col_s.append('rd2')
                if row['rd3_genre0'] == class_list[ct2] or row['rd3_genre1'] == class_list[ct2]:
                    col_s.append('rd3')
                if row['rd4_genre0'] == class_list[ct2] or row['rd4_genre1'] == class_list[ct2]:
                    col_s.append('rd4')
                if row['rd5_genre0'] == class_list[ct2] or row['rd5_genre1'] == class_list[ct2]:
                    col_s.append('rd5')
                if row['rd6_genre0'] == class_list[ct2] or row['rd6_genre1'] == class_list[ct2]:
                    col_s.append('rd6')
                if row['rd7_genre0'] == class_list[ct2] or row['rd7_genre1'] == class_list[ct2]:
                    col_s.append('rd7')
                if row['rd8_genre0'] == class_list[ct2] or row['rd8_genre1'] == class_list[ct2]:
                    col_s.append('rd8')
                if row['rd9_genre0'] == class_list[ct2] or row['rd9_genre1'] == class_list[ct2]:
                    col_s.append('rd9')
                series_list.append(row[col_s])
                col_s = ['title']
            frame = pd.DataFrame(series_list)
            temp = frame.values.tolist()
            for i in range(len(temp)):
                temp[i] = [temp[i] for temp[i] in temp[i] if temp[i] == temp[i]]

        if temp.shape[0] >= 5:
            # L, support_data = Apriori2.apriori(d.values.tolist(), min_sup=min_sup)
            # Apriori2.generateRules(L, supportData=support_data, min_conf=min_conf, path=filename)
            f = open(file=filename, mode="a", newline="", encoding="utf-8-sig")
            itemsets, rules = apriori(temp.values.tolist(), min_support=min_sup, min_confidence=min_conf)
            print(rules, file=f)
            f.close()
        ct2 += 1


def main():
    # integrate data
    path_list = []
    for i in class_list:
        path = 'D:\\projects\\scu_data_mining\\data\\clean_data\\' + i + '_.csv'
        path_list.append(path)
    data_integrated = integrate_data(path_list)

    # split the data by year
    data_year_layer, tag = split(data_integrated)
    # ming partern in this layer
    layer_mining(data_list=data_year_layer, name=tag)
    # split the data by class
    ct = 0
    for item in data_year_layer:
        data_class_layer, tag_n = split(item, 'class')
        layer_mining(data_list=data_class_layer, layer='class', name=[tag[ct]])
        ct += 1

def simple(path):
    src_path = path + '.csv'
    data = pd.read_csv(src_path).values.tolist()
    for i in range(len(data)):
        data[i] = [x for x in data[i] if x == x]
    f = open(file=path + '_res.txt', mode="a", newline="", encoding="utf-8-sig")
    itemsets, rules = apriori(data, min_support=0.02, min_confidence=0.7)
    print(rules, file=f)
    f.close()

if __name__ == "__main__":
    prefix = 'D:/projects/scu_data_mining/data/depth3_layer/'
    for k in years:
        for i in class_list:
            for j in regions_3:
                path = prefix + k + '/' + i + '/' + i + '_' + j + '_' + k
                simple(path)
