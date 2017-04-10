__author__ = 'rahmat'
# 16 December 2016 5:00 PM

"""
Script untuk preproses data.
Script ini melakukan :
- word tokenization
- stopwords removal
- stemming
- pencocokan hasil praproses diatas dengan isi kateglo
- jika ada di kateglo dan kata benda/kata sifat, maka dimasukkan ke tabel "terms"

Catatan: script ini berjalan tanpa multiproses
"""

"""
Import library
"""

# library untuk akses ke database mysql
import mysql.connector

# library regex untuk tokenizing
import re

# library nltk untuk stopword removal
from nltk.corpus import stopwords

# library Sastrawi untuk stemming
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# library Sastrawi untuk stopword removal (dapat dijadikan variasi library stopword removal)
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Open database connection
db = mysql.connector.connect(host='10.151.33.33', port='3307',database='stki',user='rahmat',password='rahmat')

# prepare a cursor object using cursor() method
cursor = db.cursor()

"""
Function code
"""

def preprocess(text):
    """
    Fungsi untuk melakukan preproses (tokenizing, stopword removal, stemming)
    :param text : data artikel yang berisi judul, kata kunci, dan isi artikel yang telah dibentuk dalam satu baris
    :return row : list yang berisi kata artikel yang sudah dilakukan preprocessing
    """

    # Word tokenizer ------------------------------
    # text masukan dipisah berdasar spasi
    raw = text.split(' ')

    # membuat variabel cleaner untuk mengambil huruf saja dari text (simbol/selain huruf akan dihapus)
    cleaner = re.compile('[^a-zA-Z-]')

    # list penyimpan hasil tokenizing
    cleaned = []

    # untuk setiap kata dalam text
    for i in raw:

        # bersihkan kata tersebut dengan variabel cleaner, rubah semua ke lowercase, dan simpan ke list cleaned
        cleaned.append(cleaner.sub('', i).lower())

    # bersihkan list cleaned dari elemen kosong (sisa penghapusan) dan simpan ke variabel row bertipe list
    row = filter(None,cleaned)

    # Stopword removal & stemmer ------------------
    # factory_stemmer untuk pembangkit variabel stemmer
    factory_stemmer = StemmerFactory()

    # factory_stopword untuk pembangkit variabel stopword removal
    factory_stopword = StopWordRemoverFactory()

    # bangkitkan variabel stemmer dari factory_stemmer
    stemmer = factory_stemmer.create_stemmer()

    # bangkitkan variabel stopword removal dari factory_stemmer (uncomment baris dibawah jika ingin melakukan Stopword Removal dengan library Sastrawi
    # stopwords_removal = factory_stopword.create_stop_word_remover()

    # stopword removal; masukkan kata ke row jika kata tersebut bukan merupakan stopword yang berada pada library nltk
    # lokasi data stopword pada nltk (bisa ditambah manual dengan text editor) : [lokasi library nltk]\nltk_data\corpora\stopwords
    row = [word for word in row if word not in stopwords.words('indonesian')]

    # stemming
    new_row = []

    # untuk setiap kata dalam row
    for i in row:

        # stem kata tersebut dan simpan pada variabel new_i
        new_i = stemmer.stem(str(i))

        # jika new_i memiliki panjang lebih dari 2 (untuk menghapus hasil stemming tidak berarti yang kurang dari 2 digit)
        if len(new_i) > 2:
            # masukkan new_i ke new_row
            new_row.append(new_i)

    row = new_row

    # kembalikan row
    return row

def make_dict(row):
    """
    Fungsi untuk memasukkan kata hasil preprocessing kedalam kamus untuk mencari tf
    :param row: list yang berisi kata artikel yang sudah dilakukan preprocessing
    :return a_dict: dictionari berisi frekuensi kemunculan setiap kata (tf)
    """

    # deklarasi dictionary bernama a_dict; a_dict digunakan untuk mencari frekuensi munculnya kata (tf)
    a_dict = {}

    # untuk setiap kata dalam row
    for i in row:

        # jika kata mengandung dash "-" (contoh kasus: PDI-P, Ahok-Djarot)
        if '-' in i:

            # pisah kata tersebut berdasar dash
            i = i.split('-')

            # untuk setiap kata dari hasil pemisahan diatas
            for j in i:

                # jika kata tersebut memiliki panjang lebih dari dua (dengan harapan memiliki arti)
                if len(j) > 2:

                    # jika dictionary a_dict memiliki key kata tersebut
                    if a_dict.has_key(j):

                        # maka tambah isi dictionary pada key tersebut dengan 1
                        a_dict[j] += 1

                    else:

                        # jika tidak, maka buat key dictionary baru berupa kata tersebut, dan mengisinya dengan 1
                        a_dict[j] = 1
        else:
            # jika dictionary a_dict memiliki key kata tersebut
            if a_dict.has_key(j):

                # maka tambah isi dictionary pada key tersebut dengan 1
                a_dict[j] += 1

            else:

                # jika tidak, maka buat key dictionary baru berupa kata tersebut, dan mengisinya dengan 1
                a_dict[j] = 1

    # kembalikan a_dict
    return a_dict

def add_term_to_db(iddok, a_dict):
    """
    Fungsi untuk memasukkan data tf kedalam database
    :param iddok: id_dokumen pada artikel yang bersesuaian
    :param a_dict: dictionary berisi kata dan frekuensi kemunculannya pada artikel tersebut (tf)
    """

    try:
        # untuk j pada a_dict yang telah disort berdasar kata (urut dari a-z)
        for j in sorted(a_dict, key=lambda key: (key)):

            # untuk debug, dapat dilakukan print iddok, kata j, dan tf nya a_dict[j]
            # print iddok, j, a_dict[j]

            # pencocokan kateglo: cek apakah kata tersebut kata benda (noun), yang didapat dari tabel kateglo
            sql_isnoun = "select count(1) from proc_definition where lemma='"+j+"' and lexical_id = 1"
            cursor.execute(sql_isnoun)
            isnoun = cursor.fetchone()

            # jika kata merupakan kata benda/noun
            if(isnoun[0]):

                # masukkan kata tersebut beserta id_dokumen dan tf nya kedalam tabel terms
                sql1 = "insert into terms (id_artikel, term, tf) values("+str(iddok)+", '"+j+"', "+str(a_dict[j])+")"
                cursor.execute(sql1)

        # lakukan update attribut flag pada tabel artikel untuk menandai sudah dilakukan preproses
        sql2 = "update artikel set flag=1 where id_artikel="+str(iddok)
        cursor.execute(sql2)

        # melakukan commit pada database
        db.commit()
        print "id_artikel:", iddok, "selesai"

    except:
        # jika ada kesalahan, lakukan rollback pada database
        db.rollback()
        print "gagal"

    return


"""
Main code
"""

print "Mulai preprocessing artikel"

# melakukan pengambilan data artikel yang belum dicek (memiliki flag=0)
cursor.execute("select * from artikel where flag=0")
data = cursor.fetchall()

# melakukan preprosesing setiap data yang didapatkan
for record in data:

    # mengambil judul, kata kunci, dan isi berita saja
    a_string = record[1]+" "+record[3]+" "+record[4]

    # menghilangkan \n dari variabel a_string agar lebih cantik
    a_string = a_string.replace('\n', ' ')

    # memisahkan tanda titik yang diapit dua huruf (karena ada beberapa kesalahan input artikel pada xml)
    # jika titik antar huruf tidak diberi spasi, maka akan dianggap satu kata sehingga mengganggu stemming dan stopword removal
    a_string = a_string.replace('.', '. ')

    # membuat dictionary a_dict untuk menampung hasil fungsi make_dict
    a_dict = make_dict(preprocess(a_string))

    # menyerahkan id_artikel dan a_dict pada fungsi add_term_to_db untuk dimasukkan ke tabel terms
    add_term_to_db(record[0], a_dict)

print "selesai."
