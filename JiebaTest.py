#encoding=utf-8
import jieba
# from scipy.misc import imread
import  jieba.posseg as pseg
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PooledDB import Mysql
from collections import Counter
import matplotlib.pyplot as plt
mysql = Mysql()
result = mysql.getAll("""select * from chat_record where msg_type='TEXT' and msg_time>='2017-11-19 00:00:00' order by id desc""")
allname = mysql.getAll("""select nick_name from chat_record    group by nick_name""")

str=""

aa=[]
for i in result:
    content=i[4]
    print "before"+content
    for n in allname:
        if content.find(n[0])>=0:
            print "find"
            content=content.replace(n[0]," ")
            getlist=list(pseg.cut(content));
            for gl in getlist:
                if gl.word.__len__()>=2:
                    aa.append(gl.word);
            # aa+=
    # str+=" ".join(jieba.cut(content))
    # print "after"+content
  # d = path.dirname(__file__)
  # back_coloring = imread(path.join(d, "img/love.jpg"))
#
# for i in aa:
#     print i
d = Counter(aa)
print d.most_common(100)
print str
backgroud_Image = plt.imread('img/love.jpg')
wc = WordCloud(background_color='white',  # 设置背景颜色
                 mask=backgroud_Image,  # 设置背景图片
                 max_words=20,  # 设置最大现实的字数
                 stopwords=STOPWORDS,  # 设置停用词
                 font_path='C:\Users\Ray\Documents\tran\msyh.ttc',  # 设置字体格式，如不设置显示不了中文
                 max_font_size=100,  # 设置字体最大值
                 random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                 )
wc.generate_from_frequencies(d)
image_colors = ImageColorGenerator(backgroud_Image)
wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()
  #                               (groupName, InviteUser))