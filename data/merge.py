import glob

years = ['1979年及以前', '1980-1999','2000年及以后']
categories = ['动作','悬疑','惊悚','剧情']
regions = ['美国', '日韩', '中国', '法国', '英国']

def mergeAll(year, category, region):
    prefix = 'D:/projects/scu_data_mining/data/depth3_layer/'
    path = prefix + year + '/' + category + '/' + region + '/*.csv'
    csv_list = glob.glob(path)
    for lst in csv_list:
        print(lst)
        f = open(lst, 'rb').read()
        new_path = prefix + year + '/' + category + '/' + category + '_' + region + '_' + year + '.csv'
        with open(new_path, 'ab') as fw:
            fw.write(f)
            print('ok')


if __name__ == '__main__':
    for year in years:
        for category in categories:
            for region in regions:
                mergeAll(year, category, region)
