# crawling-IG
TUGAS PENGANTAR KECERDASAN BUATAN ILMU KOMPUTER UNJ SEMESTER 111
Kelompok :
- Farhan Herdian Pradana 1313618030
- Tantyo Nurwahyu T 1313618004

Syarat untuk bisa menjalankan program :
    -Geckodriver.exe untuk firefox
    -browser mozilla firefox
    -python
    -MongoDB

Library yang digunakan :
    -Selenium
    -Pandas
    -PyMongo

Di tugas ini kami memisahkan program crawling instagram menjadi 4 program : 
- crawlingFollowers.py : 
    - Mengambil username instagram berdasarkan followers suatu user instagram
    - Saat dijalankan user diminta memasukan username dan password instagram yang aktif
    - User juga diminta untuk memasukkan username akun pertama yang akan dikunjungi, serta jumlah ring followers-nya
    - Username yang dikumpulkan disimpan ke dalam file accounts.txt
- level 1.py :
    - Saat dijalankan program akan mengambil username di accounts.txt
    - Program secara otomatis akan mengambil captions, jumlah likes, komentar, dan tag setiap postingan user target
    - Semua data yang diambil akan disimpan ke dalam file level 1.csv
- level 2.py (case 2):
    - Saat dijalankan secara otomatis program akan membaca level 1.csv dan mengkonversinya menjadi level 2.csv case 2
- level 3.py :
    - Sebelum menjalankan program ini, user harus menjalankan aplikasi "mongod.exe"
    - Ketika dijalankan, secara otomatis akan memasukkan file "level 1.csv" dan "level 2.csv" ke MongoDB
    - Terdapat 5 fitur pada program ini :
        - Postingan dengan like paling banyak pada setiap akun
            - Pada fitur ini, ketika dipilih, akan ditampilkan postingan dengan like paling banyak pada setiap user yang berada di file "level 1.csv"
        - Postingan dengan like paling sedikit pada setiap akun
            - Pada fitur ini, ketika dipilih, akan ditampilan postingan dengan like paling sedikit pada setiap user yang berada di file "level 2.csv"
        - Postingan dengan hashtag tertentu
            - Pada fitur ini, ketika dipilih, user akan diminta untuk memasukkan hashtag satu atau lebih dipisahkan dengan spasi. Setelah dijalankan, akan ditampilkan postingan yang mengandung hashtag tersebut
        - Peringkat hashtag teratas
            - Pada fitur ini, ketika dipilih, user akan diminta untuk memasukkan jumlah hashtag teratas, n. Setelah dijalankan, akan ditampilkan peringkat n teratas hashtag dan jumlah frekuensi hashtag tersebut
        - Prediksi kata
            - Pada fitur ini, ketika dipilih, user akan diminta untuk memasukkan kata yang nanti nya akan diprediksi kata selanjutnya menggunakan metode Naive Bayes
