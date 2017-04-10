# import MySQLdb
import mysql.connector

def add_hasil_to_db(idquery, hasil):
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    f = open("hasil/"+str(idquery)+".txt", "a+")
    l = open("log/"+str(idquery)+".txt", "a+")
    try:
        sqlinsert = "insert into expand_result (query_expanded,id_query) values('"+str(hasil)+"',"+str(idquery)+");\n"
        cursor.execute(sqlinsert)
        f.write(sqlinsert)
        db.commit()
        l.write("Id_query: "+str(idquery)+" selesai")

    except:
        db.rollback()
        #l.write("gagal")
        print "gagal"
    pass

def qexpand(data):
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')
    kalimat = data[1].split();
    hasil = data[1]
# prepare a cursor object using cursor() method
    cursor = db.cursor()
# ambil 5 sinonim teratas
    for kata in kalimat:
        
#       rahmat coba ngedit: kemarin kan ngambil sinonim dari cooc, nah sekarang dari tabel sinonim  
#         cursor.execute("SELECT term2 AS term,cluster_weight AS cluster_weight FROM cooccurence WHERE term1 LIKE '"+kata+"' UNION SELECT term1 AS term,cluster_weight_2 AS cluster_weight FROM cooccurence WHERE term2 LIKE '"+kata+"' ORDER BY cluster_weight DESC LIMIT 5")
        cursor.execute("SELECT term2 AS term FROM sinonim WHERE term1 LIKE '"+kata+"' UNION SELECT term1 AS term FROM sinonim WHERE term2 LIKE '"+kata+"'")
        
        results = cursor.fetchall()
        if len(results) > 0:
            for result in results:
                hasil = hasil + " "
                hasil = hasil + result[0]
    add_hasil_to_db(data[0],hasil)

if __name__ == '__main__':
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("select id_query,keyword_query from queries order by id_query")
    data = cursor.fetchall()
    print "Query Expansion"
    for datum in data:
        qexpand(datum)
