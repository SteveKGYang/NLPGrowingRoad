#coding:utf8

import numpy as np
import jieba


def load_stop_words():
    stop_words = []
    with open("stopwords/哈工大停用词表.txt", "r", encoding="utf8") as f:
        for line in f:
            stop_words.append(line.strip())
    with open("stopwords/中文停用词表.txt", "r", encoding="utf8") as f:
        for line in f:
            stop_words.append(line.strip())
    return stop_words


def load_dic(dic_file):
    dic = []
    with open(dic_file, "r", encoding="utf8") as f:
        for line in f:
            dic.append(line.strip())
    return dic


def load_weights(weights_file, dic):
    weights = np.zeros([len(dic), 2], dtype=float)
    count = 0
    with open(weights_file, "r", encoding="utf8") as f:
        for line in f:
            weight1, weight2 = line.strip().split()
            weights[count][0] = float(weight1)
            weights[count][1] = float(weight2)
            count += 1
    return weights


def build_dic(corpus, save_file, stop_words):
    sf = open(save_file, "w+", encoding="utf8")
    dic = []
    num = 0
    for line in corpus:
        num += 1
        if num % 1000 == 0:
            print("{} lines processed.".format(num))
        sen, _ = line.strip().split("||")
        words = sen.split("/")
        for word in words:
            if word not in dic and word not in stop_words and not word.isdigit():
                dic.append(word)
    print("词汇表大小:{}".format(len(dic)))
    for word in dic:
        sf.write(word+"\n")
    sf.close()
    return dic


def train(corpus, save_path, dic):
    weight = np.zeros([len(dic), 2], dtype=float)
    save_f = open(save_path, "w+", encoding="utf8")
    pos_result = []
    neg_result = []
    for line in corpus:
        sen, label = line.strip().split("||")
        if label == "1":
            pos_result.append(sen.split("/"))
        else:
            neg_result.append(sen.split("/"))
    print("开始进行计算：")
    for i, word in enumerate(dic):
        if i % 1000 == 0:
            print("已经完成{}个词语的计算".format(i))
        p_count = 0
        n_count = 0
        for lis in pos_result:
            if word in lis:
                p_count += 1
        for lis in neg_result:
            if word in lis:
                n_count += 1
        weight[i][0] = float(p_count) / len(pos_result)
        weight[i][1] = float(n_count) / len(neg_result)
    for i in range(len(dic)):
        save_f.write(str(weight[i][0]) + " " + str(weight[i][1])+"\n")
    save_f.close()
    return weight


def pos_neg_num(corpus):
    pos_result = []
    neg_result = []
    for line in corpus:
        sen, label = line.strip().split("||")
        if label == "1":
            pos_result.append(sen.split("/"))
        else:
            neg_result.append(sen.split("/"))
    return len(pos_result), len(neg_result)


def test(corpus, weights, dic, t_corpus):
    pos_num, neg_num = pos_neg_num(t_corpus)
    total = 0
    correct = 0
    for line in corpus:
        total += 1
        sen, label = line.strip().split("||")
        origin_words = sen.split("/")
        actual_words = []
        for word in origin_words:
            if word in dic:
                actual_words.append(word)
        pos = np.log(pos_num)
        neg = np.log(neg_num)
        for word in actual_words:
            num = dic.index(word)
            if weights[num][0] != 0:
                pos += np.log(weights[num][0])
            if weights[num][1] != 0:
                neg += np.log(weights[num][1])
        if pos > neg:
            if label == "1":
                correct += 1
        else:
            if label == "0":
                correct += 1
    print("准确率{}".format(float(correct)/total))


def analyse(sen, weights, dic, corpus):
    pos_num, neg_num = pos_neg_num(corpus)
    words = jieba.cut(sen, cut_all=False)
    print("原句为：" + sen)
    pos = np.log(pos_num)
    neg = np.log(neg_num)
    for word in words:
        if word in dic:
            num = dic.index(word)
            if weights[num][0] != 0:
                pos += np.log(weights[num][0])
            if weights[num][1] != 0:
                neg += np.log(weights[num][1])
    print("积极指数：{}".format(pos))
    print("消极指数：{}".format(neg))
    if pos > neg:
        print("情感极性为：积极")
    else:
        print("情感极性为：消极")


if __name__ == "__main__":
    corpus = []
    t_corpus = []
    with open("train.txt", "r", encoding="utf8") as f:
        for line in f:
            corpus.append(line.strip())
    with open("test.txt", "r", encoding="utf8") as f:
        for line in f:
            t_corpus.append(line.strip())
    stop_words = load_stop_words()
    #dic = build_dic(corpus, "dict.txt", stop_words)
    dic = load_dic("dict.txt")
    #weights = train(corpus, "weights.txt", dic)
    weights = load_weights("weights.txt", dic)
    #test(t_corpus, weights, dic, corpus)
    analyse("蒙牛的牛奶真好喝", weights, dic, corpus)