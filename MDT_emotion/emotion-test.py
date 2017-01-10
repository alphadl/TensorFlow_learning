#-*-coding:utf-8-*-
'''
用例
'''
from MDT_emotion_model import MDTNLP as MDTmodel
mdt=MDTmodel(u'今天天气真不错')
print mdt.sentiments