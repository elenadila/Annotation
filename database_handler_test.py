import pymysql
import Database_Handler
# Connection to the MySQL database

db = pymysql.connect(host="uc-edu.mobile.usilu.net",port = 22,user = "dilascio", password= 'selOLujAkutOs', db = 'experiment')
cursor = db.cursor()

#cursor.execute("insert into registration (user_id) values (%s);", 'u002')
db.commit()
cursor.close()
db.close()


