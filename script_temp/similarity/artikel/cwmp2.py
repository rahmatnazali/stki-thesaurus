#running speed : 300-350 pair/menit per proses. 3000-3500 pair/menit utk seluruh proses.

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 16:17:11 2016

@author: ilham
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 08:52:35 2016

@author: ilham
"""

import mysql.connector
import sys
from multiprocessing import Process

def ambil_data():
    db = mysql.connector.connect(host='10.151.33.33', port='3307', database='stki',user='rahmat',password='rahmat')
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    string = "select id_co, term1, term2, tf, idf from cooccurence"
    cursor.execute(string)
    data2 = cursor.fetchall()
    
    print "ambil data selesai, memulai hitung cluster weight"
    
    count = len(data2)/10
    bawah = 0
    maxx = len(data2)-1
    jobs = []
    for i in range(10):
        atas = bawah+count
        print "proses data dari " + str(bawah) + " sampai " + str(atas)

        if atas > maxx:
            atas = maxx
        
        p = Process(target=cluster_weight, args=(i, data2[bawah:atas], ))
        jobs.append(p)
        p.start()
        bawah = atas
                
def cluster_weight(ii, data):
    db = mysql.connector.connect(host='10.151.33.33', port='3307', database='stki',user='rahmat',password='rahmat')    
    #la = open('query ke'+str(ii)+'.txt', 'w')
    for i in data:             
        print "proses ID ke " + str(i[0])
        #print "pair kata: " +i[1]+ " dan " +i[2]+ "\n"
        
        cursor = db.cursor()
        string = "select tf, idf from terms_distinct where term = '" +i[1]+ "'"
        cursor.execute(string)
        idf = cursor.fetchall()
        tf=idf[0][0]
        idf=idf[0][1]

        cursor = db.cursor()
        string = "select weight_factor from terms_distinct where term = '" +i[2]+ "'"
        cursor.execute(string)
        weight_factor = cursor.fetchall()
        weight_factor=weight_factor[0][0]

        cursor = db.cursor()
        string = "select tf, idf from terms_distinct where term = '" +i[2]+ "'"
        cursor.execute(string)
        idf2 = cursor.fetchall()
        tf2=idf2[0][0]
        idf2=idf2[0][1]

        cursor = db.cursor()
        string = "select weight_factor from terms_distinct where term = '" +i[1]+ "'"
        cursor.execute(string)
        weight_factor2 = cursor.fetchall()
        weight_factor2=weight_factor2[0][0]

        atas = i[3]*i[4]
        cluster_weight = atas/tf*idf*weight_factor
        cluster_weight_2 = atas/tf2*idf2*weight_factor2

        cursor = db.cursor()
        #string = "update cooccurence set cluster_weight = "+str(cluster_weight)+" where id_co = "+str(id_commit)
        #la.write(string)
        cursor.execute("update cooccurence set cluster_weight = %s, cluster_weight_2 = %s where id_co = %s", (cluster_weight, cluster_weight_2, i[0]))
        db.commit()
    #db.commit()


if __name__ == '__main__':
    print "ambil data dari db..."
        
    ambil_data()
