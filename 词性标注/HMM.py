import numpy as np
from tools import remove_dash, deal_num
UNK = "UNK"


class HMM:
    def __init__(self, states, corpus, dicts, launch_name, state_name, start_name, numda):
        dicts.append(UNK)
        self.states = states
        self.dicts = dicts
        self.launch_weights = np.zeros([len(states), len(dicts)], dtype=np.float32)
        self.trans_weights = np.zeros([len(states), len(states)], dtype=np.float32)
        self.start_weights = np.zeros([len(states)], dtype=np.float32)
        count = 0
        if corpus is not None:
            for line in corpus:
                if count % 1000 == 0:
                    print("当前处理{}个句子".format(count))
                if len(line) <= 1:
                    continue
                count += 1
                line = remove_dash(line.strip())
                words = line.split()
                _, s = words[0].split("/")
                if "]" in s:
                    s = s.split("]")[0]
                if s not in states:
                    s = s[0]
                self.start_weights[int(states.index(s))] += 1
                for i in range(len(words)-1):
                    word1, state1 = words[i].split("/")
                    word2, state2 = words[i+1].split("/")
                    for chra in word1:
                        if chra in '０１２３４５６９７８一二三四五六七八九十零':
                            word1 = deal_num(word1)
                    for chra in word2:
                        if chra in '０１２３４５６９７８一二三四五六七八九十零':
                            word2 = deal_num(word2)
                    if word1 not in dicts:
                        word1 = UNK
                    if word2 not in dicts:
                        word2 = UNK
                    if "]" in state1:
                        state1 = state1.split("]")[0]
                    if "]" in state2:
                        state2 = state2.split("]")[0]
                    if state1 not in states:
                        state1 = state1[0]
                    if state2 not in states:
                        state2 = state2[0]
                    self.launch_weights[int(states.index(state1))][int(dicts.index(word1))] += 1
                    self.launch_weights[int(states.index(state2))][int(dicts.index(word2))] += 1
                    self.trans_weights[int(states.index(state1))][int(states.index(state2))] += 1
            self.laplace_smoothing(numda)
            self.save_weights(launch_name, state_name, start_name)
        else:
            self.load_weights(launch_name, state_name, start_name)

    def laplace_smoothing(self, numda):
        for i in range(len(self.states)):
            self.start_weights[i] += numda
            for j in range(len(self.states)):
                self.trans_weights[i][j] += numda
        for i in range(len(self.states)):
            for j in range(len(self.dicts)):
                self.launch_weights[i][j] += numda
        for i in range(len(self.states)):
            k = False
            for j in range(len(self.dicts)):
                if self.launch_weights[i][j] > 2:
                    k = True
                    break
            if not k:
                print("hhhhhhhhhh")
        for i in range(len(self.states)):
            self.trans_weights[i] /= np.sum(self.trans_weights[i])
            self.launch_weights[i] /= np.sum(self.launch_weights[i])
        self.start_weights /= np.sum(self.start_weights)

    def save_weights(self, launch_name, state_name, start_name):
        fl = open(launch_name, "w+")
        fs = open(state_name, "w+")
        fst = open(start_name, "w+")
        sts = ''

        for i in range(len(self.states)):
            ls = ''
            ss = ''
            sts += str(self.start_weights[i]) + " "
            for j in range(len(self.states)):
                ss += str(self.trans_weights[i][j]) + " "
            for j in range(len(self.dicts)):
                ls += str(self.launch_weights[i][j])+" "
            ls += "\n"
            ss += "\n"
            fl.write(ls)
            fs.write(ss)
        sts += "\n"
        fst.write(sts)

        fl.close()
        fs.close()
        fst.close()

    def load_weights(self, launch_name, state_name, start_name):
        fl = open(launch_name)
        fs = open(state_name)
        fst = open(start_name)
        for line in fst:
            weights = line.strip().split()
            for i, weight in enumerate(weights):
                self.start_weights[i] = weight
        for i, line in enumerate(fl):
            weights = line.strip().split()
            for j in range(len(weights)):
                self.launch_weights[i][j] = float(weights[j])
        for i, line in enumerate(fs):
            weights = line.strip().split()
            for j in range(len(weights)):
                self.trans_weights[i][j] = float(weights[j])
        fl.close()
        fs.close()

    def build_sens(self, filename):
        sens = []
        with open(filename) as f:
            for line in f:
                s = ''
                words = line.split()
                for wor in words:
                    w, state = wor.split("/")
                    s += (w + " ")
                s += "\n"
                sens.append(s)
        return sens

    def viterbi(self, sens, write_filename):
        wf = open(write_filename, "w+")
        count = 0
        for sen in sens:
            words = sen.split()
            if len(words) <= 1:
                continue
            r_value = np.zeros([len(words), len(self.states)])
            r_route = np.zeros([len(words), len(self.states)])
            for i, wor in enumerate(words):
                if wor not in self.dicts:
                    wor = UNK
                if i == 0:
                    for j in range(len(self.states)):
                        r_value[i][j] = np.log(self.start_weights[j]*self.launch_weights[j][int(self.dicts.index(wor))])
                        r_route[i][j] = -1
                else:
                    for j in range(len(self.states)):
                        b_value = -100000000
                        b_route = None
                        for k in range(len(self.states)):
                            m = r_value[i-1][k] + np.log(self.trans_weights[k][j]
                                                        *self.launch_weights[j][self.dicts.index(wor)])
                            if m > b_value:
                                b_value = m
                                b_route = k
                        if b_route is not None:
                            r_value[i][j] = b_value
                            r_route[i][j] = b_route
                        else:
                            print("NONE ROUTE FAULT")
            route = []
            max_index = 0
            max_value = r_value[len(words)-1][0]
            for i in range(len(r_value[len(words)-1])):
                if r_value[len(words)-1][i] > max_value:
                    max_value = r_value[len(words)-1][i]
                    max_index = i
            for i in range(len(words)-1, -1, -1):
                route.append(self.states[int(max_index)])
                max_index = r_route[i][int(max_index)]
            sentence = ''
            for i, wo in enumerate(words):
                sentence += wo+"/"+route[len(words)-1-i] + "  "
            sentence += "\n"
            wf.write(sentence)
        wf.close()


if __name__ == "__main__":
    states = []
    with open("states.txt") as f:
        for word in f:
            states.append(word.strip())
    corpus = []
    with open("train_seg.txt") as f:
        for sen in f:
            corpus.append(sen.strip())
    dicts = []
    with open("vocab.txt") as f:
        for sen in f:
            dicts.append(sen.strip())
    hmm = HMM(states, None, dicts, "launch1.txt", "state1.txt", "start1.txt", 2)
    sens = hmm.build_sens("test_seg.txt")
    hmm.viterbi(sens, "result.txt")

