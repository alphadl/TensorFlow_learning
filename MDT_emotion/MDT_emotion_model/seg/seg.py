# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from ..utils.tnt import TnT
from .y09_2047 import CharacterBasedGenerativeModel


class Seg(object):

    def __init__(self, name='other'):
        if name == 'tnt':
            self.segger = TnT()
        else:
            self.segger = CharacterBasedGenerativeModel()

    def load(self, fname, iszip=True):
        self.segger.load(fname, iszip)

    def seg(self, sentence):
        ret = self.segger.tag(sentence)
        tmp = ''
        for i in ret:
            if i[1] == 'e':
                yield tmp+i[0]
                tmp = ''
            elif i[1] == 'b' or i[1] == 's':
                if tmp:
                    yield tmp
                tmp = i[0]
            else:
                tmp += i[0]
        if tmp:
            yield tmp


if __name__ == '__main__':
    seg = Seg()
    print(' '.join(seg.seg('主要是用来放置一些简单快速的中文分词')))
