from nltk.tokenize import RegexpTokenizer
import pandas
import re

def load_stop_word():
    # 加载停用词表

    with open('data/stopwords.txt', 'r', encoding='utf8') as f:
        words = f.readlines()
        words = list(map(lambda x: x.strip(), words))

    return words


def load_word_dic():
    # 获取关键词并去重
    words_dic = set()
    with open('data/reserve_word.txt', 'r', encoding='utf8') as f:
        words = f.readlines()
        for i in words:
            if len(i.strip()) != 0:
                words_dic.add(i.strip())
    return words_dic


def split_word(data):
    # 分词
    words = []
    tokenizer = RegexpTokenizer(r'\w+')
    for i in data:
        split_words = tokenizer.tokenize(i)
        words.append(split_words)
    return words
def word_counts(data):
    # 计算词频，并写入文件
    d = {}
    for i in data:

        for j in i:
            d[j] = d.get(j,0) + 1
    sort_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
    with open('data/count_words.txt', 'a', encoding='utf8') as f:
        for i, j in sort_d:
            f.write(i + ' ' + str(j) + '\n')

def add_stop_words():
    # 将词频前100的词加入停用词表
    with open('data/count_words.txt', 'r', encoding='utf8') as f:
        words = f.readlines()
        words = list(map(lambda x: x.split(' ')[0], words[:100]))
    with open('data/stopwords.txt', 'a', encoding='utf8') as f:
        for i in words:
            f.write(i + '\n')
        print('写入成功')


def to_stop_word(tokens, en_stop):  # 去停用词
    #add_stop_words()  # 由于第一次已经加入高频词，故将此语句注释
    words = []
    for i in tokens:
        to_tokens = []
        for j in i:
            if j in en_stop or len(j) <= 2:
                continue
            else:
                to_tokens.append(j)
        words.append(to_tokens)
    return words

def linner_words():
    # 关键词用下划线相连 例如: intelligence_algorithm
    c = load_word_dic()
    with open('data/contents.txt', 'r', encoding='utf8') as f:
        contents = f.read()
        contents = contents.lower()  # 将原始文本所有词语都小写
        for i in c:
            i = i.lower()  # 将关键词同样小写
            if len(i.split(' ')) == 1:
                continue
            else:
                replace_word = i.replace(' ', '_')
                contents = contents.replace(i, replace_word)
    contents = contents.split('\n')


    return contents


def get_dict_file(data):  # 将处理得到的所有词语写入文件
    with open('data/word_dict.txt', 'a', encoding='utf8') as f:
        for i in data:
            f.write(' '.join(i) + '\n')
    print('写入成功')


if __name__ == "__main__":
    content = linner_words()  # 关键词用下划线相连
    stop_tokens = load_stop_word()  # 加载停用词
    split_words = split_word(content)  # 分词
    word_counts(split_words)
    to_stop_words = to_stop_word(split_words, stop_tokens)  # 去停用词

    get_dict_file(to_stop_words)  # 写入文件
