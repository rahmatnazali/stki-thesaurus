# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 08:52:35 2016

@author: ilham
"""

import mysql.connector

db = mysql.connector.connect(host='10.151.33.33', port='3307', database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
cursor = db.cursor()
#string = "select id_co, term1, term2, tf, idf from cooccurence1"
string = "select min(id_co) from cooccurence1"
cursor.execute(string)
data2 = cursor.fetchall()

string = "select max(id_co) from cooccurence1"
cursor.execute(string)
data = cursor.fetchall()

#cluster_weight = 0.0
##atas = 0.0
i=data2[0]
ii=i[0]
j = data[0]
jj=j[0]
while ii < jj:
    print "proses pair ID: " + str(ii)
    cursor.execute("select term1, term2, tf, idf from cooccurence1 where id_co="+str(ii))
    data3 = cursor.fetchall()
    print "pair: " + data3[0][0] + " " + data3[0][1]
    
    cursor = db.cursor()
    string = "select idf from terms_distinct_sort where term = '" +data3[0][0]+ "'"
    cursor.execute(string)
    idf = cursor.fetchall()
    idf=idf[0][0]
#    
    cursor = db.cursor()
    string = "select weight_factor from terms_distinct_sort where term = '" +data3[0][1]+ "'"
    cursor.execute(string)
    weight_factor = cursor.fetchall()
    weight_factor=weight_factor[0][0]
#        
    atas = data3[0][2]*data3[0][3]
    cluster_weight = atas/idf*weight_factor
    print "cluster weight: " + str(cluster_weight) + "\n"
#
    cursor = db.cursor()
    cursor.execute("update cooccurence1 set cluster_weight = %s where id_co = %s", (cluster_weight, ii))
    db.commit()
#    
    ii=ii+1
#    
