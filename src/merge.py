import glob


def mergeAll():
    csv_list = glob.glob('../clean_data/*.csv')
    for lst in csv_list:
        f = open(lst, 'rb').read()
        with open('all.csv', 'ab') as fw:
            fw.write(f)


if __name__ == '__main__':
    mergeAll()
