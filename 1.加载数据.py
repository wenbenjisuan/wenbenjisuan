import os
import re
import pandas


def load_special_words(file_name):
    # 得到关键词表
    with open(rf'datasafety/{file_name}', 'r', encoding='utf8') as f:

        contents = f.readlines()

        with open(rf'reserve_word.txt', 'a', encoding='utf8') as l:

            for i in contents:
                if i[:3] == 'DE ':
                    word = list(map(lambda x: x.strip(), i[3:].split(';')))
                    word = '\n'.join(word)
                    l.write(word + '\n')


def load_title_content(file_name):
    # 得到目标语料: 标题 + 摘要 + 年份
    # 本函数顺序为: 1.得到每篇文章的标题 + 摘要，写入contents.txt。 2.得到每篇文章的关键词，写入reserve_word.txt
    titles = []
    content = []
    with open(rf'datasafety/{file_name}', 'r', encoding='utf8') as f:
        contents = f.read()
        contents = contents.split('\nER\n\n')
    for i in contents:
        t = []  # 存放标题
        c = []  # 存放摘要
        for j in i.split('\n'):
            if j[:3] == 'AB ':
                c.append(j[3:])

            elif j[:3] == 'TI ':
                t.append(j[3:])
        if len(c) == 0:  # 如果文章没有摘要， 则用空字符串来代替
            c.append('')
        if len(t) == 0:  # 如果文章没有标题， 则用空字符串代替
            t.append('')

        titles += t  # 将每篇文章的标题按顺序存入titles列表中
        content += c  # 将每篇文章的摘要按顺序存入content列表中

    with open('data/contents.txt', 'a', encoding='utf8') as f:  # 将文章 + 标题写入文件
        for i, j in zip(titles, content):
            if i == '' or j == '':  # 如果文章没有标题或摘要， 则这篇文章不写入文件
                continue
            else:
                f.write(i.strip() + '......' + j.strip() + '......' + file_name.split('-')[0] + '\n')
                # 数据格式为 标题 + ..... + 摘要 + ..... + 年份

    load_special_words(file_name)  # 得到关键词


def to_num():
    s = re.compile(r'[.,。，0-9]')
    with open('data/contents.txt', 'r', encoding='utf8') as f:
        words = f.readlines()
    words = list(map(lambda x: s.sub('', x), words))
    with open('data/contents.txt', 'a', encoding='utf8') as f:
        for i in words:
            f.write(i)


if __name__ == "__main__":
    file_name = os.listdir('datasafety')
    for i in file_name:
        load_title_content(i)
