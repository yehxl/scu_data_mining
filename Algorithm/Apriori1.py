# 方法1：简单调库
from efficient_apriori import apriori

# 数据集设置
transactions = [['eggs', 'bacon', 'soup'],
                ['eggs', 'bacon', 'apple'],
                ['soup', 'bacon', 'banana']]

# #从文件中读入数据集
# import tensorflow as tf
# dataset = tf.data.TextLineDataset(['1.csv', '2.csv']).skip(1)
# for item in dataset:
#     print(item.numpy())

itemsets, rules = apriori(transactions, min_support=0.2, min_confidence=1)
# 每一次算法的频繁项集
print(itemsets)
# 最终结果
print(rules)
