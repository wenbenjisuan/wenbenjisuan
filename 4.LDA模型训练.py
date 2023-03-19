import math
import matplotlib
import pandas as pd
from gensim import corpora, models
import gensim
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
import matplotlib.pyplot as plt
def load_texts():
    #df = pd.read_excel('data/content_excel.xlsx') #总主题
    df = pd.read_excel('data/stage/4阶段.xlsx')
    new_df = df.iloc[:,-1].apply(lambda x: x.split(' ')).to_list()
    print(len(new_df))

    return new_df

def coherence_plot(data_set, s):
    num_topics = [*range(1, 20)]


    plt.plot(num_topics, s)
    plt.xlabel('主题数目')
    plt.ylabel('困惑度大小')
    plt.rcParams['font.sans-serif']=['SimHei']
    matplotlib.rcParams['axes.unicode_minus']=False
    #plt.title('主题-困惑度变化情况')
    plt.show()


def lda_model_train(num_topics, dictionary, corpus):

    ldamodel = LdaModel(corpus, num_topics=num_topics, id2word = dictionary, alpha=0.1, eta=0.1, minimum_probability=1e-8,
                      update_every=1, chunksize=100, passes=1)
    print(ldamodel.print_topics(num_topics=num_topics, num_words=15))
    return ldamodel
def perplexity(ldamodel: gensim.models.LdaModel, data, dictionary: gensim.corpora.Dictionary):
    """
    计算LDA模型困惑度

    :param ldamodel:  lda模型
    :param data: 计算困惑度需要训练数据
    :param dictionary: 文本处理后的Dictionary，使用corpora.Dictionary(my_data)处理训练gensim模型时的数据 my_data 后得到的
    :return: 返回困惑度
    """
    size_dictionary = len(dictionary.keys())
    testset = []
    for i in data:
        testset.append(dictionary.doc2bow(i))
    num_topics = ldamodel.num_topics
    prob_doc_sum = 0.0
    topic_word_list = []  # store the probablity of topic-word:[(u'business', 0.010020942661849608),(u'family', 0.0088027946271537413)...]
    for topic_id in range(num_topics):
        topic_word = ldamodel.show_topic(topic_id, size_dictionary)
        dic = {}
        for word, probability in topic_word:
            dic[word] = probability
        topic_word_list.append(dic)
    doc_topics_ist = []  # store the doc-topic tuples:[(0, 0.0006211180124223594),(1, 0.0006211180124223594),...]
    for doc in testset:
        doc_topics_ist.append(ldamodel.get_document_topics(doc, minimum_probability=0))
    testset_word_num = 0
    for i in range(len(testset)):
        prob_doc = 0.0  # the probablity of the doc
        doc = testset[i]
        doc_word_num = 0  # the num of words in the doc
        for word_id, num in doc:
            prob_word = 0.0  # the probablity of the word
            doc_word_num += num
            word = dictionary[word_id]
            for topic_id in range(num_topics):
                # cal p(w) : p(w) = sumz(p(z)*p(w|z))
                prob_topic = doc_topics_ist[i][topic_id][1]
                prob_topic_word = topic_word_list[topic_id][word]
                prob_word += prob_topic * prob_topic_word
            prob_doc += math.log(prob_word)  # p(d) = sum(log(p(w)))
        prob_doc_sum += prob_doc
        testset_word_num += doc_word_num
    prep = math.exp(-prob_doc_sum / testset_word_num)  # perplexity = exp(-sum(p(d)/sum(Nd))
    # print("LDA模型困惑度 : %s" % prep)
    return prep

if __name__ == '__main__':
    data_set = load_texts()[:-1]
    #coherence_plot(data_set)
    pro_list = []
    dictionary = corpora.Dictionary(data_set)
    corpus = [dictionary.doc2bow(text) for text in data_set]
    print(len(dictionary))
    for i in range(1,20):
        lda_model = lda_model_train(i, dictionary=dictionary, corpus=corpus)
        s = perplexity(lda_model, data_set, dictionary=dictionary)
        print(f'主题数：{i}', '困惑度：',s)
        pro_list.append(s)
    coherence_plot(data_set, pro_list)