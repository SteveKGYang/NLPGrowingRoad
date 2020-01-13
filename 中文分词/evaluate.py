#coding:utf8
import os

def evaluate(generated_filename, golden_filename):
    assert os.path.exists(generated_filename) and os.path.exists(golden_filename)
    generated_file = open(generated_filename)
    golden_file = open(golden_filename)
    n = 0
    e = 0
    c = 0
    for generated, golden in zip(generated_file, golden_file):
        generated_words = generated.split("/")
        goldens = golden.split()
        golden_words = [line.split("/")[0] for line in goldens]
        if len(golden_words) == 0:
            continue
        n += len(golden_words)
        for word in generated_words:
            if word.strip() not in golden_words:
                e += 1
            else:
                c += 1
    P = float(c)/(c+e)
    R = float(c)/n
    F = float(2 * P * R)/(P + R)
    return P, R, F

if __name__ == "__main__":
    count = 0
    with open("forward_predict.txt", "r") as f:
        f1 = open("backward_predict.txt", "r")
        for l1, l2 in zip(f, f1):
            if l1 != l2:
                count += 1
                print(l1)
                print(l2)
    print(count)