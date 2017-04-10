# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 15:13:33 2016

@author: ilham
"""
import mysql.connector

db = mysql.connector.connect(host='10.151.33.33', port='3307', database='stki',user='rahmat',password='rahmat')

teks=raw_input()

# prepare a cursor object using cursor() method
cursor = db.cursor()
string = "select term2, cluster_weight as cw from cooccurence12 where term1='"+teks+"' union select term1, cluster_weight_2 as cw from cooccurence12 where term2='"+teks+"' ORDER BY cw desc limit 5"
cursor.execute(string)
data = cursor.fetchall()

for i in data:
    print i
