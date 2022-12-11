# coding=gbk
import pandas as pd
from pandas import DataFrame as df
import Apriori2
from efficient_apriori import apriori

# class_list = ['����', '����', '��Ƭ','����', '���', '����', '�ƻ�', '����']
class_list = ['����', '����', '��Ƭ','����', '���', '����', '�ƻ�', '����']
col_list = ['title', 'rd0','rd1','rd2','rd3','rd4','rd5','rd6','rd7','rd8','rd9']
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
        else:
            filename = "D:\\projects\\scu_data_mining\\Algorithm\\class_layer\\" + str(name[0]) + '_' + class_list[ct2] + "_class.txt"
        
        temp = d[col_list]
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


if __name__ == "__main__":
    main()
