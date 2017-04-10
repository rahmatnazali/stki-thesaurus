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
import datetime
import sys
from multiprocessing import Process

def ambil_data():
    db = mysql.connector.connect(host='10.151.33.33', port='3307', database='stki',user='rahmat',password='rahmat')
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    string = "select id_co, term1, term2, tf, idf from cooccurence"
    cursor.execute(string)
    data2 = cursor.fetchall()
    #print len(data2)
    string = "select term, tf, idf, weight_factor from terms_distinct"
    cursor.execute(string)
    terms_raw = cursor.fetchall()
    
    terms = {x[0]:[x[1],x[2], x[3]] for x in terms_raw}
    #print terms['aba']

    print "ambil data selesai, memulai hitung cluster weight", str(datetime.datetime.now())
    
    count = len(data2)/60
    bawah = 0
    maxx = len(data2)
    jobs = []
    for i in range(60):
        atas = bawah+count
        #print "proses data dari " + str(bawah) + " sampai " + str(atas), str(datetime.datetime.now())

        if atas > maxx:
            atas = maxx
        #print len(data2[bawah:atas])
        p = Process(target=cluster_weight, args=(i, bawah, data2[bawah:atas],terms, ))
        jobs.append(p)
        p.start()
        bawah = atas
                
def cluster_weight(ii, bawah, data, terms):
   
    db = mysql.connector.connect(host='10.151.33.33', port='3307', database='stki',user='rahmat',password='rahmat')    
    #la = open('query ke'+str(ii)+'.txt', 'w')
    print "proses ID ke " + str(ii), str(datetime.datetime.now())
    cursor = db.cursor()
    rows = []
    #print len(data)
    for i in data:             
        
        #print "pair kata: " +i[1]+ " dan " +i[2]+ "\n"
        
        
        #string = "select term, tf, idf, weight_factor from terms_distinct where term = '" +i[1]+ "' or term = '"+i[2]+"'"
        #cursor.execute(string)
        #idf = cursor.fetchall()
        d1 = terms[i[1]]
        d2 = terms[i[2]]
        tf = d1[0]
        idf = d1[1]
        weight_factor2 = d1[2]

        tf2 = d2[0]
        idf2 = d2[1]
        weight_factor = d2[2]
        """
        if idf[0][0]==i[1]:
            [1]idf[0][1]
            weight_factor2=idf[0][3]        
            

            tf2=idf[1][1]
            weight_factor=idf[1][3]
            idf2=idf[1][2]
            idf=idf[0][2]
        else:
            tf=idf[1][1]
            weight_factor2=idf[1][3]        
            

            tf2=idf[0][1]
            weight_factor=idf[0][3]
            idf2=idf[0][2]
            idf=idf[1][2]
        """

        atas = i[3]*i[4]
        cluster_weight = atas/tf*idf*weight_factor
        cluster_weight_2 = atas/tf2*idf2*weight_factor2

        cursor = db.cursor()
        #string = "update cooccurence set cluster_weight = "+str(cluster_weight)+" where id_co = "+str(i[0])
        #la.write(string)
        rows = rows + [[str(cluster_weight), str(cluster_weight_2), str(i[0])]]
    print "writing" + str(ii), str(datetime.datetime.now())
    cursor.executemany("update cooccurence set cluster_weight = %s, cluster_weight_2 = %s where id_co = %s", rows)
    db.commit()
    
    print "done" + str(ii), str(datetime.datetime.now())
    #db.commit()
    

if __name__ == '__main__':
    print "ambil data dari db...", str(datetime.datetime.now())
        
    ambil_data()
