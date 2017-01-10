# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import sentiment
from . import seg
class MDTNLP(object):

    def __init__(self, doc):
        self.doc = doc
    @property
    def sentiments(self):
        return sentiment.classify(self.doc)

    @property
    def words(self):#分词测试
        return seg.seg(self.doc)

