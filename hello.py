import psycopg2
print('hello world!')

try:
  con = psycopg2.connect(
    database = 'my_db',
    user = 'postgres',
    password ='1234',
    port = '5432',
    host = 'db'
  )
  print("[INFO] Подключение с БД установлено")
  cur = con.cursor()
  cur.execute('''CREATE TABLE STUDENT  
     (ADMISSION INT PRIMARY KEY NOT NULL,
     NAME TEXT NOT NULL,
     AGE INT NOT NULL,
     COURSE CHAR(50),
     DEPARTMENT CHAR(50));''')

  print("Table created successfully")
  con.commit()  
  con.close()
except:
  print("[INFO] Нет соединения с БД")
