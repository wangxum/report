#!/usr/bin/python
# coding=utf-8
from pandas import DataFrame, read_csv, Series
import datetime as datetime
import pandas as pd
import os
import re

def parseTime(t):
    string_ = str(t)
    try:
        return datetime.date(int(string_[:4]), int(string_[4:6]), int(string_[6:]))
    except:
        return ""

fold = "./data"

#计算每天仓位
index = []
datas = []
pattern = re.compile(r"^(\d{8})-4\.csv")
for root, dirs,  files in os.walk(fold):
    for filename in files:
        match = pattern.match( filename)
        if match:
            fileDate = match.group(1)
            path = os.path.join(fold, filename)
            data = pd.read_csv(path,delimiter=",",  usecols=[6,7],nrows=1)
            index.append( parseTime( fileDate ) )
            oneDay = {}
            for key in data.keys():
                oneDay.update({ key: data[key][0]})
            datas.append( oneDay )
df = DataFrame( datas, index= index )
print( df )