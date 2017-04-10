# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 11:25:12 2016

@author: rizkyhaqiqi
"""

from mysql.connector import MySQLConnection, Error
import math
import io
import os 
import pickle
import datetime
from collections import Counter
from multiprocessing import Process

def co_ocu(num, c, artikel):        #artikel: daftar artikel
    print "running ", num
    f = open("co_ocu/daftar.pkl", 'rb')
    daftar = pickle.load(f)         #daftar: all terms at doc
    f.close()
    cooc=set([])
    c1=1;
    kam = {}    #kam : tf dict. storing tf value
    kamdf= {}   #kam : df dict. storing df value
    #nn = open("log/"+str(num)+".txt", "a");

    for i in artikel:
        #cursor.execute("SELECT * FROM terms where id_artikel="+str(i[0]))
        #gen=cursor.fetchall()

        gen = (x for x in daftar if x[1]==i[0])     #gen : get the terms of artikel
        print "Dok-"+ str(c)+"\n\n"
        c=c+1
        for j in gen:
            #cursor.execute("SELECT * FROM terms where id_term > "+str(j[0])+" and id_artikel="+str(i[0]))
            #gen1=cursor.fetchall()

            gen1 = (x for x in daftar if x[0]>j[0] and x[1]==i[0])  # gen1: get pre pariring terms
            for k in gen1:
                
                args=(j[2], k[2])   #pair
                df = 0
                tf = min(j[3], k[3])    #tf of pair is lowest tf one of term
                if tf > 0:
                    df = 1
                    
                if not args in kam: 
                    kam[args]=1         
                else:
                    kam[args]+=tf
                
                if not args in kamdf:
                    kamdf[args]=df
                else:
                    kamdf[args]+=df
                
                cooc.add(args)
                #la.write(str(c1)+" : "+str(args)+"\n")
                #c1=c1+1;
                
    with open('co_ocu/tf/'+ str(num) + '.pkl', 'wb') as f:
        pickle.dump(kam, f, pickle.HIGHEST_PROTOCOL)    #dumping variable to file
    with open('co_ocu/df/'+ str(num) + '.pkl', 'wb') as f:
        pickle.dump(kamdf, f, pickle.HIGHEST_PROTOCOL)
    with open('co_ocu/cooc/'+ str(num) + '.pkl', 'wb') as f:
        pickle.dump(cooc, f, pickle.HIGHEST_PROTOCOL)
    
def commiter(i, bawah, cooc, lenartikel):
    conn = MySQLConnection(host='10.151.33.33', port="3307", database='stki', user='rahmat', password='rahmat')
    cursor = conn.cursor()

    f = open("co_ocu/tf.pkl", 'rb')  
    kam = pickle.load(f)        #get the dumped dict from post()
    f = open("co_ocu/df.pkl", 'rb')
    kamdf = pickle.load(f)

    print "process", str(i), str(datetime.datetime.now())
    rows = []
    start = bawah
    for i in cooc:
        start = start +1
        if(kamdf[i]==0):    #idf-ing
            idf = 0
        else:        
            idf = (math.log10(lenartikel)/kamdf[i])    
        rows = rows+[[str(start), str(i[0]), str(i[1]), str(kam[i]), str(idf)]] #for inserting

    print str(i), "write", str(datetime.datetime.now())
    que="INSERT INTO cooccurence VALUES(%s, %s, %s, %s, %s, 0,0);"
    cursor.executemany(que, rows)
    conn.commit()

    print str(i), "finish", str(datetime.datetime.now())
    
def post():

    print "ready", str(datetime.datetime.now())
    df={}
    tf={}
    cooc=set([])    
    df=Counter(df)
    tf=Counter(tf)
    
    print "load tf", str(datetime.datetime.now())
    for filename in os.listdir('co_ocu/tf/'):
        f = open("co_ocu/tf/"+filename, 'rb')
        tmp = pickle.load(f)
        tf=tf+Counter(tmp)      #join tf dict from multiprocess

    print "load df", str(datetime.datetime.now())
    for filename in os.listdir('co_ocu/df/'):
        f = open("co_ocu/df/"+filename, 'rb')
        tmp = pickle.load(f)
        df=df+Counter(tmp)      #join df dict from multiprocess

    print "cooc", str(datetime.datetime.now())
    for filename in os.listdir('co_ocu/cooc/'):
        f = open("co_ocu/cooc/"+filename, 'rb')
        tmp = pickle.load(f)
        cooc=cooc.union(tmp)    #join pair from multiprocess
    f.close()   
    
    kam=dict(tf)
    kamdf=dict(df)
    with open('co_ocu/tf.pkl', 'wb') as f:
        pickle.dump(kam, f, pickle.HIGHEST_PROTOCOL)    #dumping joined tf, for commiter
    with open('co_ocu/df.pkl', 'wb') as f:
        pickle.dump(kamdf, f, pickle.HIGHEST_PROTOCOL)  #dumping joined df, for commiter


    print "processing", str(datetime.datetime.now())
    paired = list(sorted(cooc))
    count = len(paired)/60
    bawah = 0
    minn = 0
    maxx = len(paired)
    jobs=[]
    for i in range(60):
        atas = bawah+count
        if atas > maxx:
            atas = maxx

        p = Process(target=commiter, args=(i, bawah, paired[bawah:atas], len(paired), ))
        
        jobs.append(p)
        p.start()
        bawah = atas
    
    for job in jobs:
        job.join()


def pre():
    conn = MySQLConnection(host='10.151.33.33', port="3307", database='stki', user='rahmat', password='rahmat')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT id_artikel FROM terms")
    artikel = cursor.fetchall() #all id artikel
    
    
    cursor.execute("SELECT * FROM terms")   #all the terms
    daftar = cursor.fetchall()
    f = open("co_ocu/daftar.pkl", "wb")    
    pickle.dump(daftar, f, pickle.HIGHEST_PROTOCOL) #dumping for multiprocess co_ocu
    f.close()
    print "weapon loaded"
    

    print "Total dokumen : "+str(len(artikel))+"\n"
    count = len(artikel)/10
    bawah = 0
    minn = 0
    maxx = len(artikel)
    jobs=[]
    for i in range(10):
        atas = bawah+count
        if atas > maxx:
            atas = maxx

        p = Process(target=co_ocu, args=(i, bawah, artikel[bawah:atas], ))
        jobs.append(p)
        p.start()
        bawah = atas
    
    for job in jobs:
        job.join()
    
    

if __name__ == '__main__':
    print "bismillah"
    #pre()
    post()
    
    


    