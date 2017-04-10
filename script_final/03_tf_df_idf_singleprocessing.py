# -*- coding: utf-8 -*-

__author__ = 'rahmat'
# 16 December 2016 5:00 PM

"""
Script untuk menghitung tf, df, dan idf pada kata yang didapatkan dari Script 02_preprocess.py.
Script ini melakukan :
- mencari tf
- mencari df
- mencari idf
- mencari tf*idf

Catatan: script ini berjalan tanpa multiproses
"""

"""
Import library
"""

# library untuk akses ke database mysql
import mysql.connector

import math

# Open database connection
db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
cursor = db.cursor()

"""
Function code
"""

def make_dict(data):
    """
    Fungsi untuk mencari tf dan df dari kata.
    :param data: data dari tabel terms
    :return a_dict: dictionary hasil perhitungan tf dan df
    """

    # deklarasi dictionary penggabung kata
    a_dict = {}

    # untuk setiap kata i pada data
    for i in data:

        # jika dictionary a_dict memiliki key kata tersebut
        if a_dict.has_key(i[2]):

            # update isi elemen tersebut dengan menambahkan tf yang lama dengan tf yang baru, serta menambah df dengan nilai 1
            a_dict[i[2]] = [a_dict[i[2]][0] + i[3], a_dict[i[2]][1] + 1]

        # jika tidak, maka buat key dictionary baru berupa kata tersebut
        else:
            # kemudian mengisinya dengan tf kata tersebut dan df dimulai dari angka 1
            a_dict[i[2]] = [i[3], 1]

    # kembalikan a_dict
    return a_dict

def compute_idf(ndoc, data):
    """
    Fungsi untuk menghitung idf.
    :param ndoc: jumlah artikel
    :param data: data dictionary hasil dari fungsi make_dict
    :return data
    """

    # untuk setiap kata i pada data
    for i in data:

        # hitung idf nya
        data[i].append(math.log( float(ndoc[0]) / data[i][1], 10))

    # kembalikan data
    return data

def compute_tfidf(data):
    """
    Fungsi untuk menghitung tf*idf
    """
    # untuk setiap kata i pada data
    for i in data:

        # hitung tf*idf nya
        data[i].append( data[i][0] * data[i][2])

    # kembalikan data
    return data


"""
Main code
"""

# mendapatkan semua data terms dari tabel terms
cursor.execute("select * from terms")
output = cursor.fetchall()

# mendapatkan jumlah artikel yang diolah
cursor.execute("SELECT count(1) FROM `artikel`")
ndoc = cursor.fetchone()

print "Mulai menghitung tf, df, idf, tf*idf."

# menghitung tf dan df dengan memanggil fungsi make_dict
a_dict = make_dict(output)

# menghitung idf
a_dict = compute_idf(ndoc, a_dict)

# menghitung tf*idf
a_dict = compute_tfidf(a_dict)

# memasukkan hasil ke database tabel terms_distinct
try:
    # untuk setiap kata j dari a_dict yang telah di sort sesuai abjad (a-z)
    for j in sorted(a_dict, key=lambda key: (key)):

        print "menghitung", j

        # masukkan kata j, tf, df, idf, dan tf*idf nya pada tabel terms_distinct
        # mulanya, id_skenario digunakan untuk antisipasi skenario yang bervariasi, namun sampai sekarang tidak terpakai.
        sql1 = "insert into terms_distinct (term, tf, df, idf, tf_idf, id_skenario) values('"+j+"', "+str(a_dict[j][0])+", "+str(a_dict[j][1])+", "+ str(a_dict[j][2])+", "+str(a_dict[j][3])+", 1)"
        cursor.execute(sql1)

    # melakukan commit database
    db.commit()
    print "selesai."

except:
    # jika gagal, lakukan rollback database
    db.rollback()
    print "gagal."
