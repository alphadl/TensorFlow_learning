# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from .. import stopword
from .. import seg
from ..classification.bayes import Bayes

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'sentiment.marshal_mix')


class Sentiment(object):

    def __init__(self):
        self.classifier = Bayes()

    def load(self, fname=data_path, iszip=True):
        self.classifier.load(fname, iszip)

    def handle(self, doc):
        words = seg.seg(doc)
        words = stopword.filter_stop(words)
        return words

    def classify(self, sent):
        ret, prob = self.classifier.classify(self.handle(sent))
        if ret == 'pos':
            return round((prob-0.5)*100,2)
        return round(((1-prob)-0.5)*100,2)


classifier = Sentiment()
classifier.load()

def classify(sent):
    return classifier.classify(sent)
