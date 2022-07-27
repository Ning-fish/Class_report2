#!/usr/bin/env python
# coding: utf-8

# ## 爬文爬爬

# In[26]:


import requests
import re
import csv
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
import pandas as pd
url= 'https://www.ptt.cc/bbs/Japan_Travel/index.html'


def get_article_content(article_url):

    r = requests.get(article_url)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.select('span.article-meta-value')
    Japan_data = []

    author = results[0].text # 作者
    board = results[1].text  # 看版
    title = results[2].text  # 標題
    date = results[3].text   # 日期
        
    main_container = soup.find(id='main-container')  ## 查找所有html 元素 抓出內容
    all_text = main_container.text                   # 把所有文字都抓出來
    pre_text = all_text.split('--')[0]               # 把整個內容切割透過 "-- " 切割成2個陣列
    texts = pre_text.split('\n')                     # 把每段文字 根據 '\n' 切開 
    contents = texts[2:]                             # 如果你爬多篇你會發現
    content = '\n'.join(contents)                    # 內容
    
    
    
    return author,board,title,date,content
    
def get_all_href(url):
    authors = []
    boards = []
    titles = []
    dates = []
    contents = []
    df = pd.DataFrame()
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.select('div.title')
    for item in results:
        a_item = item.select_one('a')
        if a_item:
            try:
                author,board,title,date,content = get_article_content(article_url='https://www.ptt.cc'+a_item.get('href'))
            except:
                continue
            authors.append(author)
            boards.append(board)
            titles.append(title)
            dates.append(date)
            contents.append(content)
            
    
    df['authors'] = authors
    df['boards'] = boards
    df['titles'] = titles
    df['dates'] = dates
    df['contents'] = contents
    return df

            
    print('------------------ next page ------------------')
df_ = pd.DataFrame()
for page in tqdm(range(1,3)):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    btn = soup.select('div.btn-group > a')
    if btn:
        next_page_url = 'https://www.ptt.cc' + btn[3]['href']
        url = next_page_url
        print('page:', url)
        df_ = df_.append(get_all_href(url = url))
        


# In[27]:


# df_.to_csv('data_all.csv',index=False)


# In[49]:


import pandas as pd
dada = pd.read_csv('data_all.csv') 


# In[50]:


dada['contents']


# In[51]:


dada.reset_index()


# In[52]:


aa = dada.reset_index()
contents_all = aa['contents']
print(contents_all)


# In[53]:


contents_dates = aa['dates']+aa['contents']
print(contents_dates)


# In[54]:


month = [aa['dates'][i].split(' ')[1] for i in range(len(aa))]
aa['month'] = month


# In[94]:


aa


# In[56]:


aa.to_csv('data_all_month.csv',index=False)


# In[57]:


data_all_month = pd.read_csv('data_all_month.csv') 


# In[58]:


data_all_month


# In[213]:


names = ['北海道','青森','岩手','宮城','秋田','山形','福島','東京','神奈川','埼玉','千葉','茨城','栃木','群馬','山梨','新潟','長野','富山','石川','福井','愛知','岐阜','静岡','三重','大阪','兵庫','京都','滋賀','奈良','和歌山','鳥取','島根','岡山','広島','山口','徳島','香川','愛媛','高知','福岡','佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄']


# In[177]:


Spring = ['Mar','Apr','May']
Summer = ['Jun','Jul','Aug']
Fall = ['Sep','Oct','Nov']
Winter = ['Dec','Jan','Feb']
Spring_data = data_all_month[data_all_month['month'].isin(Spring)]['contents']
Summer_data = data_all_month[data_all_month['month'].isin(Summer)]['contents']
Fall_data = data_all_month[data_all_month['month'].isin(Fall)]['contents']
Winter_data = data_all_month[data_all_month['month'].isin(Winter)]['contents']


# In[144]:


def season(datas):
    dic = {}
    for name in names:
        tmp = 0
        for data in datas:
            count = str(data).count(name)
            tmp += count
        dic[name] = tmp
    return dic


# In[232]:


season(Spring_data)


# In[148]:


dic_Spring = season(Spring_data)
dic_Summer = season(Summer_data)
dic_Fall = season(Fall_data)
dic_Winter = season(Winter_data)


# In[149]:


import json
with open('Spring_cnt.json', 'w', encoding='utf-8') as f:
    json.dump(dic_Spring, f)
with open('Summer_cnt.json', 'w', encoding='utf-8') as f:
    json.dump(dic_Summer, f)
with open('Fall_cnt.json', 'w', encoding='utf-8') as f:
    json.dump(dic_Fall, f)
with open('Winter_cnt.json', 'w', encoding='utf-8') as f:
    json.dump(dic_Winter, f)


# In[150]:


f = open('Spring_cnt.json', 'r', encoding='utf-8')
Spring_cnt = json.load(f)
f = open('Summer_cnt.json', 'r', encoding='utf-8')
Summer_cnt = json.load(f)
f = open('Fall_cnt.json', 'r', encoding='utf-8')
Fall_cnt = json.load(f)
f = open('Winter_cnt.json', 'r', encoding='utf-8')
Winter_cnt = json.load(f)


# ## 春夏秋冬畫圖 (刪除 東京 大阪 京都)

# In[194]:


for i in range(len(names)):
    print(i,names[i])


# In[214]:


names_new = names
del names_new[7], names_new[23], names_new[24]
print(names_new)


# In[215]:


def season_new(datas):
    dic = {}
    for name in names_new:
        tmp = 0
        for data in datas:
            count = str(data).count(name)
            tmp += count
        dic[name] = tmp
    return dic


# In[218]:


dic_Spring_new = season_new(Spring_data)
dic_Spring_new


# In[222]:


import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Spring_new.keys())
count = list(dic_Spring_new.values())
my_colors = 'mistyrose','rosybrown','lightcoral','indianred'
plt.title('春天_日本熱門地區_(刪除東京、大阪、京都)',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_spring_new.png')


# In[219]:


dic_Summer_new = season_new(Summer_data)
dic_Summer_new


# In[227]:


plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Summer_new.keys())
count = list(dic_Summer_new.values())
my_colors = 'powderblue','paleturquoise','turquoise','c'
plt.title('春天_日本熱門地區_(刪除東京、大阪、京都)',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_summer_new.png')


# In[228]:


dic_Fall_new = season_new(Fall_data)
dic_Fall_new


# In[229]:


plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Fall_new.keys())
count = list(dic_Fall_new.values())
my_colors = 'bisque','wheat','tan','goldenrod','darkgoldenrod'
plt.title('秋天_日本熱門地區_(刪除東京、大阪、京都)',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_fall_new.png')


# In[230]:


dic_Winter_new = season_new(Winter_data)
dic_Winter_new


# In[231]:


plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Winter_new.keys())
count = list(dic_Winter_new.values())
my_colors = 'lightsteelblue','cornflowerblue','royalblue','midnightblue'
plt.title('冬天_日本熱門地區_(刪除東京、大阪、京都)',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_winter_new.png')


# ## 春夏秋冬_日本全地區 bar

# In[226]:


import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Spring.keys())
count = list(dic_Spring.values())
my_colors = 'mistyrose','rosybrown','lightcoral','indianred'
plt.title('春天_日本熱門地區',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_spring.png')


# In[162]:


plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Summer.keys())
count = list(dic_Summer.values())
my_colors = 'powderblue','paleturquoise','turquoise','c'
plt.title('夏天_日本熱門地區',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_summer.png')


# In[163]:


plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Fall.keys())
count = list(dic_Fall.values())
my_colors = 'bisque','wheat','tan','goldenrod','darkgoldenrod'
plt.title('秋天_日本熱門地區',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_fall.png')


# In[164]:


plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(dic_Winter.keys())
count = list(dic_Winter.values())
my_colors = 'lightsteelblue','cornflowerblue','royalblue','midnightblue'
plt.title('冬天_日本熱門地區',fontsize = 25) 
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_winter.png')


# ## 日本全地區次數

# In[234]:


import json
f=open('Japan_cnt.json', 'r', encoding='utf-8')
data=json.load(f)
print(data)


# In[253]:


import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Noto Serif CJK TC']
plt.figure(figsize=(30,10))
name = list(data.keys())
count = list(data.values())
my_colors = '#FFE1AB','#FFCF78','#FFBD45','#FFAC12','#E69500'
plt.title('日本熱門地區榜',fontsize = 25)
plt.bar(name, count, color = my_colors)
plt.xticks(fontsize = 20, rotation = 90)
plt.yticks(fontsize = 20)
plt.savefig('area_bar.png')


# ## 日本全地區次數繪製於地圖

# In[236]:


dic2 = dict(sorted(data.items(), key=lambda item: item[1]))
print(dic2)


# In[237]:


from pylab import *
co = []
cmap = cm.get_cmap('Wistia',50)    # PiYG

for i in range(cmap.N):
    rgba = cmap(i)
    # rgb2hex accepts rgb or rgba
    co.append(matplotlib.colors.rgb2hex(rgba))


# In[238]:


dic3 = {k:c for k,c in zip(dic2.keys(),co)}
print(dic3)


# In[239]:


import matplotlib.pyplot as plt
from japanmap import picture, get_data, pref_map
# pct = picture({'大阪': 'yellow'})  # numpy.ndarray
pct = picture(dic3)  # same to above
plt.figure(figsize=(20,20),dpi=200)
plt.imshow(pct)  # show graphics
plt.title('日本熱門地區分布圖',fontsize = 25)
plt.savefig('map.png')  # save to PNG file
svg = pref_map(range(1,48), qpqo=get_data())  # IPython.display.SVG
# print(svg.data)  # SVG source


# ## 結巴進行中

# In[639]:


import jieba
import re

# 停用詞
# 創建停用詞列表
# def get_stopwords_list():
#     stopwords = [line.strip() for line in open('stopwords.txt',encoding='UTF-8').readlines()]
#     return stopwords


def seg_depart(sentence):
    # 文章進行中文分詞
    sentence_depart = jieba.lcut(sentence.strip())
    return sentence_depart

def regex_change(line):
    # 前缀的正则
    username_regex = re.compile(r"^\d+::")      
    # 剔除URL
    url_regex = re.compile(r"""
        (https?://)?
        ([a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)*
        (/[a-zA-Z0-9]+)*
    """, re.VERBOSE|re.IGNORECASE)

    decimal_regex = re.compile(r"[^a-zA-Z]\d+") # 剔除所有数字
    space_regex = re.compile(r"\s+")            # 剔除空格
    space_jpg = re.compile(r"(.jpg)")           # 剔除.jpg
    space_XD = re.compile(r"(XD)")              # 剔除XD
    


    line = username_regex.sub(r"", line)
    line = url_regex.sub(r"", line)
    line = decimal_regex.sub(r"", line)
    line = space_regex.sub(r"", line)
    line = space_jpg.sub(r"", line)
    line = space_XD.sub(r"", line)


    return line


# 去除停用词
def move_stopwords(sentence_list, stopwords_list):
    # 去停用词
    out_list = []
    for word in sentence_list:
        if word not in stopwords_list:
            if not regex_change(word):
                continue
            if word != '\t':
                out_list.append(word)
    return out_list


# In[640]:


import jieba.analyse

# print('日本地區:北海道,青森,岩手,宮城,秋田,山形,福島,東京,神奈川,埼玉,千葉,茨城,栃木,群馬,山梨,新潟,長野,富山,石川,福井,愛知,岐阜,静岡,三重,大阪,兵庫,京都,滋賀,奈良,和歌山,鳥取,島根,岡山,広島,山口,徳島,香川,愛媛,高知,福岡,佐賀,長崎,熊本,大分,宮崎,鹿児島,沖縄')
input_area = input('輸入地區名: ')
c = 0
qq = []
for text in contents_all:
    if str(text).find(input_area) != -1:
        c += 1
        qq.append(text)

for i in  tqdm(range(len(qq))):
    cc_stop = regex_change(qq[i])
    tf_idf = jieba.analyse.extract_tags(cc_stop, topK=5, withWeight=True, allowPOS=())
    rel = tf_idf[0]
    if rel[1] >= 0.6:
        print(rel)


# In[585]:


# print('日本地區:北海道,青森,岩手,宮城,秋田,山形,福島,東京,神奈川,埼玉,千葉,茨城,栃木,群馬,山梨,新潟,長野,富山,石川,福井,愛知,岐阜,静岡,三重,大阪,兵庫,京都,滋賀,奈良,和歌山,鳥取,島根,岡山,広島,山口,徳島,香川,愛媛,高知,福岡,佐賀,長崎,熊本,大分,宮崎,鹿児島,沖縄')

input_area = input('輸入地區名: ')
c = 0
qq = []
for text in contents_all:
    if str(text).find(input_area) != -1:
        c += 1
        qq.append(text)
#         print(text)


# In[592]:


import jieba.analyse

for i in range(len(qq)):
    cc_stop = regex_change(qq[i])
    tf_idf = jieba.analyse.extract_tags(cc_stop, topK=5, withWeight=True, allowPOS=())
    rel = tf_idf[0][1]
    na = tf_idf[0][0]
#     print(na)
    if na == na:
        
    if rel >= 0.5:
        print(tf_idf[0])
#     print(tf_idf[0][1])

