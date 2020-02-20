#coding:utf8
import jieba

import numpy as np
from random import shuffle

tf = open("train.txt", "w+", encoding="utf8")
tef = open("test.txt", "w+", encoding="utf8")

keyword = ["书籍", "平板", "手机", "水果", "洗发水", "热水器", "蒙牛", "衣服", "计算机", "酒店"]
sen = []

with open("online_shopping_10_cats.csv", "r", encoding="utf8") as f:
    for line in f:
        item = line.strip().split(",")
        sen.append([item[2], item[1]])
order = [i for i in range(len(sen))]

shuffle(order)
pos_num = 0
neg_num = 0

for i in range(len(order)):
    sent = "/".join(jieba.cut(sen[order[i]][0], cut_all=False))
    if pos_num < 4000 and sen[order[i]][1] == "1":
        tef.write(sent + "||" + sen[order[i]][1]+"\n")
        pos_num += 1
    elif neg_num < 4000 and sen[order[i]][1] == "0":
        tef.write(sent + "||" + sen[order[i]][1] + "\n")
        neg_num += 1
    else:
        tf.write(sent + "||" + sen[order[i]][1] + "\n")

tef.close()
tf.close()