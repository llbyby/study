# -*- coding: utf-8 -*-
from urllib.request import urlopen
import json
from weather_city import city

citycode = None
while citycode == None:
#    cityname=input('城市：')
    cityname='香港'
    citycode=city.get(cityname)
    if citycode==None:
        print('没有这个城市')
url=('http://www.weather.com.cn/data/cityinfo/%s.html'%citycode)
try:
    content=urlopen(url).read().decode('utf-8')
except:
    print('查询失败')
#print(content)
data=json.loads(content)
#print(data)
result=data['weatherinfo']
#print(result)
str_temp=cityname+' '+\
         ('%s %s~%s %s')%(result['weather'],result['temp1'],result['temp2'],result['ptime'])
print(str_temp)