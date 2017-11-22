#encoding=utf-8
import jieba
# from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PooledDB import Mysql
import matplotlib.pyplot as plt

# str="张双磊  张双磊 黄伟玲 张双磊 张双磊 黄伟玲 黄伟玲 自己写 爱迪生 爱迪生  爱迪生  爱迪生 爱迪生 爱迪生 爱迪生"
aa=[u"我",u"你",u"我们",u"["]
for i in aa:
    if i.__len__()<2:
        aa.remove(i)
print aa
