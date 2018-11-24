# -*- coding: utf-8 -*-
from urllib.request import urlopen

url1 = 'http://m.weather.com.cn/data3/city.xml'
content1 = urlopen(url1).read().decode('UTF-8')
print('获取省份列表成功')
provinces = content1.split(',')
result = '# -*- coding: GBK -*-\ncity = {\n'
url = 'http://m.weather.com.cn/data3/city%s.xml'
count=len(provinces)
print('一共%d个省份'%count)
for p in provinces:
    print('正处理第%d个省份'%count)
    count -= 1
    p_code = p.split('|')[0]
    p_name = p.split('|')[1]
    url2 = url % p_code
#    print('--正在获取%s省的地市列表'%p_name)
    try:
        content2 = urlopen(url2).read().decode('UTF-8')
    except:
        print('!!获取%s省%s的地市列表出错'%(p_name,p_code))
    cities = content2.split(',')
    for c in cities:
        c_code = c.split('|')[0]
        c_name = c.split('|')[1]
        url3 = url % c_code
#        print('----正在获取%s市的县区列表' % c_name)
        try:
            content3 = urlopen(url3).read().decode('UTF-8')
        except:
            print('!!获取%s市%s的县区列表出错'%(c_name,c_code))
        districts = content3.split(',')
        for d in districts:
            d_pair = d.split('|')
            d_code = d_pair[0]
            name = d_pair[1]
            url4 = url % d_code
#            print('------正在获取%s县区的代码' % name)
            try:
                content4 = urlopen(url4).read().decode('UTF-8')
            except:
                print('!!获取%s县区%s的代码出错'%(name,d_code))
            code = content4.split('|')[1]
            line = "    '%s': '%s',\n" % (name, code)
            result += line
result += '}'
f = open('weather_city.py', 'w')
f.write(result)
f.close()
print('写入weather_city.py成功')