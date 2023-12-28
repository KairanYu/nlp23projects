import csv
import re  # 正则表达式提取文本
import requests
from bs4 import BeautifulSoup as BS
import os
import time
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('TkAgg')


from matplotlib import rcParams

import zhipuai
ans_list=[]
def askai(request):
    zhipuai.api_key = "77f5ec4b4d92d378c48a0b316e42b4ef.Tolo03TgdQ6YEUK7"

    response = zhipuai.model_api.invoke(
        model="chatglm_turbo",
        prompt=[{"role": "user", "content": request}],
        top_p=0.7,
        temperature=0.9,
    )
    dict1=response['data']
    dict2=dict1['choices']
    content1=dict2[0]
    content=content1["content"]
    return content
base='请对下面的一段话进行情感倾向分析，如果是积极你就回复1，如果是消极你就回复0'
f = open(r"C:\Users\AGreatHunger.LAPTOP-08QIMAJA\Desktop\2020201583\data\danmu\danmu2",encoding='utf-8')
for line in f.readlines():
    if line!=' ':
        ans=askai(base+line)
        print(ans)
        ans_list.append(ans)
df=pd.DataFrame()
df['情感分析']=ans_list
df.to_excel(r'C:\Users\AGreatHunger.LAPTOP-08QIMAJA\Desktop\2023\NLP\danmu\LLM情感评分结果.xlsx')
###77f5ec4b4d92d378c48a0b316e42b4ef.Tolo03TgdQ6YEUK7







