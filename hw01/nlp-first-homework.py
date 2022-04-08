import jieba
import math
import time
import os
import re
class GetData():

    # 1 初始化
    def __init__(self, root):
        self.root = root

    def ergodic(self):
        return GetData.getCorpus(self, self.root)

    def getCorpus(self, root):
        corpus = []
        r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'  # 用户也可以在此进行自定义过滤字符
        listdir = os.listdir(root)
        count=0
        for file in listdir:
            path  = os.path.join(root, file)
            if os.path.isfile(path):
                with open(os.path.abspath(path), "r", encoding='ansi') as file:
                    filecontext = file.read();
                    filecontext = re.sub(r1, '', filecontext)
                    filecontext = filecontext.replace("\n", '')
                    filecontext = filecontext.replace(" ", '')
                    filecontext = filecontext.replace("本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com",'')
                    #seg_list = jieba.cut(filecontext, cut_all=True)
                    #corpus += seg_list
                    count += len(filecontext)
                    corpus.append(filecontext)
            elif os.path.isdir(path):
                GetData.AllFiles(self, path)
        return corpus,count

# 词频统计，方便计算信息熵
def tf(tf_dic, words):

    for i in range(len(words)-1):
        tf_dic[words[i]] = tf_dic.get(words[i], 0) + 1

def bigram_term_frequency(tf_dic, words):
    for i in range(len(words)-1):
        tf_dic[(words[i], words[i+1])] = tf_dic.get((words[i], words[i+1]), 0) + 1

def trigram_term_frequency(tf_dic, words):
    for i in range(len(words)-2):
        tf_dic[((words[i], words[i+1]), words[i+2])] = tf_dic.get(((words[i], words[i+1]), words[i+2]), 0) + 1

def calculate_unigram(corpus,count):
    before = time.time()
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    for line in corpus:
        for x in jieba.cut(line):
            split_words.append(x)
            words_len += 1
        tf(words_tf, split_words)
        split_words = []
        line_count += 1

    print("语料库字数:", count)
    print("分词个数:", words_len)
    print("平均词长:", round(count / words_len, 5))
    entropy = []
    for uni_word in words_tf.items():
        entropy.append(-(uni_word[1] / words_len) * math.log(uni_word[1] / words_len, 2))
    print("基于词的一元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")
    after = time.time()
    print("运行时间:", round(after - before, 5), "秒")

def calculate_bigram(corpus, count):
    before = time.time()
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    bigram_tf = {}

    for line in corpus:
        for x in jieba.cut(line):
            split_words.append(x)
            words_len += 1

        tf(words_tf, split_words)
        bigram_term_frequency(bigram_tf, split_words)

        split_words = []
        line_count += 1

    print("语料库字数:", count)
    print("分词个数:", words_len)
    print("平均词长:", round(count / words_len, 5))

    bigram_len = sum([dic[1] for dic in bigram_tf.items()])
    print("二元模型长度:", bigram_len)

    entropy = []
    for bi_word in bigram_tf.items():
        jp_xy = bi_word[1] / bigram_len  # 计算联合概率p(x,y)
        cp_xy = bi_word[1] / words_tf[bi_word[0][0]]  # 计算条件概率p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算二元模型的信息熵
    print("基于词的二元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")

    after = time.time()
    print("运行时间:", round((after - before), 5), "秒")

def calculate_trigram(corpus,count):
    before = time.time()
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    trigram_tf = {}

    for line in corpus:
        for x in jieba.cut(line):
            split_words.append(x)
            words_len += 1

        bigram_term_frequency(words_tf, split_words)
        trigram_term_frequency(trigram_tf, split_words)

        split_words = []
        line_count += 1

    print("语料库字数:", count)
    print("分词个数:", words_len)
    print("平均词长:", round(count / words_len, 5))

    trigram_len = sum([dic[1] for dic in trigram_tf.items()])
    print("三元模型长度:", trigram_len)

    entropy = []
    for tri_word in trigram_tf.items():
        jp_xy = tri_word[1] / trigram_len  # 计算联合概率p(x,y)
        cp_xy = tri_word[1] / words_tf[tri_word[0][0]]  # 计算条件概率p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算三元模型的信息熵
    print("基于词的三元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")

    after = time.time()
    print("运行时间:", round(after - before , 10), "秒")


if __name__ == '__main__':
    data = GetData("./data1/")
    corpus,count = data.ergodic()
    calculate_unigram(corpus, count)
    calculate_bigram(corpus,count)
    calculate_trigram(corpus,count)
