from pyltp  import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller
import re

segmentor = Segmentor()  #初始化实例分词
segmentor.load_with_lexicon("ltp_data\\cws.model","ltp_data\\law_words.txt") #加载模型带词库

pdir='ltp_data\\pos.model'
pos = Postagger()                                        #初始化实例
pos.load(pdir)                                              #加载模型

"""
不使用命名实体识别部分,因为基本只能识别出分割出来的人名,意义不大,词性标注中的nh就是人名了
nermodel='ltp_data\\ner.model'
reg = NamedEntityRecognizer()                    #初始化命名实体实例
reg.load(nermodel)                                       #加载模型
"""
"""
parmodel = 'ltp_data\\parser.model'
parser = Parser()                                          #初始化命名实体实例
parser.load(parmodel)                                  #加载模型
"""
#def split_sentence(str s):



#text_path = "事件抽取例子.txt"
text_path = "法院描述抽取例子.txt"
with open(text_path, 'rt',encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        #如果一行里面有多个句子,需要分句,通常情况下为一句。
        sents = SentenceSplitter.split(line)
        #分词
        words = segmentor.segment(line) 
        print(' '.join(words))
        postags = pos.postag(words)                        #词性标注
        postags = list(postags)
        print("----------------词性标注----------------")
        print(u"词性:", postags)
        """
        #命名实体识别
        netags = reg.recognize(words, postags)         #对分词、词性标注得到的数据进行实体标识
        netags = list(netags)
        data={"reg": netags,"words":words,"tags":postags}
        print("----------------命名实体识别----------------")
        print(data)
        """
        """
        arcs = parser.parse(words, postags)              #句法分析
        print("----------------依存句法分析----------------")
        print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

        rely_id = [arc.head for arc in arcs]              # 提取依存父节点id
        relation = [arc.relation for arc in arcs]         # 提取依存关系
        heads = ['Root' if id == 0 else words[id-1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            print(relation[i] + '(' + words[i] + ', ' + heads[i] + ')')
        """
f.close()

segmentor.release()  #释放模型
pos.release()                                               #释放模型
#reg.release() 
#parser.release()                                           #释放模型





