import mysql.connector
import operator
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


def add_hasil_to_db(idquery,hasil,i):
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    f = open("hasilsearch/"+str(idquery)+".txt", "a+")
    l = open("logsearch/"+str(idquery)+".txt", "a+")
    try:
        sqlinsert = "UPDATE expand_result SET artikel_"+str(i)+"="+str(hasil[0])+" WHERE id_query="+str(idquery)+";\n"
        cursor.execute(sqlinsert)
        f.write(sqlinsert)
        db.commit()
        l.write("Id_query: "+str(idquery)+" selesai")

    except:
        db.rollback()
        #l.write("gagal")
        print "gagal"
    pass

def search(data):
	db = mysql.connector.connect(host='127.0.0.1', port='3306',database='stki',user='root',password='')
        kalimat = data[1]
        kalimat = kalimat.encode('ascii','ignore')
        kalimat = kalimat.split()
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        kalimat_stemmed = map(lambda x:stemmer.stem(x), kalimat)
	hasil = {}
	cursor = db.cursor()
	for kata in kalimat_stemmed:
		cursor.execute("select id_artikel,terms.tf*terms_distinct.idf as tfidf,terms.term from terms inner join terms_distinct on terms.term = terms_distinct.term where terms.term LIKE '"+kata+"' order by id_artikel")
		results = cursor.fetchall()
		for result in results:
			if result[0] in hasil:
				now = hasil[result[0]]
				hasil[result[0]] = float(result[1]) + now
			else:
				hasil[result[0]] = float(result[1])
	sorted_hasil = sorted(hasil.items(),key=operator.itemgetter(1),reverse=True)
	i = 1
	for final in sorted_hasil:
		if i < 6:
			add_hasil_to_db(data[0],final,i)
			i=i+1
		else:
			break

if __name__ == '__main__':
    db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("select id_query,query_expanded from expand_result order by id_query")
    data = cursor.fetchall()
    print "Search by Query"
    for datum in data:
        search(datum)