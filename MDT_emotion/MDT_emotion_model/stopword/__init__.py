# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import codecs

stop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'stopwords.txt')

stop = set()
fr = codecs.open(stop_path, 'r', 'utf-8')
for word in fr:
    stop.add(word.strip())
fr.close()

def filter_stop(words):
    return list(filter(lambda x: x not in stop, words))

