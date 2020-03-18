# coding=UTF-8
import MySQLdb
from time import time
from flask import Blueprint,Flask,render_template,request,redirect,url_for,jsonify,session,flash
from werkzeug import secure_filename
from collections import Counter
import flask_excel as excel
import os
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import base64
import jieba
import math
import operator  
sss = Flask(__name__,static_folder='static',template_folder='templates')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#select substr(wb_content,locate('#',wb_content),locate('#',wb_content,locate('#',wb_content)+1)-locate('#',wb_content)) from user_weibo order by id desc limit 10;

def tfcalcul(word,text):
    seg = " ".join(jieba.cut(text))
    word_list = []
    word_list.append(seg.split(' '))
    countlist = []
    count = Counter(word_list[0])
    countlist.append(count)
    return count[word]/sum(count.values())

    
@sss.route('/')
def hello_world():
    return 'Hello World!'

@sss.route('/search',methods=['GET','POST']) 
def search():

    if request.method == 'GET':
        return render_template("result.html")
    if request.method == 'POST':
        if('go' in request.form): #搜关键词
            keyword = request.form.get('search') 
            # connect to db
            
            db = MySQLdb.connect(host='localhost', user='root', passwd='zndzt4328086', db='weibo') 
            cursor = db.cursor() 
	    #rank = (length(wb_username)-length(replace(wb_username,\'"+keyword+"\','')))/length(\'"+keyword+"\')+(length(wb_content)-length(replace(wb_content,\'"+keyword+"\','')))/length(\'"+keyword+"\')=关键词在用户名出现的次数+关键词在内容出现的次数       
            # verify user info
            #sql = "select id,wb_username,wb_content,wb_id from user_weibo where locate( %s,wb_content)>0 order by id desc limit 100"
#            exist = cursor.execute(sql,keyword)
            sql = "select (length(wb_username)-length(replace(wb_username,%s,'')))/length(%s)+(length(wb_content)-length(replace(wb_content,%s,'')))/length(%s),wb_username,wb_content,wb_id,hashtag from user_weibo where locate(%s,wb_content)>0 order by (length(wb_username)-length(replace(wb_username,%s,'')))/length(%s)+(length(wb_content)-length(replace(wb_content,%s,'')))/length(%s) desc limit 100" #抓取某个关键词出现的次数并且用这个次数排序
            val=(keyword,keyword,keyword,keyword,keyword,keyword,keyword,keyword,keyword)
            exist = cursor.execute(sql,val)

            data = cursor.fetchall()
            db.commit()
            cursor.close()
            db.close()
            posts = list()
            for i in range(len(data)):
                posts.append({
			'times':data[i][0],
                        'rank':tfcalcul(keyword,data[i][2]),
			'username':data[i][1],
			'content':data[i][2],
			'wbid':data[i][3],
                        'hashtag':data[i][4]
                })#把所有参数插入一个表，渲染进页面
#            return str(posts)
            posts_ranked = sorted(posts,key=operator.itemgetter('rank'),reverse=True)

            return render_template("result.html",posts = posts_ranked)
        elif('comment' in request.form): #搜评论
            keyword = request.form.get('search') 
            # connect to db
            
            db = MySQLdb.connect(host='localhost', user='root', passwd='zndzt4328086', db='weibo') 
            cursor = db.cursor() 
	    #rank = (length(wb_content)-length(replace(wb_content,\'"+keyword+"\','')))/length(\'"+keyword+"\')=关键词在内容出现的次数       
            # verify user info
            sql = "select (length(comment_content)-length(replace(comment_content,\'"+keyword+"\','')))/length(\'"+keyword+"\'),comment_username,comment_content,wb_id from comment where locate(\'"+keyword+"\',comment_content)>0 order by (length(comment_content)-length(replace(comment_content,\'"+keyword+"\','')))/length(\'"+keyword+"\') desc limit 100" #抓取某个关键词出现的次数并且用这个次数排序
            exist = cursor.execute(sql)
            data = cursor.fetchall()
            db.commit()
            cursor.close()
            db.close()
            posts = list()
            for i in range(len(data)):
                posts.append({
			'times':data[i][0],
                        'rank':tfcalcul(keyword,data[i][2]),
			'username':data[i][1],
			'content':data[i][2],
			'wbid':data[i][3]
                })#把所有参数插入一个表，渲染进页面
#            return str(posts)
            posts_ranked = sorted(posts,key=operator.itemgetter('rank'),reverse=True)
            return render_template("result.html",posts = posts_ranked)

        elif('hashtag' in request.form): #搜话题
            keyword = request.form.get('search') 
            # connect to db
            
            db = MySQLdb.connect(host='localhost', user='root', passwd='zndzt4328086', db='weibo') 
            cursor = db.cursor() 
	    #rank = (length(wb_content)-length(replace(wb_content,\'"+keyword+"\','')))/length(\'"+keyword+"\')=关键词在内容出现的次数       
            # verify user info
            sql = "select count(wb_username) as total,wb_username,wb_userid from user_weibo where locate(\'"+keyword+"\',wb_content)>0 group by wb_username,wb_userid order by total desc limit 100;"
            exist = cursor.execute(sql)
            data = cursor.fetchall()
            db.commit()
            cursor.close()
            db.close()
            posts = list()
            for i in range(len(data)):
                posts.append({
			'rank':data[i][0],
			'username':data[i][1],
			'userid':data[i][2]
                })#把所有参数插入一个表，渲染进页面
#            return str(posts)
            return render_template("hashtag.html",posts = posts)


if __name__ == '__main__':
    sss.run()
