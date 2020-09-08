# coding=utf8
import re
from triple_extraction import *
# coding=gbk
extractor = TripleExtractor()
svos = extractor.triples_main("经审理查明，原告单身生活多年膝下无子，1995年6月5日经人介绍原告收养被告为养子，将被告户口上在原告名义，但未办理过养手续，在日后的实际生活中也未在一起生活。")
print('svos', svos)
