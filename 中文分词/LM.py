#coding:utf8

import numpy as np
from dict_match import load_text, load_dict


class LanguageModel:
    def __init__(self, N, texts, dic):
        self.dic = dic
        dict_size = len(dic)
        sum = 0
        print("语言模型建立：")
        if N == 1:
            self.prob = np.zeros([dict_size])
            for i, text in enumerate(texts):
                if i % 10000 == 0:
                    print("{} 句已经训练。".format(i))
                segs = [word.split("/")[0] for word in text.split()]
                for word in segs:
                    self.prob[dic.index(word)] += 1.0
                    sum += 1
            self.constant = float(2)/sum
            self.prob /= sum
            '''
            for i in self.prob:
                if i != 0:
                    print(i)
            '''
    def get_prob(self, word):
        if word.strip() in self.dic:
            return self.prob[self.dic.index(word.strip())]
        else:
            print(word)
            return None

    def save_prob(self, filename):
        f = open(filename, "w+")
        for i in range(len(self.prob)):
            f.write(str(float(self.prob[i]))+"\n")


def build_LM(N, text_filename, dic):
    texts = load_text(text_filename)
    return LanguageModel(N, texts, dic)


def build_DAG(sentence, LM):
    dag = {}
    for i in range(len(sentence)-1, -1, -1):
        pos = []
        for j in range(i+1, len(sentence)+1):
            if LM.get_prob(sentence[i:j]) is not None:
                pos.append([j, np.log(LM.get_prob(sentence[i:j]))])
        if len(pos) == 0:
            pos.append([i+1, 0])
        dag.update(i, pos)
    return dag


def frequency(LM, test_file, save_file):
    test_s = open(test_file)
    save_f = open(save_file, "w+")

    for line in test_s:
        sen = line.strip()
        choices = {len(sen): [len(sen), 0]}
        dag = build_DAG(sen, LM)

        for i in range(len(sen)-1, -1, -1):
            max_num = -1
            max_value = -100000
            for record in dag[i]:
                num, value = record
                v = value + choices[num][1]
                if v > max_value:
                    max_num = num
                    max_value = v
            choices.update(i, [max_num, max_value])
        result = []
        k = 0
        while k < len(sen):
            result.append(sen[k:choices[k]])
            k = choices[k]
        save_f.write("/".join(result)+"\n")

    test_s.close()
    save_f.close()


def modify(forward_file, backward_file, LM, save_file):
    ff = open(forward_file)
    bf = open(backward_file)
    sf = open(save_file, "w+")
    for fl, bl in zip(ff, bf):
        fs = 0
        bs = 0
        fw = fl.split("/")
        bw = bl.split("/")
        if len(fw) < len(bw):
            sf.write(fl)
        elif len(fw) > len(bw):
            sf.write(bl)
        else:
            for word in fw:
                if LM.get_prob(word) is not None:
                    fs += np.log(LM.get_prob(word))
                else:
                    fs += np.log(LM.constant)
            for word in bw:
                if LM.get_prob(word) is not None:
                    bs += np.log(LM.get_prob(word))
                else:
                    bs += np.log(LM.constant)
            if fs > bs:
                sf.write(fl)
            else:
                sf.write(bl)

if __name__ == "__main__":
    dic, _ = load_dict()
    lm = build_LM(1, "train_seg.txt", dic)
    modify("forward_predict.txt", "backward_predict.txt", lm, "length_lm_predict.txt")