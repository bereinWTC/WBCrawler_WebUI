import MySQLdb
db = MySQLdb.connect(host='localhost', user='root', passwd='zndzt4328086', db='weibo') 
cursor = db.cursor() 
sql="select substr(wb_content,locate('#',wb_content)+1,locate('#',wb_content,locate('#',wb_content)+1)-locate('#',wb_content)-1),id from user_weibo"
exist = cursor.execute(sql)
data = cursor.fetchall()
for i in range(len(data)):
	sql2 = "update user_weibo set hashtag = %s where id=%s"
	exist2 = cursor.execute(sql2,(data[i][0],data[i][1]))
db.commit()
cursor.close()
db.close()

