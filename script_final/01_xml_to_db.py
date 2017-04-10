__author__ = 'rahmat'

"""
Script untuk import XML ke database.
Sekarang tidak digunakan.
Import XML ke database sudah dibuat Bilfash didalam laravelnya

----------------
Contoh untuk run

import xml_to_db
xml_to_db("contoh_xml/",'10.151.33.33', 'rahmat', 'rahmat', 'stki')

Contoh keluaran
C:\Python27\python.exe D:/Onedrive/Python/STKI/fp/01_xml_parser/01_xml_to_db.py
contoh_xml/OLA_PO_15_001.xml sukses
contoh_xml/OLA_PO_15_002.xml sukses
contoh_xml/OLA_PO_15_003.xml sukses

Process finished with exit code 0
"""

import MySQLdb
import xml.etree.ElementTree as ET
import os

def xml_to_db(directory, host, username, password, database):
    """
    Fungsi untuk membaca semua file xml yang diberikan oleh paramter direktori, kemudian memasukkan ke database stki
    tabel artikel
    :param directory: lokasi folder tempat xml berada
    :param host: host db
    :param username: username db
    :param password: password db
    :param database: nama db
    :return: memanggil fungsi add-artikel untuk mengisi tabel arikel pada db stki
    """

    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            print os.path.join(directory, filename),
            a_xml = ET.parse(directory+filename).getroot()
            record = [None] * 7

            # cmiiw, dibaut if biar kalo ada temen2 yang xml nya kebalik nggak masalah
            for child in a_xml:
                if child.tag == 'id':
                    record[5] = directory+filename
                    record[6] = child.text[7:9]
                elif child.tag == 'judul':
                    record[0] = child.text
                elif child.tag == 'tanggal':
                    record[1] = child.text[6:]+"-"+child.text[3:5]+"-"+child.text[0:2]
                elif child.tag == 'kata_kunci':
                    record[2] = child.text
                elif child.tag == 'isi':
                    record[3] = child.text
                elif child.tag == 'link':
                    record[4] = child.text
            add_artikel_db(record, host, username, password, database)

def add_artikel_db(record, host, username, password, database):
    """
    Menambahkan sebuah record artikel ke tabel artikel pada database stki
    :param record: sebuah record berbentuk list, dengan indeks 7
    :param host: host db
    :param username: username db
    :param password: password db
    :param database: nama db
    :return: -; db artikel terisi dengan record
    """
    db = MySQLdb.connect(host, username, password, database )
    cursor = db.cursor()
    try:
        sql = "INSERT INTO artikel (judul_artikel, tanggal_artikel, kata_kunci_artikel, isi_artikel, link_artikel, nama_file, kelompok_pengunggah, created_at, updated_at) VALUES ('"+record[0]+"', '"+record[1]+"', '"+record[2]+"', '"+record[3]+"', '"+record[4]+"', '"+record[5]+"', '"+record[6]+"', NOW(), NOW())"
        cursor.execute(sql)
        db.commit()
        print "sukses"
    except:
        db.rollback()
        print "gagal"
    db.close()

# contoh run
# xml_to_db("contoh_xml/",'10.151.33.33', 'rahmat', 'rahmat', 'stki')
