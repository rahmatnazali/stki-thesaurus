# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 12:14:25 2016

@author: ilham
"""

# import MySQLdb
import mysql.connector
import math

db = mysql.connector.connect(host='10.151.33.33',database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
cursor = db.cursor()
string = "select id, idf from terms_distinct"
cursor.execute(string)
data = cursor.fetchall()

cursor = db.cursor()
string = "select count(*) from artikel"
cursor.execute(string)
data2 = cursor.fetchall()
lenarti = data2[0]
lenartikel = lenarti[0]

weight_factor = 0.0
for i in data:
    weight_f = i[1]
    weight_factor = weight_f/math.log(lenartikel)
    print i
    cursor = db.cursor()
    cursor.execute("update terms_distinct set weight_factor = %s where id = %s", (weight_factor, i[0]))
    db.commit()
