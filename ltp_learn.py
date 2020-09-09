from pyltp  import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller


#text = "刘某2于1974年6月25日出生，刘某2亲生父亲刘志河系原告刘某1之弟。刘某2亲生母亲王大珍于1974年11月份去世。刘某2出生后三个月，刘志河将刘某2交由原告刘某1夫妇收养 。刘某1之妻李秀婷于2013年7月27日去世。2008年起，刘某2在与刘某1夫妇共同生活期间，常发生口角、争执，双方关系恶化。"

text = ""
text_path = "收养关系纠纷总和.txt"
with open(text_path, 'rt',encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        text = text + line
         
f.close()

print(text)
#"ltp_data\\word.txt"                           #外部字典

#分句
sents = SentenceSplitter.split(text)
print("----------------分句----------------")
print('\n'.join(sents))

#中文分词
segmentor = Segmentor()  #初始化实例
#segmentor.load("ltp_data\\cws.model")  #加载模型
segmentor.load_with_lexicon("ltp_data\\cws.model","ltp_data\\word.txt")
words = segmentor.segment(text)  #分词
#print(type(words))
print("----------------分词----------------")
print(' '.join(words))
segmentor.release()  #释放模型


#词性标注
pdir='ltp_data\\pos.model'
pos = Postagger()                                        #初始化实例
pos.load(pdir)                                              #加载模型
#pos.load_with_lexicon()

postags = pos.postag(words)                        #词性标注
postags = list(postags)
print("----------------词性标注----------------")
print(u"词性:", postags)
pos.release()                                               #释放模型
#print("----------------词性标注2----------------")
#data = {"words": words, "tags": postags}
#print(data)

#命名实体识别
nermodel='ltp_data\\ner.model'
reg = NamedEntityRecognizer()                    #初始化命名实体实例
reg.load(nermodel)                                       #加载模型
netags = reg.recognize(words, postags)         #对分词、词性标注得到的数据进行实体标识
netags = list(netags)
#print("----------------命名实体识别1----------------")
#print(u"命名实体识别:", netags)

#实体识别结果
data={"reg": netags,"words":words,"tags":postags}
print("----------------命名实体识别2----------------")
print(data)
reg.release()                                                 #释放模型

#依存句法分析
parmodel = 'ltp_data\\parser.model'
parser = Parser()                                          #初始化命名实体实例
parser.load(parmodel)                                  #加载模型
arcs = parser.parse(words, postags)              #句法分析

#输出结果
#print(words)
print("----------------依存句法分析----------------")
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

rely_id = [arc.head for arc in arcs]              # 提取依存父节点id
relation = [arc.relation for arc in arcs]         # 提取依存关系
heads = ['Root' if id == 0 else words[id-1] for id in rely_id]  # 匹配依存父节点词语
for i in range(len(words)):
    print(relation[i] + '(' + words[i] + ', ' + heads[i] + ')')

parser.release()                                           #释放模型

#语义角色标注
srlmodel = 'ltp_data\\pisrl_win.model'
labeller = SementicRoleLabeller()                #初始化实例
labeller.load(srlmodel)                                 #加载模型

words = ['元芳', '你', '怎么', '看']
postags = ['nh', 'r', 'r', 'v']
arcs = parser.parse(words, postags)             #依存句法分析

#arcs使用依存句法分析的结果
roles = labeller.label(words, postags, arcs)    #语义角色标注

# 打印结果
print("----------------语义角色标注----------------")
for role in roles:
    print(role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

labeller.release()                                           #释放模型