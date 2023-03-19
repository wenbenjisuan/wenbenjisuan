
import pandas
import pandas as pd

with open('data/word_dict.txt','r', encoding='utf8') as f:
    content = f.readlines()
    text = list(map(lambda x: ' '.join(x.split(' ')[:-1]).strip(), content))  # 提取每条数据中的题目 + 摘要
with open('data/contents.txt', 'r', encoding='utf8') as f:
    texts = f.readlines()

    year = list(map(lambda x: x.split('......')[-1].strip().replace('.',''), texts))  # 提取每条数据中的年份

d = {'title_content':text, 'year':year}  # 将数据转换为字典格式
pd.DataFrame(d).to_excel('data/content_excel.xlsx')  # 写入excel表格
