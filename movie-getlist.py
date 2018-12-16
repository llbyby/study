# -*- coding: utf-8 -*-
import web
from urllib.request import urlopen
import json
import time

db = web.database(dbn='sqlite', db='dbs/MovieSite.db')

'''
movie_ids = []
print("开始从豆瓣拉前250")
for index in range(0,250,50):
#    print(index)
    response = urlopen('http://api.douban.com/v2/movie/top250?start=%d&count=50'%index)
    data = response.read()
    data_json = json.loads(data)
    movie250 = data_json['subjects']
    for movie in movie250:
        movie_ids.append(movie['id'])
#        print(movie['id'], movie['title'])
    time.sleep(3)
print("成功拉取", len(movie_ids))

def add_movie(data):
    movie = json.loads(data)
#    print(movie['title'])
    db.insert('movie',
            id = movie['id'],
            title = movie['title'],
            origin = movie['original_title'],
            url = movie['alt'],
            rating = movie['rating']['average'],
            image = movie['images']['large'],
            directors = ','.join([d['name'] for d in movie['directors']]),
            casts = ','.join([c['name'] for c in movie['casts']]),
            year = movie['year'],
            genres = ','.join(movie['genres']),
            countries = ','.join(movie['countries']),
            summary = movie['summary'],
    )

count = 1
for mid in movie_ids:
    print("写入", count, mid)
    response = urlopen('http://api.douban.com/v2/movie/subject/%s' % mid)
    data = response.read()
    add_movie(data)
    count += 1
    time.sleep(3)
'''
def get_pic(id,url):
    pic = urlopen(url).read()
    file_name = 'moviepic/%s.jpg'%id
    f = open(file_name,"wb")
    f.write(pic)
    f.close()

movies = db.select('movie')
count = 1
for movie in movies:
    print("抓图", count, movie.id)
    get_pic(movie.id,movie.image)
    count += 1
    time.sleep(2)