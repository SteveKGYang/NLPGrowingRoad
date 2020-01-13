#coding:utf8
import numpy as np


senf = open("199801_sent.txt", "r")
tokenf = open("199801_seg&pos.txt", "r")
trainsen = open("train_sent.txt", "w+")
traintoken = open("train_seg.txt", "w+")
testsen = open("test_sent.txt", "w+")
testtoken = open("test_seg.txt", "w+")

sens = [line.strip() for line in senf]
segs = [seg.strip() for seg in tokenf]
choose = []
for i in range(1000):
    d = np.random.randint(0, 23031)
    while int(d) in choose:
        d = np.random.randint(0, 23031)
    choose.append(int(d))

for i, sen in enumerate(sens):
    if i in choose:
        testsen.write(sen[19:]+"\n")
        testtoken.write(segs[i][22:]+"\n")
    else:
        trainsen.write(sen[19:] + "\n")
        traintoken.write(segs[i][22:] + "\n")
