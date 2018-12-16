# -*- coding: utf-8 -*-
import web

urls = (
    '/', 'index',
    '/movie/(\d+)', 'movie',
    '/moviepic/(.*.jpg)', 'moviepic',
    '/cast/(.*)', 'cast',
)

##webpy自带的server貌似不能自动加载静态资源，需要手工读取文件来加载到页面显示
class moviepic:
    def GET(self, file):
        f = open('static/moviepic/'+file, 'rb')
        ##rb表示以二进制加载
        return f.read()

render = web.template.render('templates/')

db = web.database(dbn='sqlite', db='dbs/MovieSite.db')

class index:
    def GET(self):
        movies = db.select('movie')
        count = db.query('select count(*) as count from movie')[0]['count']
        return render.index(movies, count, None)
    def POST(self):
        data = web.input()
        condition = r'title like "%' + data.title + r'%"'
        movies = db.select('movie', where=condition)
        count = db.query('select count(*) as count from movie where '+condition)[0]['count']
        return render.index(movies, count, data.title)

class movie:
    def GET(self, movie_id):
        condition = 'id="' + movie_id + '"'
        movie = db.select('movie', where=condition)[0]
        return render.movie(movie)

class cast:
    def GET(self, cast_name):
        condition = r'casts like "%' + cast_name.encode('iso-8859-1').decode('UTF-8') + r'%"'
        ##castname需要转码
        movies = db.select('movie', where=condition)
        count = db.query('select count(*) as count from movie where ' + condition)[0]['count']
        return render.index(movies, count, cast_name.encode('iso-8859-1').decode('UTF-8'))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()