import re
import numpy as np
from gensim.models import Word2Vec

def get_word_num():
    with open('data/stage/4阶段主题.txt', 'r', encoding='utf8') as f:
        words = f.readlines()
    num_rule = re.compile(r'0\.(.*?)\*')
    word_rule = re.compile(r'\"(.*?)\"')
    num = []
    word = []
    for i in words:
        num.append(list(map(lambda x: int(x) / 100, re.findall(num_rule, i))))  # 提取每个主题词的概率值
        word.append(re.findall(word_rule, i))  # 提取每个主题的主题词
    word = np.array(word)
    num = np.array(num)
    return word, num
def write_in(data):
    with open('data/topic_vec/4阶段主题词加权向量.txt', 'a', encoding='utf8') as f:
        for i in data:
            f.write(str(list(i)) + '\n')
    print('写入成功')

if __name__ == "__main__":
    model_path = 'output/data.model'
    model = Word2Vec.load(model_path)  # 加载训练好的word2vec模型
    word, num = get_word_num()  # 得到数据
    all_em = []
    for i, j in zip(word, num):
        word_em = []
        for w, n in zip(i, j):
            word_em.append(model.wv[w] * n)  # 得到每个主题的各个主题词的加权词向量 计算: 词向量 * (概率值 * 100)
        sum_em = sum(word_em)  # 将主题的词向量加和，得到的向量代表主题
        all_em.append(sum_em)
    write_in(all_em)
