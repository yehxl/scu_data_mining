# 方法2：自主实现

# 生成第一个候选项集C1
def createC1(dataset):
    C1 = []
    # 遍历dataset， 寻找每一个项
    for transaction in dataset:
        for iterm in transaction:
            if not [iterm] in C1:
                C1.append([iterm])
    C1.sort()
    return list(map(frozenset, C1))  # 将C1由Python列表转换为不变集合（frozenset，Python中的数据结构）


# 根据候选项集生成频繁项集
def scanD(dataset, Ck, min_sup):
    # 统计每个候选集在dataset中出现的次数
    ssCnt = {}
    for tid in dataset:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt.keys():
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(dataset))
    Lk = []  # 候选项集Ck生成的频繁项集Lk
    supportData = {}  # 候选项集Cn的支持度字典
    # 计算候选项集的支持度， supportData key 候选项, value: 支持度
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= min_sup:
            Lk.append(key)
        supportData[key] = support
    return Lk, supportData


# 根据频繁项集生成下一个候选项集
def aprioriGen(Lk_1, k):
    Ck = []
    lenLk = len(Lk_1)
    for i in range(lenLk):
        L1 = list(Lk_1[i])[: k - 2]
        L1.sort()
        for j in range(i + 1, lenLk):
            L2 = list(Lk_1[j])[: k - 2]
            L2.sort()
            # 前k-2个项相同时将两个集合合并
            if L1 == L2:
                Ck.append(Lk_1[i] | Lk_1[j])
    return Ck


# apriori算法
def apriori(dataset, min_sup):
    # 创建候选项集 C1
    C1 = createC1(dataset)
    # 创建第一个频繁项集 L1, 用supportData记录所有频繁项集中的支持度
    L1, supportData = scanD(dataset, C1, min_sup)
    # 创建专门用来存放频繁项集的数组 L
    L = [L1]
    k = 2  # 表示下一个生成第几个项集
    # 在L1 的基础上，生成候选项集 C2，再生成频繁项集 L2 不断迭代，直到当前的 Li 为空集
    while (len(L[k - 2]) > 0):
        # 根据上一个 Lk 生成下一个候选项集 Ck+1
        Lk_1 = L[k - 2]
        Ck = aprioriGen(Lk_1, k)
        # 根据 Ck 生成频繁项集 Lk, 相应的记录支持度的字典
        Lk, supK = scanD(dataset, Ck, min_sup)
        # 更新supportData, L
        supportData.update(supK)
        L.append(Lk)
        k += 1

    return L, supportData


# 生成关联规则
def generateRules(L, supportData, min_conf):
    # 包含置信度的规则列表
    bigRuleList = []
    # 从频繁2项集开始遍历
    for i in range(1, len(L)):
        for freqSet in L[i]:
            # 对于每一个项集, 生成其全排列
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, min_conf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, min_conf)
    return bigRuleList


# 计算是否满足最小可信度
def calcConf(freqSet, H, supportData, brl, min_conf):
    prunedH = []
    # 用每个conseq作为后件
    for conseq in H:
        # 计算置信度
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= min_conf:
            print(freqSet - conseq, '--->', conseq, 'conf:', conf)
            # 元组中的三个元素：前件， 后件， 置信度
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    # 返回后件列表
    return prunedH


# 对规则进行评估
def rulesFromConseq(freqSet, H, supportData, brl, min_conf):
    m = len(H[0])
    if len(freqSet) > (m + 1):
        Hmp1 = aprioriGen(H, m + 1)

        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, min_conf)
        # 判断：若X->Y不满足置信度要求，那么 X- X' -> Y+ X'也不满足置信度要求，其中 X'是 X的子集
        if len(Hmp1) > 0:
            rulesFromConseq(freqSet, Hmp1, supportData, brl, min_conf)


if __name__ == "__main__":
    # 加载数据集
    dataset = [('eggs', 'bacon', 'soup'),
               ('eggs', 'bacon', 'apple'),
               ('soup', 'bacon', 'banana')]

    # 设置参数: min_sup 最小支持度， min_conf 最小置信度
    min_sup = 0.2
    min_conf = 0.7

    # 生成频繁项集和统计其支持度
    L, supportData = apriori(dataset, min_sup)

    # 根据频繁项集生成关联规则
    bigRuleList = generateRules(L, supportData, min_conf)
