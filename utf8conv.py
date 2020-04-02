"""
author: Barış Şenyerli
Mail: baris.senyerli@ogr.sakarya.edu.tr
"""

import MySQLdb
host = "192.168.1.23"
passwd = "some_pass"
user = "barisx"
dbname = "supereleman_son"

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
cursor = db.cursor()
cursor.execute("SET sql_mode = ''") #0000-00-00 default değerli tarihlerin hatalarını atlarız ve bunu sadece 1 swefe
"""
Disabling the SQL mode temporarily for the current connection
Connect to MySQL server.

Run the following query:

mysql> SET sql_mode = '';

Disabling the SQL mode temporarily for the current connection
SET GLOBAL sql_mode = 'modes';
"""
cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci'" % dbname)

sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname

cursor.execute(sql)

results = cursor.fetchall()

cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci'" % dbname)

sql = "SELECT DISTINCT table_name,column_name FROM information_schema.columns WHERE table_schema = '%s' AND (data_type='blob' OR data_type='binary' OR data_type='mediumblob' OR data_type='tinyblob' OR data_type='longblob' OR data_type='varbinary')" % dbname

cursor.execute(sql)

blobs = cursor.fetchall()
print()

cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci'" % dbname)

sql = "SELECT DISTINCT table_name,column_name FROM information_schema.columns WHERE table_schema = '%s' AND data_type=('date')" % dbname

cursor.execute(sql)

dates = cursor.fetchall()

if(dates):
	for t,c in dates: #dates OK
		try:
			sql = "ALTER TABLE `%s` ALTER COLUMN `%s` DROP DEFAULT;" % (t,c)
			cursor.execute(sql)
			print(sql)
		except :
			print("[ERROR] = "+sql)
else:
	print("Tarih kolonu bulunamadı.")

if(blobs):
	for t,c in blobs:
		sql = "ALTER TABLE `%s` MODIFY COLUMN `%s` TEXT" % (t,c)
		print("blob"+sql)
		cursor.execute(sql)
else:
	print("İkilik kolonlar bulunamadı. ('VARBINARY','BLOB', etc..)")
if(results):
	for row in results:#"ALTER TABLE `%s` MODIFY columnname INTEGER;"
		sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
		cursor.execute(sql)	
else:
	print("Tablo isimleri çekilemedi, boş veya dosya bozuk.")

db.close()
