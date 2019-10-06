# crawling-IG
TUGAS PENGANTAR KECERDASAN BUATAN ILMU KOMPUTER UNJ SEMESTER 111
Kelompok :
- Farhan Herdian Pradana 1313618030
- Tantyo Nurwahyu T 1313618004

Syarat untuk bisa menjalankan program :
    -Geckodriver.exe untuk firefox
    -browser mozilla firefox
    -python

Library yang digunakan :
    -Selenium
    -Pandas

Di tugas ini kami memisahkan program crawling instagram menjadi 3 program : 
- crawlingFollowers.py : 
    - Mengambil username instagram berdasarkan followers suatu user instagram
    - Saat dijalankan user diminta memasukan username dan password instagram yang aktif
    - User juga diminta untuk memasukkan jumlah username instagram yang akan diambil
    - Username yang dikumpulkan disimpan ke dalam file accounts.txt
- level 1.py :
    - Saat dijalankan program akan mengambil username di accounts.txt
    - Program secara otomatis akan mengambil captions, jumlah likes, komentar, dan tag setiap postingan user target
    - Semua data yang diambil akan disimpan ke dalam file level 1.csv
- level 2.py (case 2):
    - Saat dijalankan secara otomatis program akan membaca level 1.csv dan mengkonversinya menjadi level 2.csv case 2
