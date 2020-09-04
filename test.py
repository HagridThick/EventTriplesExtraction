from triples_extraction import *

extractor = TripleExtractor()
svos = extractor.triples_main("原告刘某甲诉1974年被告母亲去世后")
print('svos', svos)