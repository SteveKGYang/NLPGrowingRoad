#encoding: gbk
from tools import remove_dash, deal_num


ftr = open("train_seg.txt")
fte = open("test_seg.txt")
fw = open("vocab.txt", "w+")
fn = open("newwords.txt", "w+")

words = []
for line in ftr:
    pwords = line.split()
    for word in pwords:
        w = remove_dash(word.split("/")[0])
        for chra in w:
            if chra in '０１２３４５６９７８一二三四五六七八九十零':
                w = deal_num(w)
        words.append(w)

words = set(words)
print("一共有{}个词".format(len(words)))

twords = []
for line in fte:
    pwords = line.split()
    for word in pwords:
        w = remove_dash(word.split("/")[0])
        for chra in w:
            if chra in '０１２３４５６９７８一二三四五六七八九十零':
                w = deal_num(w)
        twords.append(w)

twords = set(twords)

nwo = 0
num = 0
nwords = []
for word in twords:
    if word not in words:
        nwo += 1
        for chra in word:
            if chra in '０１２３４５６９７８一二三四五六七八九十零':
                num += 1
                break
        nwords.append(word)
nwords = set(nwords)
print("测试数据中有{}个词不在训练词表中".format(nwo))
print("其中有{}个含数字词".format(num))
for word in words:
    fw.write(word+"\n")
for word in nwords:
    fn.write(word+"\n")

ftr.close()
fte.close()
fw.close()
fn.close()