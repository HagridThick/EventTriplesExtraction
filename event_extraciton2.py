from pyltp  import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller
import re
from typing import List


def event_extract(words,postages):
    #找postages中的 n nh ni nl ns 做为entity ,v作为relation,没有就缺失,其他词性作为n,v的属性保留
    #step1:先处理  的  顿号  和,  A的B取B作为e,A\B  A和B  取A+B
    #step2:找 n 和 v,找不到的缺失
    #记录所有n和v的位置,以v为分割线,将前后的n如果有多个就合并, 也可能是 n n v
    entity = ['n','nh','ni','nl','ns']  #需要更改,分为n  和 备用 nh 等
    entity_pos = []
    relation_pos = []
    for i in range(len(postages)):
        if postages[i] in entity:
            entity_pos.append(i)
        if postages[i] == 'v':
            relation_pos.append(i)
    #step3:将其他的词性有用的作为额外补充属性,添加到n和v
    print(entity_pos)
    print(relation_pos)

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
                words_list = list(words)  #转换成 list类型再处理
                print(u"分词:",words_list)
                postags = pos.postag(words)                        #词性标注
                postags = list(postags)
                print(u"词性:", postags)
                #print('\n')
                #针对分词和词性做事件抽取处理
                event_extract(words_list,postags)
f.close()

segmentor.release()  #释放模型
pos.release()                                               #释放模型