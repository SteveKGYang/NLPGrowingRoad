#coding:utf8
import os

def load_dict():
    with open("dict.txt", "r") as f:
        b = f.read()
        dic = b.split("\n")

    max_len = 0
    for word in dic:
        if len(word) > max_len:
            max_len = len(word)
    return dic, max_len

def forward_match(texts, save_file, dic, max_len):
    save = open(save_file, "w+")
    seg_list = []
    for i, text in enumerate(texts):
        if i%10 == 0:
            print("{}句已处理".format(i))
        seg = []
        while len(text) > 0:
            length = min(len(text), max_len)
            try_word = text[0:length]
            while try_word not in dic:
                if len(try_word) == 1:
                    break
                try_word = try_word[:len(try_word)-1]
            seg.append(try_word)
            text = text[len(try_word):]
        save.write("/".join(seg)+"\n")
        seg_list.append(seg)
    return seg_list

def backward_match(texts, save_file, dic, max_len):
    save = open(save_file, "w+")
    seg_list = []
    for i, text in enumerate(texts):
        if i%10 == 0:
            print("{}句已处理".format(i))
        seg = []
        while len(text) > 0:
            length = min(len(text), max_len)
            try_word = text[len(text)-length:]
            while try_word not in dic:
                if len(try_word) == 1:
                    break
                try_word = try_word[1:]
            seg.append(try_word)
            text = text[:len(text)-len(try_word)]
        seg.reverse()
        save.write("/".join(seg)+"\n")
        seg_list.append(seg)
    return seg_list

def load_text(filename):
    texts = []
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        for line in f:
            texts.append(line.strip())
    return texts


if __name__ == "__main__":
    dic, max_len = load_dict()
    text = load_text("test_sent.txt")
    a = forward_match(text, "forward_predict.txt", dic, max_len)