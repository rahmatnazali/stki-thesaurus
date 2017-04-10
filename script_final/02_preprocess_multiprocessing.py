__author__ = 'rahmat, haqiqi'
# 16 December 2016 6:44 PM

"""
Script untuk preproses data.
Script ini melakukan :
- word tokenization
- stopwords removal
- stemming
- pencocokan hasil praproses diatas dengan isi kateglo
- jika ada di kateglo dan kata benda/kata sifat, maka dimasukkan ke tabel "terms"

Catatan: script ini berjalan dengan multiproses
"""

# import MySQLdb
import mysql.connector
import re
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from multiprocessing import Process
import os

def preprocess(text):
    raw = text.split(' ')
    cleaner = re.compile('[^a-zA-Z-]')
    cleaned = []
    for i in raw:
        cleaned.append(cleaner.sub('', i).lower())
    row = filter(None,cleaned)
    factory_stemmer = StemmerFactory()
    stemmer = factory_stemmer.create_stemmer()
    row = [word for word in row if word not in stopwords.words('indonesian')]
    new_row = []
    for i in row:
        new_i = stemmer.stem(str(i))
        if len(new_i) > 2:
            new_row.append(new_i)
    row = new_row
    return row

def make_dict(row):
    a_dict = {}
    for i in row:
        if '-' in i:
            i = i.split('-')
            for j in i:
                if len(j) > 2:
                    if a_dict.has_key(j):
                        a_dict[j] += 1
                    else:
                        a_dict[j] = 1
            pass
        else:
            if a_dict.has_key(i):
                a_dict[i] += 1
            else:
                a_dict[i] = 1
    return a_dict

def add_term_to_db(i, iddok, a_dict):
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')
    cursor = db.cursor()
    c=i
    try:
        for j in sorted(a_dict, key=lambda key: (key)):
            sql_isnoun = "select count(1) from proc_definition where lemma='"+j+"' and lexical_id = 1"
            cursor.execute(sql_isnoun)
            isnoun = cursor.fetchone()
            if(isnoun[0]):
                sql1 = "insert into terms (id_artikel, term, tf) values("+str(iddok)+", '"+j+"', "+str(a_dict[j])+");\n"
                cursor.execute(sql1)
                c=c+1
        sql2 = "update artikel set flag=1 where id_artikel="+str(iddok)
        cursor.execute(sql2)
        db.commit()
        print "id_artikel:", iddok, "selesai"

    except:
        db.rollback()
        print "gagal"

def preprocessing(i, data):
    print "Preprocessing", i
    for record in data:
        a_string = record[1]+" "+record[3]+" "+record[4]
        a_string = a_string.replace('\n', ' ')
        a_string = a_string.replace('.', '. ')
        a_dict = make_dict(preprocess(a_string))
        add_term_to_db(i, record[0], a_dict)
    print i, "selesai."

def commiter():
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')
    cursor = db.cursor()
    for filename in os.listdir('hasil/'):

        f=open("hasil/"+filename, "r")
        print filename

        sql = f.readlines()
        #print sql
        for i in sql:
            cursor.execute(i)
            print i
        db.commit()

if __name__ == '__main__':
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')
    cursor = db.cursor()
    cursor.execute("select * from artikel where flag=0 order by id_artikel")
    data = cursor.fetchall()

    print "Preprocessing artikel"

    count = len(data)/5
    bawah = 0
    minn = 0
    maxx = len(data)-1
    for i in range(5):
        atas = bawah+count
        if atas > maxx:
            atas = maxx
        jobs = []
        p = Process(target=preprocessing, args=(i, data[bawah:atas], ))
        jobs.append(p)
        p.start()
        bawah = atas
    for job in jobs:
        job.join()
    commiter()
    print "cie, selesai"
