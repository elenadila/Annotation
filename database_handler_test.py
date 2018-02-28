import pymysql
import Database_Handler
# Connection to the MySQL database

db = pymysql.connect(host="127.0.0.1",port = 3306,user = "root", passwd= '', db = 'laughter_analysis')
cursor = db.cursor()

cursor.execute("insert into feat_test (user_id) values (%s);", 'u002')
db.commit()
cursor.close()
db.close()


