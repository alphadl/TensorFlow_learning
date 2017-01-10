# -*- coding:utf-8 -*- 
import pandas as pd
from datetime import datetime
import jieba
import jieba.analyse
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
from MDT_emotion_model import MDTNLP as MDTmodel
import sys
from string import *

#pandas解析JSON数据格式
def get_json_data(json):
    data=pd.DataFrame(pd.read_json(json),columns=['authorId','authorName','comments','content','isCurrentUser',
                                                         'likes','mediaListSize','snsId','timestamp','date','year',
                                                         'month','hour','words','keywords','emotion'])
    for i in range(len(data)):
        data.loc[i,'date'] =data['timestamp'][i].strftime('%Y-%m-%d')
        data.loc[i,'year'] =data['timestamp'][i].strftime('%Y') 
        data.loc[i,'month'] =data['timestamp'][i].strftime('%m')
        data.loc[i,'hour'] =data['timestamp'][i].strftime('%H')
        data.loc[i,'emotion']=MDTmodel(data.content[i]).sentiments
        #data['words'][i] = list(jieba.cut(data.content[i], cut_all=False))
        #data['keywords'][i] = jieba.analyse.extract_tags(data.content[i], topK=3)  
    return data
#获取所需年份的数据
def get_json_year(data):
    data=data[data.year=='2016']
    data.index=[i for i in range(len(data))]
    return data
#2016全年朋友圈总记录数
def get_year_moments(data):
    df = len(data)
    return df
#2016全年朋友圈总图片、视频和转载数
def get_year_media(data):
    df = sum(data.mediaListSize)
    return df
#2016年朋友圈总字数
def get_year_words(data):
    allwords=' '.join(data.content)
    num=0
    for line in allwords:
        num=num + len(split(line))
    return num
#朋友圈总记录数最多的月份和数量
def get_month_max(data):
    df1=data.snsId.groupby(data.month).count()
    maxvalues=df1.max()
    maxdata=df1[df1.values==maxvalues]  
    return maxdata
#朋友圈总记录数最少的月份和数量
def get_month_min(data):
    df1=data.snsId.groupby(data.month).count()
    minvalues=df1.min()
    mindata=df1[df1.values==minvalues]  
    return mindata
#各月份说说计数
def get_all_month(data):
    y=pd.DataFrame(columns=['w'])
    df=data.snsId.groupby(data.month).size()
    y.w=[str((df.index[i],df.values[i])) for i in range(len(df))]
    return ' '.join(y.w.values)
#各月份说说情感值
def get_month_emotion(data):
    y=pd.DataFrame(columns=['w'])
    df=data.emotion.groupby(data.month).mean()
    y.w=[str((df.index[i],df.values[i])) for i in range(len(df))]
    return ' '.join(y.w.values) 
#朋友圈总记录数最多的日期和数量
def get_date_max(data):
    df=data.snsId.groupby(data.date).count()
    maxvalues=df.max()
    maxdata=df[df.values==maxvalues]  
    return maxdata 
#朋友圈总记录数最多的时段和数量
def get_hour_max(data):
    df=data.snsId.groupby(data.hour).count()
    maxvalues=df.max()
    maxdata=df[df.values==maxvalues]  
    return maxdata
#朋友圈所有记录的前100个关键词
def key_word_cut(data):
    all_words=' '.join(data.content)
    key_words=list(jieba.analyse.extract_tags(all_words, topK=100))
    return key_words
#朋友圈词云图的构建
def word_cloud(data):
    stopwords=pd.read_excel('./workfile/stop_words_zh_gbk.xlsx')
    stopwords.columns=['stops']
    all_words=' '.join(data.content)
    segs=pd.DataFrame(jieba.cut(all_words, cut_all=False),columns=['words'])
    df=segs.groupby(segs.words).size()
    key_word=key_word_cut(data)
    word_freq=[(df.index[i],df.values[i]) for i in range(len(df)) if df.index[i] not in stopwords.stops.values and df.index[i] in key_word]
    wc = WordCloud(font_path='./workfile/msyh.ttf',background_color="white",max_font_size=80,random_state=40,margin=5)
    wc.generate_from_frequencies(word_freq)
    wc.to_file('./picresult/'+data.authorId[0]+'.png')
#朋友圈影响力等级
def get_influe_power(data):
    a=all_num=get_year_moments(data)
    b=media_num=get_year_media(data)
    c=total_words=get_year_words(data)
    a_power=0
    b_power=0
    c_power=0
    if a>=350:
        a_power=a_power+10
    elif a>=250:
        a_power=a_power+8 
    elif a>=180:
        a_power=a_power+6
    elif a>=90:
        a_power=a_power+5
    else:
        a_power=a_power+4
    if b>=350:
        b_power=b_power+10
    elif b>=250:
        b_power=b_power+8 
    elif b>=180:
        b_power=b_power+6
    elif b>=90:
        b_power=b_power+5
    else:
        b_power=b_power+4
    if c>=3000:
        c_power=c_power+10
    elif c>=2000:
        c_power=c_power+8 
    else:
        c_power=c_power+6 
    return round((a_power+b_power+c_power)/3)    

def get_result(json):
    data1=get_json_data(json) #微信某用户JSON数据
    data2=get_json_year(data1)
    word_cloud(data2)
    df=pd.DataFrame(index=['data'],columns=['authorId','power','all_num','media_num','total_words','monthmax','monthmax_num','monthmin',
                                                       'monthmin_num','datemax','datemax_num','hour_prefer','all_month','month_emotion'])       
    df.authorId=data2.authorId[0]
    df.power=get_influe_power(data2)
    df.all_num=get_year_moments(data2)
    df.media_num=get_year_media(data2)
    df.total_words=get_year_words(data2)
    
    a=get_month_max(data2)
    df.monthmax=a.index.values[0]
    df.monthmax_num=a.values[0]

    b=get_month_min(data2)
    df.monthmin=b.index.values[0]
    df.monthmin_num=b.values[0]

    c=get_date_max(data2)
    df.datemax=c.index.values[0]
    df.datemax_num=c.values[0]

    d=get_hour_max(data2)
    df.hour_prefer=d.index.values[0]
    df.all_month=get_all_month(data2)
    df.month_emotion=get_month_emotion(data2)
    df.T.to_json('./jsonresult/'+data2.authorId[0]+'.json')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        json = sys.argv[1]
        get_result(json)
    else:
        print 'json'

