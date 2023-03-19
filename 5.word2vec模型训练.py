import warnings
warnings.filterwarnings(action = 'ignore', category = UserWarning, module = 'gensim')#忽略警告
import multiprocessing
from gensim.models import Word2Vec, word2vec
from gensim.models.word2vec import LineSentence




fdir = './output/'
inp = './data/word_dicts.txt'
outp1 = fdir + 'data.model'
outp2 = fdir + 'data.vector'
#model = Word2Vec(LineSentence(inp), size = 400, window = 5, min_count = 5, workers = multiprocessing.cpu_count())
#sg=1表示使用skip_gram,hs=1,表示Hierarchical Softmax
model = Word2Vec(LineSentence(inp), vector_size= 150, window = 5, min_count =3,sg=1, hs=1, epochs=10, workers=multiprocessing.cpu_count())
# 训练word2vec模型
print(model)
model.save(outp1)
model.wv.save_word2vec_format(outp2, binary=False)
print("Word2Vec训练完成")
