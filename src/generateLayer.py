import csv
import glob
import pandas as pd


choices = ['剧情', '爱情', '动作', '犯罪']
genre_layer = ['剧情', '惊悚', '动作', '悬疑']
# 美国 + 英国 => 英美 region => language
region_layer = ['美国', '中国', '日韩', '英国', '法国']
# region_layer = ['west', 'east']
# (*, 1979], [1980, 1999], [2000, *)
period_layer = [1979, 1999]


def getRdInfo(prefix, suffix):
    filename = '../clean_data/' + prefix + '_rd/' + prefix + '_rd' + str(suffix) + '.csv'
    ans = []
    with open(filename) as frd:
        rd_reader = csv.reader(frd)
        for sub_row in rd_reader:
            ans.append(sub_row)
    return ans


def GenreLayer():
    for g in range(len(choices)):
        # ['genre0', 'genre1', 'director0', 'ReleaseDate', 'region0']
        depth1_rdInfo = []
        for i in range(10):
            depth1_rdInfo.append(getRdInfo(choices[g], i))

        # ['link', 'title', 'director0', 'attr0-2', 'genre0-3', 'region0-2', 'lang', 'ReleaseDate', 'rd0-9']
        # title 1; genre 6-9; region 10-12; ReleaseDate 14; rd 15-24
        tInfo = []
        g_open_file = '../clean_data/' + choices[g] + '.csv'
        with open(g_open_file) as fr:
            t_reader = csv.reader(fr)
            for row in t_reader:
                tInfo.append(row)

        for gg in range(len(genre_layer)):
            genre_type = genre_layer[gg]
            res = []
            item_num = len(tInfo)
            for i in range(item_num):
                t = tInfo[i]
                tmp = []
                if t[6] == genre_type or t[7] == genre_type or t[8] == genre_type or t[9] == genre_type:
                    tmp.append(t[1])
                for j in range(10):
                    trd = depth1_rdInfo[j][i]
                    if trd[1] == genre_type or trd[2] == genre_type:
                        l_pos = t[15 + j].find("'") + 1
                        r_pos = t[15 + j].find(",") - 1
                        tmp.append(t[15 + j][l_pos: r_pos])

                res.append(tmp)

            layer_filename = genre_type + str(g + 1) + '.csv'
            with open(layer_filename, 'a') as fw:
                writer = csv.writer(fw)
                writer.writerows(res)


def GenreToRegionLayer():
    for ii in range(len(choices)):
        # ['genre0', 'genre1', 'director0', 'ReleaseDate', 'region0']
        depth2_rdInfo = []
        for i in range(10):
            depth2_rdInfo.append(getRdInfo(choices[ii], i))

        # ['link', 'title', 'director0', 'attr0-2', 'genre0-3', 'region0-2', 'lang', 'ReleaseDate', 'rd0-9']
        # title 1; genre 6-9; region 10-12; ReleaseDate 14; rd 15-24
        tInfo = []
        # choices = ['剧情', '爱情', '动作', '犯罪']
        open_file = '../clean_data/' + choices[ii] + '.csv'
        with open(open_file) as fr:
            t_reader = csv.reader(fr)
            for row in t_reader:
                tInfo.append(row)

        for k in range(len(genre_layer)):
            genre_type = genre_layer[k]

            for region in range(len(region_layer)):
                region_type = region_layer[region]
                regions_cn = ['中国大陆', '中国香港', '中国台湾']
                regions_jk = ['日本', '韩国']
                regions_west = ['美国', '英国', '法国', '德国', '西班牙', '意大利', '加拿大', '阿根廷', '俄罗斯', '澳大利亚', '巴西']
                regions_east = ['中国大陆', '中国香港', '中国台湾', '日本', '韩国', '印度', '泰国']

                res = []
                item_num = len(tInfo)
                for i in range(item_num):
                    t = tInfo[i]
                    tmp = []

                    if region_type == '中国':
                        if (t[6] == genre_type or t[7] == genre_type or t[8] == genre_type or t[9] == genre_type) \
                            and (t[10] in regions_cn or t[11] in regions_cn or t[12] in regions_cn) \
                            and t[14] != 'unknown' and int(t[14]) > 1979 and int(t[14]) <= 1999:
                            tmp.append(t[1])
                            for j in range(10):
                                trd = depth2_rdInfo[j][i]
                                if (trd[1] == genre_type or trd[2] == genre_type) \
                                        and trd[5] in regions_cn \
                                        and trd[4] != 'unknown' and int(trd[4]) > 1979 and int(trd[4]) <= 1999:
                                    l_pos = t[15 + j].find("'") + 1
                                    r_pos = t[15 + j].find(",") - 1
                                    tmp.append(t[15 + j][l_pos: r_pos])
                    elif region_type == '日韩':
                        if (t[6] == genre_type or t[7] == genre_type or t[8] == genre_type or t[9] == genre_type) \
                                and (t[10] in regions_jk or t[11] in regions_jk or t[12] in regions_jk) \
                                and t[14] != 'unknown' and int(t[14]) > 1979 and int(t[14]) <= 1999:
                            tmp.append(t[1])
                            for j in range(10):
                                trd = depth2_rdInfo[j][i]
                                if (trd[1] == genre_type or trd[2] == genre_type) \
                                        and trd[5] in regions_jk \
                                        and trd[4] != 'unknown' and int(trd[4]) > 1979 and int(trd[4]) <= 1999:
                                    l_pos = t[15 + j].find("'") + 1
                                    r_pos = t[15 + j].find(",") - 1
                                    tmp.append(t[15 + j][l_pos: r_pos])
                    else:
                        if (t[6] == genre_type or t[7] == genre_type or t[8] == genre_type or t[9] == genre_type) \
                                and (t[10] == region_type or t[11] == region_type or t[12] == region_type) \
                                and t[14] != 'unknown' and int(t[14]) > 1979 and int(t[14]) <= 1999:
                            tmp.append(t[1])
                        for j in range(10):
                            trd = depth2_rdInfo[j][i]
                            if (trd[1] == genre_type or trd[2] == genre_type) \
                                    and trd[5] == region_type \
                                    and trd[4] != 'unknown' and int(trd[4]) > 1979 and int(trd[4]) <= 1999:
                                l_pos = t[15 + j].find("'") + 1
                                r_pos = t[15 + j].find(",") - 1
                                tmp.append(t[15 + j][l_pos: r_pos])

                    res.append(tmp)

                    # if region_type == 'west':
                    #     if (t[6] == genre_type or t[7] == genre_type or t[8] == genre_type or t[9] == genre_type) \
                    #         and (t[10] in regions_west or t[11] in regions_west or t[12] in regions_west):
                    #         tmp.append(t[1])
                    #         for j in range(10):
                    #             trd = depth2_rdInfo[j][i]
                    #             if (trd[1] == genre_type or trd[2] == genre_type) \
                    #                     and trd[5] in regions_west:
                    #                 l_pos = t[15 + j].find("'") + 1
                    #                 r_pos = t[15 + j].find(",") - 1
                    #                 tmp.append(t[15 + j][l_pos: r_pos])
                    # else:
                    #     if (t[6] == genre_type or t[7] == genre_type or t[8] == genre_type or t[9] == genre_type) \
                    #             and (t[10] in regions_east or t[11] in regions_east or t[12] in regions_east):
                    #         tmp.append(t[1])
                    #     for j in range(10):
                    #         trd = depth2_rdInfo[j][i]
                    #         if (trd[1] == genre_type or trd[2] == genre_type) \
                    #                 and trd[5] in regions_east:
                    #             l_pos = t[15 + j].find("'") + 1
                    #             r_pos = t[15 + j].find(",") - 1
                    #             tmp.append(t[15 + j][l_pos: r_pos])
                    #
                    # res.append(tmp)

                layer_filename = genre_type + '_' + region_type + str(ii + 1) + '_1980-1999.csv'
                with open(layer_filename, 'a') as fw:
                    writer = csv.writer(fw)
                    writer.writerows(res)


def GenreToRegionToPeriod():
    return


if __name__ == '__main__':
    # csv_list = glob.glob('../clean_data/剧情_rd/*.csv')
    # GenreLayer()
    GenreToRegionLayer()