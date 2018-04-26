#!/usr/bin/python
# coding=utf-8
from pandas import DataFrame, read_csv, Series
import datetime as datetime
import pandas as pd
import os
import re
######################################################################################
#取出每天融资帐户的净资和持仓量
#按年化收益最低20%最高目标40%，调整杠杆
#当到达最低20%时，开始逐步减杠杆
#当到达最高40%时，去掉杠杆
#每周一次计算
#起始位置20180305
######################################################################################
def parseTime(t):
    string_ = str(t)
    try:
        return datetime.date(int(string_[:4]), int(string_[4:6]), int(string_[6:]))
    except:
        return ""

fold = "./data"

transaction = {
   "20180329" : 25000,
   "20180330" : 25000,
   "20180402" : 25000,
   "20180403" : 25000,
   "20180404" : 25000,
   "20180411" : 25000
}

index = []
datas = []
pattern = re.compile(r"^(\d{8})-3\.csv")
for root, dirs,  files in os.walk(fold):
    for filename in files:
        match = pattern.match( filename)
        if match:
            fileDate = match.group(1)
            path = os.path.join(fold, filename)
            data = pd.read_csv(path,delimiter=",", header=None, usecols=[0,1])
            if(  fileDate in transaction ):
                data[1][3] = float(data[1][3])-transaction[fileDate]
            index.append( parseTime( fileDate ) )
            data[1].index = data[0]
            datas.append( data[1].to_dict() )

df = DataFrame( datas, index= index )

df = df.ix[:,["总负债",'净资产']]
df = df.transform(lambda x: x.map(float))

print( df )
 #df['总负债'].map( float )
# df = df['净资产']
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties 
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax = df.plot(ax=ax,style="k--")
# plt.savefig("output.svg")
legend = ax.get_legend()
for text in legend.texts:
    text.set_font_properties(font)
plt.show()