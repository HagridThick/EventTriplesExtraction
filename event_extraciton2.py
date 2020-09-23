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
    entity_list = ['ni','nl','ns']
    eproperty_list = ['m','u']
    vproperty_list =['a','d','p']
    #pos列表
    entity_pos = []
    backup_entity_pos = []
    eproperty_pos = []
    
    relation_pos = []
    vproperty_pos = []

    wp_pos = []
    nt_pos = [] #时间
    #记录各词性位置
    for i in range(len(postages)):
        if postages[i] == "wp" or postages[i] == "c"  and words[i] != "。":  #过滤句尾逗号
            wp_pos.append(i)  #记录顿号的位置,最后将顿号前后的n合并
        if postages[i] == "n" or postages[i] == "nh" :
            entity_pos.append(i) #主体客体
        if postages[i] in entity_list:
            backup_entity_pos.append(i)
        if postages[i] == "v" :
            relation_pos.append(i)#事件动作
        if postages[i] in eproperty_list:
            eproperty_pos.append(i)
        if postages[i] in vproperty_list:
            vproperty_pos.append(i)
        if postages[i] == "nt":
            nt_pos.append(i)
    #输出结果
    print("entity_pos:",entity_pos)
    print("backup_entity_pos:",backup_entity_pos)
    print("eproperty_pos:",eproperty_pos)  #直接添加进属性
    print("relation_pos:",relation_pos)
    print("vproperty_pos:",vproperty_pos)  #直接添加进属性
    #print("wp_pos:",wp_pos)
    #print("nt_pos:",nt_pos)

    #转化成事件三元组,主体缺失由前面补充
    #格式为 1主体 2关系 3客体 4主体属性 5关系属性 6客体属性
    """
    rule1: entity_pos 为空,则用backup_entity_pos 作为 e
    rule2: 顿号前后的e合并, 多个e合并(以v为区分)
    rule3: nt作为这个事件的时间属性,放在v里面 
    """
    #在entity_pos relation_pos 找 123
    subject = ""
    object_result = ""

    sj_property = ""
    r_property = ""
    ob_property = ""
    
    if len(relation_pos) != 0:
        relation = words[relation_pos[0]]
        for i in entity_pos:
            if i<relation_pos[0]:
                subject = subject + words[i]
            else:
                object_result = object_result + words[i]
        #添加backup_entity_pos   eproperty_pos vproperty_pos 到属性
        for i in backup_entity_pos:
            if i < relation_pos[0]:
                sj_property = sj_property + ":" + words[i]
            else:
                ob_property = ob_property + ":" + words[i]
        for i in eproperty_pos:
            if i < relation_pos[0]:
                sj_property = sj_property + ":" + words[i]
            else:
                ob_property = ob_property + ":" + words[i]
        for i in vproperty_pos:
            r_property = r_property + ":" + words[i]
        print(subject)
        print(relation)
        print(object_result)
        print(sj_property)
        print(r_property)
        print(ob_property)
    else:
        #没有v就没有事件
        print("nothing happened in this sentence")



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