from pyltp  import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller
import re
from typing import List

segmentor = Segmentor()  #初始化实例分词
segmentor.load_with_lexicon("ltp_data\\cws.model","ltp_data\\law_words.txt") #加载模型带词库

pdir='ltp_data\\pos.model'
pos = Postagger()                                        #初始化实例
pos.load(pdir)                                              #加载模型

text_path = "test.txt"
with open(text_path, 'rt',encoding='utf-8') as f:
    for line in f:
        sents = SentenceSplitter.split(line.rstrip())  #去掉行尾的空格,并分句
        for i in sents: #对每一句话进行事件抽取,按照逗号进行分隔,每一短话都是一个事件
            short_sents = re.split(r'[,，]\s*', i)  #匹配中英文逗号
            for j in short_sents:
                words = segmentor.segment(j)   #<pyltp.VectorOfString object at 0x00000247E3013DB0>
                postags = pos.postag(words)                        #词性标注
                postags = list(postags)
                print(u"词性:", postags)
                print('\n')
                #针对分词和词性做处理
                words_list = list(words)  #转换成 list类型再处理

f.close()

segmentor.release()  #释放模型
pos.release()                                               #释放模型



def event_extract(words,postages):
    return 0


