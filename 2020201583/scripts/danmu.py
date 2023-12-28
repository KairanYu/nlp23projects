import re  # 正则表达式提取文本
import csv
import requests  # 爬虫发送请求
from bs4 import BeautifulSoup as BS  # 爬虫解析页面
import time
import pandas as pd  # 存入csv文件
import os
from snownlp import SnowNLP
from wordcloud import WordCloud
import jieba.analyse
from PIL import Image
import numpy as np
from pprint import pprint
# headers = {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTMsnowL, like Gecko)", }
# r1 = requests.get(
#     url='https://api.bilibili.com/x/player/pagelist?bvid='+"BV1TA411V77o", headers=headers)
# html1 = r1.json()
# cid = html1['data'][0]['cid']  # 获取视频对应的cid号
# print('该视频的cid是:', cid)
# danmu_url= 'http://comment.bilibili.com/{}.xml'.format(cid)  # 弹幕地址
# print('弹幕地址是：', danmu_url)
# r2 = requests.get(danmu_url)
# html2=r2.text.encode("raw-unicode-escape")
# soup = BS(html2, 'xml')
# danmu_list = soup.find_all('d')
# print('共爬取到{}条弹幕'.format(len(danmu_list)))
# video_url_list = []  # 视频地址
# danmu_url_list = []  # 弹幕地址
# time_list = []  # 弹幕时间
# text_list = []  # 弹幕内容
#
# v_url='https://api.bilibili.com/x/player/pagelist?bvid='+"BV1TA411V77o"
# v_result_file='弹幕'
# for d in danmu_list:
#       data_split = d['p'].split(',')  # 按逗号分隔
#       temp_time = time.localtime(int(data_split[4]))  # 转换时间格式
#       danmu_time = time.strftime("%Y-%m-%d %H:%M:%S", temp_time)
#       video_url_list.append(v_url)
#       danmu_url_list.append(danmu_url)
#       time_list.append(danmu_time)
#       text_list.append(d.text)
#       print('{}:{}'.format(danmu_time, d.text))
# df=pd.DataFrame()
# # df['视频地址']= video_url_list
# # df['弹幕地址']= danmu_url_list
# # df['弹幕时间']=time_list
# df['弹幕内容']=text_list
# if os.path.exists(v_result_file):
#         header=None
# else:
#         header=['弹幕内容']
# df.to_csv("danmu1")

#文字预实验
def sentiment_analyse(v_cmt_list):#利用SNOWNLP情感打分
    score_list = []  # 情感评分值
    tag_list = []  # 打标分类结果
    pos_count = 0  # 计数器-积极
    neg_count = 0  # 计数器-消极
    for comment in v_cmt_list:
        tag = ''
        sentiments_score = SnowNLP(comment).sentiments
        if sentiments_score < 0.3:
            tag = '消极'
            neg_count += 1
        else:
            tag = '积极'
            pos_count += 1
        score_list.append(sentiments_score)  # 得分值
        tag_list.append(tag)  # 判定结果
    print('积极评价占比：', round(pos_count / (pos_count + neg_count), 4))
    print('消极评价占比：', round(neg_count / (pos_count + neg_count), 4))
    df['情感得分'] = score_list
    df['分析结果'] = tag_list
    df.to_excel(r'C:\Users\AGreatHunger.LAPTOP-08QIMAJA\Desktop\2023\NLP\danmu\SNOW情感评分结果.xlsx')



def make_wordcloud(v_str, v_stopwords, v_outfile):

    print('开始生成词云图：{}'.format(v_outfile))
    try:
        stopwords = v_stopwords  # 停用词
        backgroud_Image = np.array(Image.open(r"C:\Users\AGreatHunger.LAPTOP-08QIMAJA\Desktop\2023\NLP\background.jpeg"))  # 读取背景图片
        wc = WordCloud(
            background_color="white",  # 背景颜色
            width=1500,  # 图宽
            height=1200,  # 图高
            max_words=1000,  # 最多字数
            # font_path='/System/Library/Fonts/SimHei.ttf',  # 字体文件路径，根据实际情况(Mac)替换
            # font_path="C:\Windows\Fonts\simhei.ttf",  # 字体文件路径，根据实际情况(Windows)替换
            stopwords=stopwords,  # 停用词
            mask=backgroud_Image,  # 背景图片
        )
        jieba_text = " ".join(jieba.lcut(v_str))  # jieba分词
        wc.generate_from_text(jieba_text)  # 生成词云图
        wc.to_file(v_outfile)  # 保存图片文件
        print('词云文件保存成功：{}'.format(v_outfile))
    except Exception as e:
        print('make_wordcloud except: {}'.format(str(e)))



if __name__=='__main__':
    print("1")
    df = pd.read_csv('danmu1') # 读取excel
    v_cmt_list = df['弹幕内容' ].values.tolist() # 评论内容列表
    print('length of v_cmt_list is:}'.format(len(v_cmt_list)))
    v_cmt_list = [str(i) for i in v_cmt_list] # 数据清洗-List所有元素转换成字符串
    v_cmt_str =  ''.join(str(i) for i in v_cmt_list) # 评论内容转换为字符串
    #1、情感分析打分
    sentiment_analyse(v_cmt_list=v_cmt_list)
    # 2、用iieba统计弹幕中的top10高频词
    keywords_top10 = jieba.analyse.extract_tags(v_cmt_str, withweight=True, topk=10)
    pprint(keywords_top10)
    make_wordcloud(v_cmt_str,
               ["的","啊","她","是","了","你","我","都","也","不","在","吧","说","就是","这","有"],# 停用词
               '弹幕_词云图.jpg')



