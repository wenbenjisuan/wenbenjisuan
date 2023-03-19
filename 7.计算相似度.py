import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
def cos_rule(x, word):
    cos = cosine_similarity([word, x])[0][1]
    return cos

def get_sentence_em():
    with open('data/topic_vec/3阶段主题词加权向量.txt', 'r', encoding='utf8') as f:
        sentence = list(map(lambda x: eval(x.strip()), f.readlines()))

    return sentence

def get_LDA_em():
    with open('data/topic_vec/4阶段主题词加权向量.txt', 'r', encoding='utf8') as f:
        word = list(map(lambda x: eval(x.strip()), f.readlines()))
    return word
def get_cos_similar(word, sentence):
    sentences = pd.DataFrame({'sentence':sentence})
    topics = [*range(14)]  # 每次计算都要更改，值为纵轴的主题数量
    for i, j in zip(topics, word):
        sentences[i] = sentences['sentence'].apply(lambda x: cos_rule(x, j))  # 对纵轴的每个值依次和横轴的每个值进行cos相似度求值
    sentences.to_excel('data/3-4阶段相似度.xlsx')  # 写入文件

if __name__ == "__main__":
    sentence = get_sentence_em()  # 得到相似度矩阵的纵轴
    word = get_LDA_em()  # 得到相似度矩阵的横轴
    get_cos_similar(word=word, sentence=sentence)  # 每次计算都要更改内部topics的值，值为纵轴的主题数量