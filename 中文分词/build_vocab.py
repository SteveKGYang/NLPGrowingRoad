#coding:utf-8

dic = open("dict.txt", "w+")
words = []
with open("train_seg.txt", "r") as f:
    f1 = open("test_seg.txt", "r")
    for line in f:
        k = line.split()
        for item in k:
            words.append(item.split("/")[0])
    '''for line in f1:
        k = line.split()
        for item in k:
            words.append(item.split("/")[0])'''
words = set(words)
print("词表大小：{}".format(len(words)))
for word in words:
    dic.write(word+"\n")
dic.close()