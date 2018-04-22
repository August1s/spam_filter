#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from sklearn.feature_extraction.text import CountVectorizer


# 贝叶斯公式  P(A|B)=P(B|A)*P(A)/P(B)
# 利用贝叶斯公式进行邮件筛选
# A：收到垃圾邮件  B：邮件含有某个词语
# P(A|B)：在含有该词语的条件下A为垃圾的概率
# P(B|A)：垃圾邮件中出现该词的概率
# P(A)：收到垃圾邮件的概率，一般为0.5
# P(B)：在所有邮件中该词语出现的概率

# 联合概率计算公式  P=P1*P2...Pm/P1*P2*...Pn+(1-P1)*(1-P2)...(1-Pn)
# 利用贝叶斯公式计算出每一个词对应的条件概率后，再代入联合概率公式


# 将text中的标点符号和数字过滤,小写化
def Filter_text(text):
    str = re.sub('[^a-zA-Z]', ' ', text)
    str = re.sub(r'\s+', ' ', str)
    # print(str)
    return str.lower()


# 统计垃圾邮件和健康邮件的词频
def Count(text):
    vectorizer = CountVectorizer()
    L = ['']
    L[0] = text
    weight = vectorizer.fit_transform(L).toarray()
    word = vectorizer.get_feature_names()  # 所有文本的关键字
    print(word)
    return {word[j]: int(weight[0][j]) for j in range(len(word))}


# 求词频字典的总频数
def Sum(dic):
    n = 0
    for value in dic.values():
        n = n + value
    return n


def Bayes(test):
    test = Filter_text(test)
    test_count = sorted(Count(test).items(), key=lambda x: x[1], reverse=True)
    # print(test_count)

    # 提取前15个词作计算条件概率，代入贝叶斯联合公式
    # 如果长度不够，就取总词数
    if len(test_count) >= 15:
        r = 15
    else:
        r = len(test_count)
    # print(r)
    P = []
    for n in range(r):
        word = test_count[n][0]
        if not spam_dic.get(word):
            P.append(0.4)
        # 如果有的词是第一次出现,无法计算P(S | W),就假定这个值等于0.4。
        # 因为垃圾邮件用的往往都是某些固定的词语，所以如果你从来没见过某个词，它多半是一个正常的词。
        elif not health_dic.get(word):
            word_ham = 0.003
            # 这个值可能还需要修正,资料中给出的值是1%
            # 如果某个词只出现在垃圾邮件中, 就假定，它在正常邮件的出现频率是0.3 %
            word_spam = spam_dic[word] / spam_sum
            P.append((word_spam * 0.5) / ((word_ham * 0.5) + (word_spam * 0.5)))

        else:
            word_spam = spam_dic[word] / spam_sum
            word_ham = health_dic[word] / health_sum
            P.append((word_spam * 0.5) / ((word_ham * 0.5) + (word_spam * 0.5)))
    # print(P)
    # 计算联合概率
    p1 = 1
    p2 = 1
    for n in range(r):
        p1 = p1 * P[n]
        p2 = p2 * (1 - P[n])
    return (p1 / (p1 + p2))


# 导入文件，创建 health邮件库和spam邮件库
health = ''
spam = ''
for x in range(1, 21):
    f = open('E:/PY/spam_filter/email/ham/' + str(x) + '.txt', 'r', errors='ignore')
    health = health + f.read() + ' '
    f.close()
    f = open('E:/PY/spam_filter/email/spam/' + str(x) + '.txt', 'r', errors='ignore')
    spam = spam + f.read() + ' '
    f.close()
health = Filter_text(health)
spam = Filter_text(spam)[1:]  # spam字符串第一个是空格，不好看
# 转化为有序的字典
health_dic = dict(sorted(Count(health).items(), key=lambda x: x[1], reverse=True))
spam_dic = dict(sorted(Count(spam).items(), key=lambda x: x[1], reverse=True))
# print(spam_dic)
health_sum = Sum(health_dic)
spam_sum = Sum(spam_dic)

# 测试
for x in range(21, 26):
    f = open('E:/PY/spam_filter/email/spam/' + str(x) + '.txt', 'r', errors='ignore')
    test = f.read()
    f.close()
    print('spam' + str(x), Bayes(test))
for x in range(21, 26):
    f = open('E:/PY/spam_filter/email/ham/' + str(x) + '.txt', 'r', errors='ignore')
    test = f.read()
    f.close()
    print('ham' + str(x), Bayes(test))

