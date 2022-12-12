import csv

titleList = []
# rdList = []
existList = []


# 12-21

def searchTitle():
    with open('all.csv') as f:
        reader = csv.reader(f)
        # print(list(reader))
        for row in reader:
            # print(row[1])
            titleList.append(row[1])


def searchRd():
    rdList = []
    with open('all.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp = []
            for i in range(10):
                tmp.append(row[12 + i])
            rdList.append(tmp)

    return rdList


def tagTrueOrFalse():
    # title = []
    with open('allTitle.csv') as fr:
        reader = csv.reader(fr)
        for row in reader:
            title = row
    rdList = searchRd()
    for rds in rdList:
        tmp = []
        for rd in rds:
            if rd in title:
                tmp.append(1)
            else:
                tmp.append(0)
        existList.append(tmp)
    with open('exist.csv', 'a') as fw:
        rdWriter = csv.writer(fw)
        rdWriter.writerows(existList)


if __name__ == '__main__':
    # searchTitle()
    # with open('allTitle.csv', 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(titleList)
    tagTrueOrFalse()
