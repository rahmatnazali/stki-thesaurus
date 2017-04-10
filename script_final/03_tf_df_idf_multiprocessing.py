# -*- coding: utf-8 -*-
__author__ = 'rahmat, haqiqi'
# 16 December 2016 6:45 PM

import mysql.connector
import math
import time

def make_dict(data):
    a_dict = {}
    for i in data:
        if a_dict.has_key(i[2]):
            a_dict[i[2]] = [a_dict[i[2]][0] + i[3], a_dict[i[2]][1] + 1]
        else:
            a_dict[i[2]] = [i[3], 1]
    return a_dict

def compute_idf(ndoc, data):
    for i in data:
        data[i].append(math.log( float(ndoc[0]) / data[i][1], 10))
    return data

def compute_tfidf(data):
    for i in data:
        data[i].append( data[i][0] * data[i][2])
    return data

db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')
cursor = db.cursor()

cursor.execute("select * from terms")
output = cursor.fetchall()

cursor.execute("SELECT count(1) FROM `artikel`")
ndoc = cursor.fetchone()

a_dict = make_dict(output)
a_dict = compute_idf(ndoc, a_dict)
a_dict = compute_tfidf(a_dict)

print "Penghitungan tf df idf"

try:
    for j in sorted(a_dict, key=lambda key: (key)):
        sql1 = "insert into terms_distinct (term, tf, df, idf, tf_idf, id_skenario) values('"+j+"', "+str(a_dict[j][0])+", "+str(a_dict[j][1])+", "+ str(a_dict[j][2])+", "+str(a_dict[j][3])+", 1)"
        cursor.execute(sql1)
        print "menghitung", j
    db.commit()
    print "selesai."

except:
    db.rollback()
    print "gagal."
