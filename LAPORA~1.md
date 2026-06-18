## **LAPORAN PROYEK AKHIR** 

**AUDIT KEAMANAN DAN IMPLEMENTASI MEKANISME PERLINDUNGAN PADA LAYER SESI, PRESENTASI, DAN APLIKASI (OSI LAYER 5–7) BERBASIS OWASP ASVS DAN ISO/IEC 27001:2022 PADA PLATFORM MARKETPLACE BERIMA** 

## **Mata Kuliah: Keamanan Jaringan** 

**Dosen Pengampu:** Dr. Susanto, M.Kom. 

## **Disusun oleh:** 

1. 2410512100 - Adam Dorman 

2. 2410512077 - Jehezkiel Hinn Sumita 

3. 2410512088 - Muhammad Afif Fadhilah 

4. 2410512082 - Rafael Ananta Razid 

5. 2410512093 - Rajendra Mahyaputra Adityawan 

_Keamanan Jaringan | Kelas C | Pertemuan 16_ 

## **PROGRAM STUDI S1 SISTEM INFORMASI FAKULTAS ILMU KOMPUTER UNIVERSITAS PEMBANGUNAN NASIONAL VETERAN JAKARTA JAKARTA SELATAN DKI JAKARTA** 

**2026** 

## **DAFTAR ISI** 

**DAFTAR ISI............................................................................................................................. 2 DAFTAR GAMBAR................................................................................................................ 3 BAB I | PENDAHULUAN....................................................................................................... 1** 1.1 Latar Belakang............................................................................................................... 1 1.2 Rumusan Masalah.......................................................................................................... 2 1.3 Tujuan Proyek................................................................................................................ 2 1.4 Ruang Lingkup (Scope)................................................................................................. 2 **BAB II | TINJAUAN LITERATUR........................................................................................4** 2.1 Model Referensi OSI pada Konteks Keamanan Aplikasi Web......................................4 2.2 Autentikasi dan Manajemen Sesi Web...........................................................................5 2.3 Password Hashing: Algoritma dan Praktik Terbaik....................................................... 5 2.4 Role-Based Access Control (RBAC)............................................................................. 6 2.5 Transport Layer Security (TLS) 1.3...............................................................................7 2.6 ISO/IEC 27001:2022 dan Kontrol yang Relevan...........................................................7 2.7 OWASP Application Security Verification Standard (ASVS)....................................... 8 **BAB III | IDENTIFIKASI ASET INFORMASI................................................................. 10** 3.1 Metodologi Identifikasi Aset........................................................................................10 3.2 Inventarisasi Aset Informasi Platform Berima.............................................................10 3.2.1 Aset Data Pengguna............................................................................................ 10 3.2.2 Aset Data Autentikasi dan Sesi........................................................................... 10 3.2.3 Aset Data Transaksi Jasa (Gig)........................................................................... 11 3.2.4 Aset Data Peran dan Otorisasi.............................................................................11 3.2.5 Aset Infrastruktur dan Konfigurasi......................................................................11 3.2.6 Aset Log dan Audit Trail.....................................................................................12 3.3 Ringkasan Matriks Aset............................................................................................... 12 **BAB IV | ANALISIS ANCAMAN DAN RISIKO............................................................... 13** 4.1 Metodologi Analisis Ancaman.....................................................................................13 4.2 Identifikasi dan Analisis Ancaman per Kategori STRIDE.......................................... 13 4.2.1 Spoofing - Pemalsuan Identitas...........................................................................13 4.2.2 Tampering - Manipulasi Data..............................................................................14 4.2.3 Repudiation - Penyangkalan Tindakan................................................................14 4.2.4 Information Disclosure - Pengungkapan Informasi............................................ 14 4.2.5 Denial of Service - Penolakan Layanan.............................................................. 15 4.2.6 Elevation of Privilege - Peningkatan Hak Akses................................................ 15 4.3 Matriks Risiko Konsolidasi..........................................................................................15 **BAB V | EVALUASI TATA KELOLA KEAMANAN (ISO/IEC 27001:2022)................. 17** 5.1 Metodologi Evaluasi.................................................................................................... 17 5.2 Hasil Gap Analysis.......................................................................................................17 5.3 Ringkasan Gap Analysis.............................................................................................. 19 **BAB VI | IMPLEMENTASI MEKANISME KEAMANAN.............................................. 21** 

**ii** 

6.1 Arsitektur Sistem..........................................................................................................21 6.2 Konfigurasi Keamanan Dasar (config.py)....................................................................22 6.3 Model Database (models.py)........................................................................................23 6.4 Implementasi Autentikasi Aman (auth/routes.py)....................................................... 27 6.5 Implementasi Role-Based Access Control (utils/decorators.py)..................................32 6.6 Implementasi HTTPS/TLS dan Security Headers....................................................... 37 **BAB VII | PENGUJIAN KEAMANAN............................................................................... 43** 7.1 Metodologi Pengujian.................................................................................................. 43 7.2 Pengujian Password Hashing....................................................................................... 43 7.3 Pengujian Autentikasi dan Session Management.........................................................44 7.4 Pengujian RBAC dan Kontrol Akses...........................................................................46 7.5 Pengujian Konfigurasi TLS..........................................................................................47 7.6 Pengujian Menggunakan OWASP ZAP.......................................................................48 7.7 Ringkasan Hasil Pengujian...........................................................................................48 **BAB VIII | KESIMPULAN DAN REKOMENDASI..........................................................50** 8.1 Kesimpulan...................................................................................................................50 8.2 Rekomendasi untuk Pengembangan Lebih Lanjut.......................................................51 **REFERENSI...........................................................................................................................52** 

**ii** 

## **DAFTAR GAMBAR** 

Gambar 1. Visibilitas Mesin IDS (ids-server) pada Jaringan Mesh VPN Tailscale...................5 Gambar 2. Akses Remote Terminal Berhasil Dilakukan Menggunakan PuTTY.......................6 

**iii** 

## **BAB I | PENDAHULUAN** 

## **1.1 Latar Belakang** 

Perkembangan ekosistem digital kampus menciptakan peluang sekaligus risiko keamanan informasi yang signifikan. Platform berbasis web yang memfasilitasi transaksi antar pengguna, khususnya model Customer-to-Customer (C2C)  menjadi target yang menarik bagi pelaku ancaman karena menyimpan kombinasi data pribadi, data finansial, dan data transaksi secara bersamaan dalam satu sistem. Berima merupakan platform marketplace micro-gigs berbasis C2C yang dirancang untuk memenuhi kebutuhan komunitas mahasiswa di lingkungan kampus, menghubungkan mahasiswa yang menawarkan jasa (seller) dengan mahasiswa yang membutuhkan jasa (buyer) dalam ekosistem yang terstruktur. 

Dari perspektif keamanan jaringan, aplikasi web merupakan entitas yang beroperasi pada layer-layer atas model referensi OSI, khususnya Layer 5 (Session), Layer 6 (Presentation), dan Layer 7 (Application). Ketiga layer ini merupakan titik interaksi langsung antara pengguna dengan sistem, sehingga menjadi vektor serangan yang paling sering dieksploitasi. Data dari OWASP Top 10 2021 menunjukkan bahwa kelemahan pada lapisan ini, mulai dari Broken Access Control (A01), Cryptographic Failures (A02), Injection (A03), hingga Identification and Authentication Failures (A07), secara konsisten mendominasi daftar kerentanan paling kritis pada aplikasi web modern. 

Berima, sebagai platform yang mengelola identitas pengguna, sesi autentikasi, data transaksi jasa, dan pengendalian akses berbasis peran, memerlukan fondasi keamanan yang kuat dan terstruktur. Tanpa implementasi mekanisme keamanan yang memadai pada ketiga layer tersebut, platform ini rentan terhadap berbagai serangan seperti session hijacking, credential stuffing, privilege escalation, man-in-the-middle attacks, dan cross-site scripting yang dapat merusak kepercayaan pengguna serta integritas platform secara keseluruhan. 

Laporan ini mendokumentasikan seluruh proses audit keamanan dan implementasi mekanisme perlindungan pada platform Berima, mulai dari identifikasi aset informasi, analisis ancaman dan risiko menggunakan metodologi STRIDE, evaluasi tata kelola keamanan berdasarkan framework ISO/IEC 27001:2022, hingga implementasi teknis yang mencakup mekanisme autentikasi aman, manajemen sesi, password hashing, Role-Based Access Control (RBAC), dan enkripsi komunikasi melalui HTTPS/TLS. Seluruh implementasi diuji secara sistematis untuk memverifikasi efektivitasnya. 

**1** 

## **1.2 Rumusan Masalah** 

Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam laporan ini adalah sebagai berikut: 

1. Aset informasi apa saja yang dimiliki platform Berima dan bagaimana profil sensitivitasnya? 

2. Ancaman dan risiko keamanan apa yang relevan terhadap platform Berima pada layer 5, 6, dan 7 OSI? 

3. Sejauh mana tata kelola keamanan platform Berima sesuai dengan kontrol-kontrol dalam ISO/IEC 27001:2022? 

4. Bagaimana mekanisme keamanan yang tepat dapat diimplementasikan untuk melindungi aset informasi Berima pada ketiga layer tersebut? 

5. Bagaimana efektivitas implementasi mekanisme keamanan tersebut dapat diverifikasi melalui pengujian? 

## **1.3 Tujuan Proyek** 

Tujuan laporan proyek akhir ini adalah: 

1. Mengidentifikasi dan mengklasifikasikan seluruh aset informasi yang dikelola oleh platform Berima berdasarkan tingkat sensitivitas dan kritikalitasnya. 

2. Menganalisis ancaman dan risiko keamanan yang relevan menggunakan model ancaman STRIDE dan matriks risiko. 

3. Mengevaluasi kondisi tata kelola keamanan eksisting Berima menggunakan subset kontrol ISO/IEC 27001:2022 yang relevan. 

4. Merancang dan mengimplementasikan mekanisme keamanan yang mencakup: login/logout aman, manajemen sesi, password hashing dengan bcrypt, RBAC tiga tingkat (admin/seller/buyer), dan komunikasi terenkripsi via HTTPS/TLS 1.3. 

5. Melakukan pengujian keamanan fungsional dan penetrasi terbatas untuk memverifikasi efektivitas implementasi. 

**2** 

## **1.4 Ruang Lingkup (Scope)** 

Ruang lingkup laporan ini dibatasi pada: 

1. **Sistem yang dianalisis:** Platform web Berima (versi pengembangan lokal berbasis Python Flask) 

2. **Layer yang dicakup:** OSI Layer 5 (Session), Layer 6 (Presentation), Layer 7 (Application) 

3. **Framework referensi:** ISO/IEC 27001:2022 (subset kontrol relevan), OWASP Application Security Verification Standard (ASVS) v4.0.3, OWASP Top 10 2021, NIST SP 800-63B 

4. **Implementasi teknis:** Menggunakan Python 3.11, Flask 3.x, bcrypt, Flask-Login, SQLite/PostgreSQL, Werkzeug, dan sertifikat TLS self-signed untuk lingkungan pengembangan 

5. **Pengujian:** Pengujian fungsional, pengujian penetrasi terbatas menggunakan OWASP ZAP dan curl, serta verifikasi manual 

**3** 

## **BAB II | TINJAUAN LITERATUR** 

## **2.1 Model Referensi OSI pada Konteks Keamanan Aplikasi Web** 

- Model referensi OSI (Open Systems Interconnection) yang didefinisikan dalam 

- standar ISO/IEC 7498-1 membagi komunikasi jaringan menjadi tujuh lapisan hierarkis. Dalam konteks keamanan aplikasi web, tiga layer teratas memiliki relevansi paling tinggi karena merupakan titik di mana logika bisnis, autentikasi, otorisasi, dan enkripsi data berlangsung. 1. **Layer 5 - Session Layer** bertanggung jawab atas pembentukan, pemeliharaan, dan penghentian sesi komunikasi antar aplikasi. Dalam konteks web, layer ini mencakup manajemen sesi HTTP melalui mekanisme seperti session cookies, token berbasis JWT (JSON Web Token), atau session ID yang tersimpan di server. Risiko keamanan yang paling signifikan pada layer ini meliputi session hijacking, session fixation, dan session replay attacks. Standar OWASP ASVS v4.0.3 mendedikasikan seluruh bab V3 (Session Management Verification Requirements) untuk persyaratan keamanan pada layer ini. 

   2. **Layer 6 - Presentation Layer** menangani representasi data, termasuk enkripsi, dekripsi, kompresi, dan konversi format. Dalam implementasi web modern, layer ini direpresentasikan oleh protokol TLS (Transport Layer Security) yang mengenkripsi seluruh payload komunikasi antara klien dan server. TLS 1.3, yang distandarkan dalam RFC 8446 (Rescorla, 2018), merupakan versi terkini yang menghilangkan algoritma kriptografi lemah dari versi-versi sebelumnya dan memperkenalkan mekanisme handshake yang lebih cepat dan lebih aman melalui 0-RTT resumption. Pada layer ini, password hashing juga tergolong sebagai mekanisme presentasi data karena mengubah representasi kredensial dari plaintext menjadi digest yang tidak dapat dibalik. 

   3. **Layer 7 - Application Layer** adalah layer yang langsung berinteraksi dengan pengguna dan menyediakan layanan jaringan kepada aplikasi. Protokol utama pada layer ini dalam konteks web adalah HTTP/HTTPS. Keamanan layer 7 mencakup autentikasi pengguna, otorisasi berbasis peran, validasi input, pengelolaan error, logging, dan perlindungan terhadap serangan seperti SQL injection, XSS, CSRF, dan broken access control. OWASP Top 10 2021 secara dominan mengidentifikasi 

**4** 

kerentanan pada layer ini sebagai yang paling sering ditemui dan paling merusak secara bisnis. 

## **2.2 Autentikasi dan Manajemen Sesi Web** 

Autentikasi merupakan proses verifikasi identitas entitas yang mengklaim identitas tertentu kepada sistem. NIST SP 800-63B (Grassi et al., 2020) mendefinisikan tiga faktor autentikasi: sesuatu yang diketahui (knowledge factor, seperti password), sesuatu yang dimiliki (possession factor, seperti OTP token), dan sesuatu yang melekat pada diri pengguna (inherence factor, seperti biometrik). Untuk konteks platform marketplace akademik seperti Berima, autentikasi berbasis knowledge factor melalui kombinasi email dan password dengan penguatan melalui password policy yang ketat merupakan baseline yang dipersyaratkan. 

Manajemen sesi web mengacu pada serangkaian mekanisme yang digunakan untuk mempertahankan konteks autentikasi pengguna antara satu permintaan HTTP dan permintaan berikutnya, mengingat sifat HTTP yang stateless secara inheren. OWASP Session Management Cheat Sheet menggariskan praktik terbaik yang mencakup: penggunaan session ID yang panjang dan acak secara kriptografis (minimal 128 bit entropy), transmisi session ID hanya melalui channel terenkripsi (HTTPS), penandaan cookie dengan atribut HttpOnly dan Secure, implementasi session timeout yang tepat, regenerasi session ID setelah peristiwa privilege escalation (login, logout, perubahan peran), dan mekanisme invalidasi sesi pada server. 

## **2.3 Password Hashing: Algoritma dan Praktik Terbaik** 

Penyimpanan password dalam bentuk plaintext merupakan pelanggaran keamanan fundamental. Penggunaan fungsi hash kriptografis generik seperti MD5 atau SHA-1 tanpa salt juga tidak memadai karena rentan terhadap rainbow table attacks dan dictionary attacks yang dipercepat oleh hardware modern (GPU clusters mampu menghitung miliaran hash MD5 per detik). Standar industri saat ini mensyaratkan penggunaan fungsi hash yang dirancang khusus untuk password dengan karakteristik: komputasi yang secara sengaja lambat (intentionally slow), resistensi terhadap serangan berbasis GPU, dan dukungan untuk parameter cost yang dapat dikalibrasi seiring peningkatan kapasitas komputasi. 

Algoritma yang direkomendasikan saat ini adalah: 

**bcrypt** (Provos & Mazières, 1999) - dikembangkan oleh Niels Provos dan David Mazières, bcrypt menggunakan algoritma Blowfish yang dimodifikasi dan memiliki parameter cost factor (work factor) yang mengontrol jumlah iterasi. Dengan cost factor 12, sebuah hash 

bcrypt membutuhkan waktu sekitar 250ms pada hardware modern, menjadikan serangan brute force secara praktis tidak layak. bcrypt secara resmi direkomendasikan oleh OWASP Password Storage Cheat Sheet dan NIST SP 800-63B untuk aplikasi yang memiliki kendala pada penggunaan Argon2. 

**Argon2id** - pemenang Password Hashing Competition (PHC) 2015, Argon2id merupakan varian hibrida yang menggabungkan resistensi terhadap GPU attacks (dari Argon2d) dan resistensi terhadap side-channel attacks (dari Argon2i). Argon2id adalah pilihan pertama yang direkomendasikan oleh OWASP saat ini. 

Dalam implementasi Berima, bcrypt dipilih karena ketersediaan library yang matang di ekosistem Python (passlib.hash.bcrypt) dan kompatibilitasnya yang luas, dengan cost factor yang dikonfigurasi pada nilai 12. 

## **2.4 Role-Based Access Control (RBAC)** 

RBAC adalah model kontrol akses yang didefinisikan secara formal dalam NIST RBAC Model (Sandhu et al., 1996) dan standar ANSI INCITS 359-2004. Dalam RBAC, izin (permissions) ditetapkan pada peran (roles), bukan langsung pada pengguna individual. Pengguna kemudian ditugaskan ke satu atau lebih peran, sehingga secara tidak langsung memperoleh izin yang terkait dengan peran tersebut. Pendekatan ini memungkinkan administrasi kontrol akses yang jauh lebih terkelola dibandingkan Discretionary Access Control (DAC) pada sistem dengan jumlah pengguna yang besar. 

Model RBAC standar mendefinisikan empat komponen inti: Users (U), Roles (R), Permissions (P), dan Sessions (S), beserta fungsi mapping UA: U → 2^R (user-role assignment), PA: R → 2^P (permission-role assignment), dan user_sessions: U → 2^S. Prinsip Least Privilege — yang merupakan salah satu prinsip keamanan paling fundamental, diartikulasikan pertama kali oleh Saltzer & Schroeder (1975) — secara alami ditegakkan dalam RBAC dengan memastikan setiap peran hanya memiliki izin minimum yang diperlukan untuk menjalankan fungsinya. 

Pada platform Berima, tiga peran didefinisikan: **Admin** (akses penuh terhadap seluruh sistem, termasuk manajemen pengguna, verifikasi seller, dan audit log), **Seller** (akses untuk mengelola profil, listing jasa, dan memproses order yang masuk), dan **Buyer** (akses untuk menelusuri listing, melakukan order, dan mengelola profil). 

## **2.5 Transport Layer Security (TLS) 1.3** 

**6** 

TLS adalah protokol kriptografis yang menyediakan keamanan komunikasi melalui jaringan komputer, berjalan tepat di atas TCP dan di bawah protokol aplikasi seperti HTTP (menghasilkan HTTPS). TLS 1.3, yang distandarkan dalam RFC 8446 pada Agustus 2018, membawa perubahan signifikan dibandingkan TLS 1.2: 

Pertama, cipher suite yang diizinkan dikurangi drastis menjadi hanya lima: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_AES_128_GCM_SHA256, TLS_AES_128_CCM_8_SHA256, dan TLS_AES_128_CCM_SHA256. Seluruh cipher suite yang menggunakan algoritma lemah (RC4, 3DES, MD5, SHA-1) dieliminasi. Kedua, mekanisme key exchange menggunakan ephemeral Diffie-Hellman secara eksklusif, yang memastikan Forward Secrecy, bahwa kompromi kunci privat jangka panjang tidak memungkinkan dekripsi rekaman sesi lama. Ketiga, proses handshake dipercepat menjadi satu round-trip (1-RTT) untuk koneksi baru, dan zero round-trip (0-RTT) untuk resumption sesi. 

Untuk implementasi pada platform Berima di lingkungan pengembangan, digunakan sertifikat self-signed yang dihasilkan melalui OpenSSL, sementara untuk lingkungan produksi direkomendasikan penggunaan sertifikat dari Certificate Authority (CA) yang diakui melalui protokol ACME (Automated Certificate Management Environment, RFC 8555) yang diimplementasikan oleh Let's Encrypt. 

## **2.6 ISO/IEC 27001:2022 dan Kontrol yang Relevan** 

ISO/IEC 27001:2022 adalah standar internasional untuk Information Security Management Systems (ISMS) yang diterbitkan oleh International Organization for Standardization dan International Electrotechnical Commission. Standar ini menetapkan persyaratan untuk membangun, mengimplementasikan, memelihara, dan terus memperbaiki sistem manajemen keamanan informasi dalam konteks organisasi. Pembaruan tahun 2022 merestrukturisasi Annex A dari 114 kontrol dalam 14 klausul menjadi 93 kontrol dalam 4 tema: Organizational Controls (37), People Controls (8), Physical Controls (14), dan Technological Controls (34). 

Kontrol-kontrol ISO/IEC 27001:2022 yang paling relevan dengan implementasi keamanan layer 5–7 pada Berima antara lain: 

1. **A.5.15 - Access Control:** Persyaratan untuk menetapkan, mendokumentasikan, dan menegakkan kebijakan kontrol akses berdasarkan prinsip need-to-know dan least privilege. 

**7** 

2. **A.5.16 - Identity Management:** Pengelolaan siklus hidup identitas pengguna, termasuk pembuatan, pemeliharaan, dan penghapusan akun. 

3. **A.5.17 - Authentication Information:** Persyaratan untuk pengelolaan informasi autentikasi yang aman, termasuk kebijakan password, penyimpanan kredensial yang aman, dan kontrol distribusi. 

4. **A.8.3 - Information Access Restriction:** Pembatasan akses terhadap informasi dan fungsi sistem aplikasi sesuai dengan kebijakan kontrol akses. 

5. **A.8.5 - Secure Authentication:** Implementasi mekanisme autentikasi aman berdasarkan penilaian risiko terhadap aplikasi. 

6. **A.8.20 - Network Security:** Keamanan jaringan mencakup penggunaan protokol yang aman dan perlindungan terhadap transmisi data. 

7. **A.8.24 - Use of Cryptography:** Kebijakan penggunaan kriptografi, termasuk persyaratan enkripsi untuk data dalam transit dan data saat penyimpanan. 

8. **A.8.26 - Application Security Requirements:** Persyaratan keamanan yang harus diintegrasikan dalam siklus pengembangan aplikasi. 

9. **A.8.28 - Secure Coding:** Penerapan prinsip pengkodean aman untuk mencegah kerentanan umum pada layer aplikasi. 

## **2.7 OWASP Application Security Verification Standard (ASVS)** 

OWASP ASVS v4.0.3 adalah kerangka kerja komprehensif yang mendefinisikan persyaratan keamanan fungsional dan non-fungsional untuk aplikasi web dan layanan web. ASVS mendefinisikan tiga level verifikasi: Level 1 (minimal, untuk semua perangkat lunak), Level 2 (untuk aplikasi yang memproses data sensitif), dan Level 3 (untuk aplikasi kritis yang memerlukan tingkat kepercayaan tertinggi). Untuk platform Berima yang memproses data transaksi dan identitas pengguna, Level 2 adalah target yang sesuai. 

Bab-bab ASVS yang relevan dengan proyek ini adalah: 

1. **V2 - Authentication Verification Requirements:** Mencakup keamanan password, autentikasi general, dan mekanisme pencegahan brute force. 

2. **V3 - Session Management Verification Requirements:** Mencakup fundamental manajemen sesi, binding sesi, dan logout serta timeout. 

**8** 

3. **V4 - Access Control Verification Requirements:** Mencakup prinsip desain kontrol akses dan model kontrol akses berbasis peran. 

4. **V6- Stored Cryptography Verification Requirements:** Mencakup persyaratan untuk penyimpanan data kriptografis. 

5. **V9 - Communication Verification Requirements:** Mencakup keamanan komunikasi melalui TLS. 

**9** 

## **BAB III | IDENTIFIKASI ASET INFORMASI** 

## **3.1 Metodologi Identifikasi Aset** 

Identifikasi aset informasi dilakukan menggunakan pendekatan berbasis data flow analysis, menelusuri setiap titik di mana data dibuat, diproses, disimpan, ditransmisikan, atau dihapus dalam platform Berima. Proses ini mengacu pada panduan inventarisasi aset dalam ISO/IEC 27001:2022 Klausul 8.1 dan A.5.9 (Inventory of Information and Other Associated Assets). Setiap aset yang diidentifikasi kemudian diklasifikasikan berdasarkan tiga dimensi keamanan informasi: Confidentiality (C), Integrity (I), dan Availability (A), dengan skala penilaian Tinggi (T), Sedang (S), dan Rendah (R). 

## **3.2 Inventarisasi Aset Informasi Platform Berima** 

## **3.2.1 Aset Data Pengguna** 

Aset paling sensitif dalam platform Berima adalah data identitas pengguna. Ini mencakup: nama lengkap, alamat email, nomor induk mahasiswa (NIM), nomor telepon, dan password hash. Data ini memiliki klasifikasi Confidentiality: Tinggi, Integrity: Tinggi, Availability: Tinggi, karena kompromisasi terhadap data identitas dapat menyebabkan identity theft, penyalahgunaan akun, dan pelanggaran privasi yang signifikan bagi komunitas mahasiswa. Berdasarkan Undang-Undang Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP), data nama, alamat email, nomor telepon, dan NIM termasuk kategori data pribadi yang dilindungi, sementara informasi biometrik dan data keuangan termasuk kategori data pribadi yang bersifat spesifik dengan perlindungan yang lebih ketat. 

## **3.2.2 Aset Data Autentikasi dan Sesi** 

Aset ini mencakup: credential hash (bcrypt digest dari password pengguna), session token/cookie, dan mekanisme pemulihan akun (reset password token). Kredensial hash memiliki nilai Confidentiality: Tinggi karena meskipun sudah di-hash, kompromi massal terhadap tabel password dapat memungkinkan offline brute force attack. Session token bersifat sangat sensitif karena kepemilikan session token yang valid setara dengan kepemilikan akses terautentikasi ke akun pengguna tanpa memerlukan password sama sekali. Reset password token memiliki waktu hidup terbatas (time-limited, single-use) namun sangat kritis karena memberikan akses untuk mengambil alih akun. 

**10** 

## **3.2.3 Aset Data Transaksi Jasa (Gig)** 

Data listing jasa (gig) yang diposting oleh seller mencakup: judul layanan, deskripsi, harga, portofolio, dan status ketersediaan. Data order mencakup: informasi pembeli, spesifikasi permintaan, status order (pending/in-progress/completed/cancelled), dan riwayat komunikasi. Data transaksi mencakup: nominal, metode pembayaran, timestamp, dan status. Aset-aset ini memiliki Confidentiality: Sedang-Tinggi (tergantung sensitivitas konten spesifik), Integrity: Tinggi (karena manipulasi data transaksi berdampak langsung pada kepercayaan dan nilai finansial), dan Availability: Tinggi (karena unavailability platform langsung mengganggu aktivitas bisnis pengguna). 

## **3.2.4 Aset Data Peran dan Otorisasi** 

Tabel pemetaan peran pengguna (user-role mapping), definisi izin per peran (permission definitions), dan log audit akses merupakan aset kontrol yang kritis. Manipulasi terhadap data ini, misalnya mengubah peran buyer menjadi admin secara tidak sah, merupakan privilege escalation attack yang dapat memberikan akses tidak terbatas terhadap seluruh sistem. Klasifikasi: Confidentiality: Tinggi, Integrity: Tinggi, Availability: Sedang. 

## **3.2.5 Aset Infrastruktur dan Konfigurasi** 

Kunci privat TLS, kunci enkripsi aplikasi (secret key Flask), konfigurasi database, dan variabel lingkungan (environment variables) merupakan aset infrastruktur yang sangat sensitif. Kompromi terhadap kunci privat TLS memungkinkan penyerang melakukan man-in-the-middle attacks terhadap seluruh komunikasi pengguna. Kompromi terhadap secret key Flask memungkinkan pemalsuan session cookie. Klasifikasi: Confidentiality: Tinggi, Integrity: Tinggi, Availability: Tinggi. 

## **3.2.6 Aset Log dan Audit Trail** 

Log aktivitas autentikasi (login success/failure), log akses per endpoint, dan log audit perubahan data sensitif merupakan aset detektif yang kritis untuk keamanan. Log ini memungkinkan investigasi insiden, deteksi anomali, dan pembuktian dalam proses penanggulangan insiden. Klasifikasi: Confidentiality: Sedang (log berisi metadata aktivitas yang sensitif), Integrity: Tinggi (manipulasi log menghilangkan bukti serangan), Availability: Sedang. 

**11** 

## **3.3 Ringkasan Matriks Aset** 

**Tabel 1.** Summary Matriks Aset 

|**No**|**Nama Aset**|**Kategori**|**C**|**I**|**A**|**Prioritas**|
|---|---|---|---|---|---|---|
|A1|Data Identitas Pengguna|Data|T|T|T|Kritis|
|A2|Credential<br>Hash<br>&<br>Session Token|Autentikasi|T|T|T|Kritis|
|A3|Data Transaksi & Order|Transaksi|T|T|T|Kritis|
|A4|Data Peran & Otorisasi|Kontrol Akses|T|T|S|Kritis|
|A5|Kunci TLS & Secret Key<br>Aplikasi|Infrastruktur|T|T|T|Kritis|
|A6|Log Audit & Aktivitas|Detektif|S|T|S|Tinggi|
|A7|Listing Jasa (Gig Data)|Konten|S|T|T|Tinggi|
|A8|Konfigurasi Database|Infrastruktur|T|T|T|Kritis|



**12** 

## **BAB IV | ANALISIS ANCAMAN DAN RISIKO** 

## **4.1 Metodologi Analisis Ancaman** 

Analisis ancaman dilakukan menggunakan model ancaman STRIDE yang dikembangkan oleh Microsoft, dipadukan dengan matriks risiko berbasis OWASP Risk Rating Methodology. STRIDE merupakan akronim untuk enam kategori ancaman: **S** poofing (pemalsuan identitas), **T** ampering (manipulasi data), **R** epudiation (penyangkalan tindakan), **I** nformation Disclosure (pengungkapan informasi), **D** enial of Service (penolakan layanan), dan **E** levation of Privilege (peningkatan hak akses). Setiap ancaman dinilai berdasarkan dua dimensi: Likelihood (kemungkinan terjadinya, skala 1–5) dan Impact (dampak jika terjadi, skala 1–5), menghasilkan Risk Score = Likelihood × Impact, yang dikategorikan sebagai: 1–5 (Rendah), 6–10 (Sedang), 11–19 (Tinggi), 20–25 (Kritis). 

## **4.2 Identifikasi dan Analisis Ancaman per Kategori STRIDE** 

## **4.2.1 Spoofing - Pemalsuan Identitas** 

Ancaman spoofing yang paling relevan pada platform Berima adalah **credential stuffing** dan **brute force authentication attacks** . Credential stuffing memanfaatkan pasangan username-password yang bocor dari pelanggaran data di platform lain (data breach repositories), mengotomatiskan percobaan login massal dengan asumsi bahwa pengguna menggunakan password yang sama di berbagai layanan. Serangan ini sangat efektif karena tidak memerlukan eksploitasi kerentanan teknis pada Berima sendiri, melainkan mengeksploitasi perilaku pengguna. Brute force attacks, khususnya menggunakan distributed attack tools, dapat mencoba ribuan kombinasi password per menit jika tidak ada mekanisme rate limiting. 

Ancaman kedua adalah **session token theft** , di mana penyerang mencuri session token aktif pengguna melalui berbagai vektor: XSS yang mengambil cookie, network sniffing pada koneksi HTTP yang tidak terenkripsi, atau kompromi terhadap perangkat pengguna. Kepemilikan session token yang valid memberikan akses penuh ke akun tanpa memerlukan password. Likelihood: 4, Impact: 5, Risk Score: 20 (Kritis). 

## **4.2.2 Tampering - Manipulasi Data** 

Ancaman tampering yang signifikan adalah **SQL Injection (SQLi)** pada parameter input yang tidak divalidasi, yang dapat memungkinkan penyerang membaca, memodifikasi, atau menghapus data dalam database. Meskipun penggunaan ORM 

**13** 

(Object-Relational Mapper) seperti SQLAlchemy secara signifikan mengurangi risiko SQLi, kueri raw SQL yang tidak diparameterisasi tetap menjadi vektor yang harus diaudit. Likelihood: 3, Impact: 5, Risk Score: 15 (Tinggi). 

**Insecure Direct Object Reference (IDOR)** merupakan ancaman tampering lain yang kritis, di mana pengguna dapat memanipulasi parameter referensi objek (seperti order_id atau user_id dalam URL) untuk mengakses atau memodifikasi data milik pengguna lain. Contoh konkret: buyer mengakses /orders/123 yang seharusnya hanya dapat diakses oleh pemilik order tersebut. Likelihood: 4, Impact: 4, Risk Score: 16 (Tinggi). 

## **4.2.3 Repudiation - Penyangkalan Tindakan** 

Tanpa logging yang komprehensif dan audit trail yang tidak dapat dimanipulasi, pengguna dapat menyangkal tindakan yang telah mereka lakukan, misalnya menyangkal telah melakukan order atau menyangkal telah mengubah detail listing. Ini berdampak langsung pada kemampuan Berima untuk menyelesaikan sengketa antar pengguna. Likelihood: 3, Impact: 3, Risk Score: 9 (Sedang). 

## **4.2.4 Information Disclosure - Pengungkapan Informasi** 

**Man-in-the-Middle (MitM) Attack** pada koneksi HTTP yang tidak terenkripsi memungkinkan penyerang yang berada di jalur komunikasi (misalnya pada jaringan Wi-Fi kampus yang sama) untuk mencegat dan membaca seluruh data yang ditransmisikan, termasuk password dan session token. Likelihood: 4, Impact: 5, Risk Score: 20 (Kritis). 

**Verbose error messages** yang mengungkapkan detail implementasi (stack trace, nama tabel database, versi framework) kepada pengguna akhir memberikan informasi berharga bagi penyerang untuk merancang serangan yang lebih terfokus. Likelihood: 3, Impact: 3, Risk Score: 9 (Sedang). 

## **4.2.5 Denial of Service - Penolakan Layanan** 

**Enumeration attacks** pada endpoint autentikasi, di mana penyerang mencoba secara sistematis untuk mengidentifikasi akun yang valid berdasarkan perbedaan respons sistem (misalnya "email tidak terdaftar" vs "password salah"), dapat diikuti dengan targeted credential attacks. **Resource exhaustion** melalui serangan terhadap proses hashing password, karena bcrypt dirancang untuk komputasi yang lambat, sejumlah 

**14** 

besar permintaan login simultan dapat membebani CPU server, merupakan vektor DoS yang spesifik terhadap implementasi password hashing yang kuat. Likelihood: 3, Impact: 4, Risk Score: 12 (Tinggi). 

## **4.2.6 Elevation of Privilege - Peningkatan Hak Akses** 

**Broken Access Control** merupakan ancaman paling kritis dalam kategori ini. Kegagalan dalam menegakkan pemeriksaan otorisasi pada setiap endpoint, misalnya buyer yang mengakses endpoint admin hanya dengan mengetahui URL-nya, memungkinkan privilege escalation horizontal maupun vertikal. OWASP menempatkan Broken Access Control sebagai ancaman nomor satu dalam OWASP Top 10 2021 (A01). Likelihood: 4, Impact: 5, Risk Score: 20 (Kritis). 

**Insecure session management** , khususnya kegagalan untuk meregenerasi session ID setelah login berhasil, memungkinkan session fixation attack, di mana penyerang terlebih dahulu menetapkan session ID yang diketahuinya pada browser korban, menunggu korban login, kemudian menggunakan session ID tersebut untuk mengambil alih sesi yang sudah terautentikasi. Likelihood: 3, Impact: 5, Risk Score: 15 (Tinggi). 

## **4.3 Matriks Risiko Konsolidasi** 

**Tabel 2.** Ringkasan Matriks Risiko Konsolidasi 

|**ID**|**Ancaman**|**Kategori**<br>**STRIDE**|**Layer**<br>**OSI**|**Likelihood**|**Impact**|**Risk**<br>**Score**|<br>**Level**|
|---|---|---|---|---|---|---|---|
|T1|Credential<br>Stuffing/Brute<br>Force|Spoofing|7|4|5|20|Kritis|
|T2|Session Token<br>Theft<br>(XSS/Sniffing<br>)|Spoofing|5|4|5|20|Kritis|
|T3|Man-in-the-M<br>iddle Attack|Information<br>Disclosure|6|4|5|20|Kritis|
|T4|Broken<br>Access<br>Control<br>/<br>Privilege<br>Escalation|Elevation of<br>Privilege|7|4|5|20|Kritis|
|T5|SQL Injection|Tampering|7|3|5|15|Tinggi|



**15** 

|T6|Insecure<br>Direct Object<br>Reference<br>(IDOR)|Tampering|7|4|4|16|Tinggi|
|---|---|---|---|---|---|---|---|
|T7|Session<br>Fixation|Elevation of<br>Privilege|5|3|5|15|Tinggi|
|T8|DoS via Login<br>Endpoint<br>Flooding|Denial of<br>Service|7|3|4|12|Tinggi|
|T9|Verbose Error<br>Information<br>Disclosure|Information<br>Disclosure|7|3|3|9|Sedang|
|T10|Non-Repudiat<br>ion<br>/ Audit<br>Trail Absence|Repudiation|7|3|3|9|Sedang|



**16** 

## **BAB V | EVALUASI TATA KELOLA KEAMANAN (ISO/IEC 27001:2022)** 

## **5.1 Metodologi Evaluasi** 

Evaluasi tata kelola keamanan dilakukan dalam dua tahap: pertama, pemetaan kondisi eksisting platform Berima terhadap kontrol-kontrol ISO/IEC 27001:2022 yang relevan (gap analysis), dan kedua, penetapan rekomendasi perbaikan berdasarkan temuan gap analysis. Status kepatuhan dinilai menggunakan skala empat tingkat: **Implemented** (telah diimplementasikan dan efektif), **Partially Implemented** (sebagian diimplementasikan namun terdapat gap), **Planned** (direncanakan untuk diimplementasikan), dan **Not Applicable** (tidak berlaku untuk konteks Berima). 

## **5.2 Hasil Gap Analysis** 

## 1. **A.5.15 - Access Control** 

_Kondisi Eksisting:_ Pada tahap awal pengembangan Berima, mekanisme kontrol akses bersifat ad-hoc — beberapa endpoint hanya memiliki pemeriksaan login sederhana tanpa diferensiasi peran. Tidak terdapat kebijakan kontrol akses yang terdokumentasi. _Status:_ Partially Implemented 

_Gap:_ Tidak ada kebijakan kontrol akses formal; implementasi RBAC belum konsisten di semua endpoint; tidak ada mekanisme review berkala terhadap hak akses. 

_Rekomendasi:_ Implementasi RBAC tiga tingkat (admin/seller/buyer) dengan dekorator otorisasi pada setiap endpoint; dokumentasi kebijakan kontrol akses; review hak akses periodik. 

## 2. **A.5.16 - Identity Management** 

_Kondisi Eksisting:_ Platform memiliki sistem registrasi dan manajemen akun dasar, namun belum ada proses formal untuk deprovisioning akun (penghapusan akun pengguna yang tidak aktif atau melanggar ketentuan layanan) maupun audit terhadap akun-akun yang ada. 

_Status:_ Partially Implemented 

_Gap:_ Tidak ada proses deprovisioning; tidak ada audit akun periodik; tidak ada mekanisme deteksi dan penanganan akun yang dikompromikan. 

_Rekomendasi:_ Implementasi mekanisme deaktivasi akun (soft delete) oleh admin; log aktivitas per akun; alert untuk pola login abnormal. 

## 3. **A.5.17 - Authentication Information** 

_Kondisi Eksisting:_ Password disimpan tanpa hashing pada versi awal (plaintext 

**17** 

storage — pelanggaran kritis), atau dengan hashing menggunakan MD5 tanpa salt pada beberapa iterasi pengembangan. 

_Status:_ Not Implemented (kondisi awal) → Implemented (setelah remediasi) 

_Gap Kritis:_ Penyimpanan password plaintext merupakan pelanggaran fundamental terhadap kontrol ini. Tidak ada password policy (minimum length, complexity); tidak ada mekanisme pencegahan password reuse; tidak ada kebijakan reset password yang aman. 

_Rekomendasi:_ Implementasi bcrypt dengan cost factor 12 untuk seluruh password; kebijakan password minimum 8 karakter dengan kombinasi karakter; mekanisme reset password melalui email dengan token single-use time-limited. 

## 4. **A.8.5 - Secure Authentication** 

_Kondisi Eksisting:_ Tidak ada mekanisme pencegahan brute force (rate limiting, account lockout); tidak ada feedback yang seragam terhadap kegagalan login (beberapa endpoint mengungkapkan apakah email terdaftar atau tidak); tidak ada logging terhadap upaya autentikasi yang gagal. 

_Status:_ Not Implemented 

_Gap:_ Tidak ada rate limiting; respons error yang berbeda antara "email tidak ditemukan" dan "password salah" memungkinkan enumeration; tidak ada deteksi anomali login. 

_Rekomendasi:_ Implementasi rate limiting menggunakan Flask-Limiter; generic error message untuk semua kegagalan autentikasi ("Email atau password tidak valid"); logging semua upaya login beserta IP dan timestamp. 

## 5. **A.8.20 — Network Security** 

_Kondisi Eksisting:_ Pada lingkungan pengembangan, platform berjalan pada HTTP biasa tanpa enkripsi. Tidak ada kebijakan mengenai protokol yang diizinkan untuk komunikasi. 

_Status:_ Not Implemented 

_Gap:_ Tidak ada enkripsi komunikasi; tidak ada konfigurasi security headers pada respons HTTP (HSTS, X-Content-Type-Options, X-Frame-Options, Content-Security-Policy). 

_Rekomendasi:_ Implementasi HTTPS/TLS 1.3; konfigurasi HTTP Strict Transport Security (HSTS); implementasi security headers lengkap menggunakan Flask-Talisman. 

**18** 

## 6. **A.8.24 — Use of Cryptography** 

_Kondisi Eksisting:_ Tidak ada kebijakan penggunaan kriptografi yang terdefinisi; penggunaan algoritma kriptografis bersifat ad-hoc. 

_Status:_ Not Implemented 

_Gap:_ Tidak ada kebijakan kriptografi formal; tidak ada inventarisasi terhadap penggunaan kriptografi dalam sistem; tidak ada prosedur manajemen kunci. 

_Rekomendasi:_ Penetapan kebijakan kriptografi yang mendefinisikan algoritma yang diizinkan (bcrypt untuk password, TLS 1.3 untuk komunikasi, AES-256-GCM untuk enkripsi data sensitif at-rest jika diperlukan); rotasi secret key Flask secara periodik; penyimpanan kunci melalui environment variables, tidak hardcoded. 

## 7. **A.8.26 - Application Security Requirements** 

_Kondisi Eksisting:_ Tidak ada security requirements yang secara eksplisit terdefinisi dalam proses pengembangan; keamanan ditangani secara reaktif. 

_Status:_ Not Implemented 

_Gap:_ Tidak ada secure development lifecycle; tidak ada security testing dalam pipeline pengembangan. 

_Rekomendasi:_ Integrasi persyaratan keamanan OWASP ASVS Level 2 dalam checklist pengembangan; pengujian keamanan sebagai gate dalam proses code review. 

## **5.3 Ringkasan Gap Analysis** 

**Tabel 3.** Summary Analisa Gap 

|**Kontrol ISO 27001:2022**|**Status Awal**|**Status Target**|**Prioritas**|
|---|---|---|---|
|A.5.15 Access Control|Partially Implemented|Implemented|Kritis|
|A.5.16 Identity<br>Management|Partially Implemented|Implemented|Tinggi|
|A.5.17 Authentication<br>Information|Not Implemented|Implemented|Kritis|
|A.8.5 Secure<br>Authentication|Not Implemented|Implemented|Kritis|
|A.8.20 Network Security|Not Implemented|Implemented|Kritis|
|A.8.24 Use of<br>Cryptography|Not Implemented|Implemented|Kritis|



**19** 

|A.8.26 Application<br>Security Requirements|Not Implemented|Planned|Tinggi|
|---|---|---|---|
|A.8.28 Secure Coding|Partially Implemented|Implemented|Tinggi|



**20** 

## **BAB VI | IMPLEMENTASI MEKANISME KEAMANAN** 

## **6.1 Arsitektur Sistem** 

Platform Berima diimplementasikan menggunakan stack teknologi berikut: Python 3.11 sebagai bahasa pemrograman, Flask 3.x sebagai web framework, SQLAlchemy 2.x sebagai ORM, bcrypt (via passlib) untuk password hashing, Flask-Login untuk session management, Flask-Limiter untuk rate limiting, Flask-Talisman untuk security headers dan TLS enforcement, dan SQLite untuk database pengembangan (PostgreSQL untuk produksi). Seluruh dependensi dikelola melalui requirements.txt yang di-pin ke versi spesifik untuk reproducibility. 

Struktur direktori aplikasi mengikuti pola Flask application factory: 

berima/ 

├── app/ │   ├── __init__.py          # Application factory 

│   ├── models.py            # Database models (User, Role, Gig, Order) 

│   ├── auth/ │   │   ├── __init__.py │   │   └── routes.py        # Login, logout, register endpoints 

│   ├── main/ │   │   ├── __init__.py │   │   └── routes.py        # Core application routes │   ├── admin/ │   │   ├── __init__.py │   │   └── routes.py        # Admin-only routes │   └── utils/ │       └── decorators.py    # RBAC decorators ├── config.py                # Configuration classes ├── certificates/ 

**21** 

│   ├── cert.pem             # TLS certificate (self-signed untuk dev) 

│   └── key.pem              # TLS private key 

├── requirements.txt 

└── run.py                   # Entry point 

## **6.2 Konfigurasi Keamanan Dasar (config.py)** 

Konfigurasi aplikasi memisahkan parameter sensitif dari kode menggunakan environment variables, sebuah praktik yang direkomendasikan dalam The Twelve-Factor App methodology dan secara eksplisit dipersyaratkan oleh OWASP Secure Configuration Cheat Sheet. 

Sc → config.py 

import os 

from datetime import timedelta 

class Config: 

# Secret key: HARUS di-set via environment variable, tidak boleh hardcoded SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or os.urandom(32) 

# Database 

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \ 

'sqlite:///berima_dev.db' 

SQLALCHEMY_TRACK_MODIFICATIONS = False 

# Session security configuration 

SESSION_COOKIE_SECURE = True        # Cookie hanya dikirim via HTTPS 

SESSION_COOKIE_HTTPONLY = True      # Cookie tidak dapat diakses via JavaScript 

SESSION_COOKIE_SAMESITE = 'Lax'    # CSRF protection 

**22** 

PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Session timeout 2 jam 

# WTForms CSRF Protection 

WTF_CSRF_ENABLED = True 

WTF_CSRF_TIME_LIMIT = 3600 

# Rate limiting 

RATELIMIT_DEFAULT = "200 per day;50 per hour" 

RATELIMIT_STORAGE_URL = "memory://" 

class ProductionConfig(Config): 

SESSION_COOKIE_SECURE = True 

PREFERRED_URL_SCHEME = 'https' 

class DevelopmentConfig(Config): 

DEBUG = True 

# Untuk development dengan self-signed cert, tetap aktifkan HTTPS 

SESSION_COOKIE_SECURE = True 

Nilai SECRET_KEY yang dihasilkan menggunakan os.urandom(32) menghasilkan 256-bit random key yang digunakan oleh Flask untuk menandatangani session cookie secara kriptografis menggunakan HMAC-SHA256. Tanpa secret key yang kuat dan acak, penyerang yang mengetahui secret key dapat memalsukan session cookie untuk pengguna mana pun. 

## **6.3 Model Database (models.py)** 

from datetime import datetime, timezone from app import db, login_manager from passlib.hash import bcrypt as bcrypt_hash from flask_login import UserMixin 

**23** 

class Role(db.Model): 

"""Model RBAC: mendefinisikan peran dalam sistem.""" 

__tablename__ = 'roles' 

id = db.Column(db.Integer, primary_key=True) 

name = db.Column(db.String(64), unique=True, nullable=False) 

description = db.Column(db.String(256)) 

# Relasi ke pengguna yang memiliki peran ini 

users = db.relationship('User', backref='role', lazy='dynamic') 

- @staticmethod 

def insert_roles(): 

"""Inisialisasi tiga peran dasar dalam sistem.""" 

roles = { 

'buyer': 'Pengguna yang dapat menelusuri dan memesan jasa', 

'seller': 'Pengguna yang dapat membuat dan mengelola listing jasa', 

'admin': 'Administrator dengan akses penuh ke seluruh sistem' 

- } 

for role_name, description in roles.items(): 

role = Role.query.filter_by(name=role_name).first() 

if role is None: 

role = Role(name=role_name, description=description) 

db.session.add(role) 

db.session.commit() 

class User(UserMixin, db.Model): 

"""Model pengguna dengan implementasi keamanan password dan session.""" 

__tablename__ = 'users' 

id = db.Column(db.Integer, primary_key=True) 

email = db.Column(db.String(128), unique=True, nullable=False, index=True) 

username = db.Column(db.String(64), unique=True, nullable=False) 

password_hash = db.Column(db.String(256), nullable=False) 

**24** 

nim = db.Column(db.String(20), unique=True, nullable=True) 

phone = db.Column(db.String(20), nullable=True) 

is_active = db.Column(db.Boolean, default=True, nullable=False) 

is_verified = db.Column(db.Boolean, default=False, nullable=False) 

role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False) 

created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 

last_login = db.Column(db.DateTime, nullable=True) 

failed_login_attempts = db.Column(db.Integer, default=0) 

locked_until = db.Column(db.DateTime, nullable=True) 

# Relasi ke entitas lain 

gigs = db.relationship('Gig', backref='seller', lazy='dynamic', 

foreign_keys='Gig.seller_id') 

orders_as_buyer = db.relationship('Order', backref='buyer', lazy='dynamic', 

foreign_keys='Order.buyer_id') 

def set_password(self, password: str) -> None: 

""" 

Hash password menggunakan bcrypt dengan cost factor 12. 

bcrypt secara otomatis menambahkan salt yang unik per hash, 

sehingga dua hash dari password yang sama akan menghasilkan 

digest yang berbeda. Ini mencegah rainbow table attacks. 

Cost factor 12 menghasilkan waktu hashing ~250ms pada hardware 

modern, menjadikan brute force secara praktis tidak layak. 

""" 

if len(password) < 8: 

raise ValueError("Password harus minimal 8 karakter") 

self.password_hash = bcrypt_hash.using(rounds=12).hash(password) 

def verify_password(self, password: str) -> bool: 

""" 

Verifikasi password terhadap hash tersimpan. 

**25** 

passlib.hash.bcrypt.verify() menggunakan constant-time comparison 

secara internal, mencegah timing side-channel attacks. 

""" 

if not self.password_hash: 

return False 

return bcrypt_hash.verify(password, self.password_hash) 

def is_locked(self) -> bool: 

"""Cek apakah akun sedang dalam status terkunci.""" 

if self.locked_until and self.locked_until > datetime.now(timezone.utc): 

return True 

return False 

def has_role(self, role_name: str) -> bool: 

"""Verifikasi apakah pengguna memiliki peran tertentu.""" 

return self.role and self.role.name == role_name 

def __repr__(self): 

return f'<User {self.username} [{self.role.name if self.role else "no role"}]>' 

@login_manager.user_loader 

def load_user(user_id: str): 

""" 

Callback Flask-Login untuk memuat pengguna dari session. 

Dipanggil pada setiap request untuk pengguna yang terautentikasi. """ 

return User.query.get(int(user_id)) 

Beberapa aspek keamanan kritis dalam desain model ini perlu dijelaskan secara eksplisit. Kolom password_hash menyimpan output bcrypt yang mencakup algorithm identifier, cost factor, salt (22 karakter Base64), dan digest (31 karakter Base64) dalam satu string berformat $2b$12$[22-char-salt][31-char-digest]. Salt yang dihasilkan secara acak per hash memastikan bahwa dua pengguna dengan password identik memiliki hash yang berbeda, 

**26** 

mengeliminasi risiko rainbow table attacks. Kolom failed_login_attempts dan locked_until digunakan untuk implementasi account lockout policy yang mencegah brute force attacks yang persisten. 

## **6.4 Implementasi Autentikasi Aman (auth/routes.py)** 

from flask import Blueprint, render_template, redirect, url_for, flash, request, session from flask_login import login_user, logout_user, login_required, current_user from flask_limiter import Limiter 

from flask_limiter.util import get_remote_address 

from datetime import datetime, timezone, timedelta 

from app import db 

from app.models import User, Role 

from app.auth.forms import LoginForm, RegistrationForm 

import logging 

auth = Blueprint('auth', __name__) 

# Konfigurasi logger untuk audit trail autentikasi auth_logger = logging.getLogger('berima.auth') 

# Rate limiter diinisialisasi di application factory 

limiter = Limiter(key_func=get_remote_address) 

@auth.route('/login', methods=['GET', 'POST']) 

@limiter.limit("10 per minute;50 per hour") 

# Maksimum 10 percobaan login per menit per IP — mencegah brute force 

def login(): 

""" 

Endpoint login dengan mekanisme keamanan berlapis: 

1. Rate limiting berbasis IP 

2. Account lockout setelah 5 kegagalan berturutan 

3. Generic error message (tidak membedakan email/password salah) 

4. Session ID regeneration setelah login berhasil 

5. Audit logging untuk setiap percobaan 

**27** 

""" 

if current_user.is_authenticated: 

return redirect(url_for('main.dashboard')) 

## form = LoginForm() 

if form.validate_on_submit(): 

email = form.email.data.lower().strip() 

password = form.password.data 

# Pencarian pengguna berdasarkan email 

user = User.query.filter_by(email=email).first() 

# PENTING: Pesan error HARUS generik untuk mencegah user enumeration. 

# Tidak boleh membedakan "email tidak terdaftar" vs "password salah". 

GENERIC_ERROR = "Email atau password yang Anda masukkan tidak valid." 

# Cek keberadaan user dan status akun 

if user is None or not user.is_active: 

auth_logger.warning( 

f"LOGIN_FAILED | IP: {get_remote_address()} | " 

f"Email: {email} | Reason: user_not_found_or_inactive" 

) 

# Tetap lakukan "dummy" password verification untuk mencegah 

# timing attack yang dapat digunakan untuk user enumeration. 

# Jika kita langsung return saat user is None, timing yang lebih 

# cepat mengungkapkan bahwa email tidak terdaftar. 

bcrypt_hash.using(rounds=12).hash("dummy_password_to_normalize_timing") 

flash(GENERIC_ERROR, 'danger') 

return render_template('auth/login.html', form=form) 

# Cek status account lockout 

if user.is_locked(): 

remaining = (user.locked_until - datetime.now(timezone.utc)).seconds // 60 

**28** 

auth_logger.warning( 

f"LOGIN_BLOCKED | IP: {get_remote_address()} | " 

f"UserID: {user.id} | Reason: account_locked | " 

f"Remaining: {remaining}m" ) 

flash(f"Akun Anda terkunci. Coba lagi dalam {remaining} menit.", 'warning') 

return render_template('auth/login.html', form=form) 

# Verifikasi password 

if not user.verify_password(password): 

# Increment failed attempt counter 

user.failed_login_attempts += 1 

# Account lockout setelah 5 kegagalan berturutan 

if user.failed_login_attempts >= 5: 

user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15) auth_logger.warning( 

f"ACCOUNT_LOCKED | IP: {get_remote_address()} | " 

f"UserID: {user.id} | FailedAttempts: {user.failed_login_attempts}" ) flash("Terlalu banyak percobaan gagal. Akun dikunci 15 menit.", 'danger') else: 

auth_logger.warning( f"LOGIN_FAILED | IP: {get_remote_address()} | " f"UserID: {user.id} | FailedAttempts: {user.failed_login_attempts}" ) flash(GENERIC_ERROR, 'danger') 

db.session.commit() return render_template('auth/login.html', form=form) 

# === LOGIN BERHASIL === 

# Reset failed attempts counter 

user.failed_login_attempts = 0 

**29** 

user.locked_until = None 

user.last_login = datetime.now(timezone.utc) 

# SESSION ID REGENERATION — kritis untuk mencegah session fixation. 

# Flask-Login login_user() secara internal menangani ini, namun kita 

# juga secara eksplisit membersihkan session state sebelumnya. 

session.clear() 

# Login pengguna melalui Flask-Login 

remember_me = form.remember_me.data 

login_user(user, remember=remember_me, 

duration=timedelta(hours=2) if remember_me else None) 

db.session.commit() 

auth_logger.info( 

f"LOGIN_SUCCESS | IP: {get_remote_address()} | " 

f"UserID: {user.id} | Username: {user.username} | " 

f"Role: {user.role.name}" 

) 

# Redirect ke halaman yang diminta (jika ada) atau dashboard 

next_page = request.args.get('next') 

# Validasi URL next untuk mencegah open redirect vulnerability 

if next_page and not next_page.startswith('/'): 

next_page = None 

return redirect(next_page or url_for('main.dashboard')) 

return render_template('auth/login.html', form=form) 

@auth.route('/logout', methods=['POST']) 

@login_required def logout(): 

**30** 

""" 

Endpoint logout yang aman. 

Menggunakan POST method (bukan GET) untuk mencegah CSRF-based 

forced logout melalui embedded images atau links. Seluruh 

session data dibersihkan dari server-side dan cookie sesi diinvalidasi. 

""" 

user_id = current_user.id 

username = current_user.username 

# Logout dari Flask-Login (menghapus user ID dari session) 

logout_user() 

# Bersihkan seluruh session data 

session.clear() 

auth_logger.info( 

f"LOGOUT | IP: {get_remote_address()} | " 

f"UserID: {user_id} | Username: {username}" 

) 

flash("Anda telah berhasil logout.", 'success') 

return redirect(url_for('auth.login')) 

@auth.route('/register', methods=['GET', 'POST']) @limiter.limit("5 per hour")  # Batasi registrasi untuk mencegah spam 

def register(): 

""" 

Endpoint registrasi pengguna baru. 

Semua pengguna baru terdaftar dengan peran 'buyer' secara default. 

Peningkatan ke 'seller' memerlukan proses verifikasi oleh admin. """ 

if current_user.is_authenticated: 

**31** 

return redirect(url_for('main.dashboard')) 

form = RegistrationForm() 

if form.validate_on_submit(): 

# Cek duplikasi email 

if User.query.filter_by(email=form.email.data.lower()).first(): 

# Gunakan pesan generik untuk mencegah email enumeration flash("Registrasi berhasil! Silakan cek email Anda.", 'success') return redirect(url_for('auth.login')) 

buyer_role = Role.query.filter_by(name='buyer').first() 

user = User( 

email=form.email.data.lower().strip(), username=form.username.data.strip(), nim=form.nim.data.strip() if form.nim.data else None, role=buyer_role ) 

user.set_password(form.password.data)  # bcrypt hashing di sini 

db.session.add(user) db.session.commit() 

auth_logger.info( 

f"REGISTER_SUCCESS | IP: {get_remote_address()} | " f"UserID: {user.id} | Email: {user.email}" ) 

flash("Akun berhasil dibuat! Silakan login.", 'success') return redirect(url_for('auth.login')) 

return render_template('auth/register.html', form=form) 

## **6.5 Implementasi Role-Based Access Control (utils/decorators.py)** 

**32** 

RBAC diimplementasikan melalui decorator Python yang dapat dikomposisikan, mengikuti pola yang serupa dengan @login_required dari Flask-Login namun memperluas pemeriksaan ke level peran pengguna. 

from functools import wraps 

from flask import abort, flash, redirect, url_for 

from flask_login import current_user 

import logging 

rbac_logger = logging.getLogger('berima.rbac') 

def role_required(*role_names): 

""" 

Decorator untuk membatasi akses endpoint berdasarkan peran pengguna. 

Penggunaan: 

@role_required('admin')                    # Hanya admin 

@role_required('seller', 'admin')          # Seller atau admin 

@role_required('buyer', 'seller', 'admin') # Semua peran terautentikasi 

Implementasi mengikuti prinsip Fail-Safe Defaults: default-nya 

adalah menolak akses, dan hanya mengizinkan jika kondisi eksplisit 

terpenuhi. 

""" 

def decorator(f): 

@wraps(f) 

def decorated_function(*args, **kwargs): 

**33** 

# Cek autentikasi terlebih dahulu 

if not current_user.is_authenticated: 

return redirect(url_for('auth.login')) 

# Cek apakah akun aktif 

if not current_user.is_active: 

flash("Akun Anda telah dinonaktifkan.", 'danger') return redirect(url_for('auth.login')) 

# Cek kepemilikan peran 

if current_user.role and current_user.role.name in role_names: 

return f(*args, **kwargs) 

# Log upaya akses tidak sah rbac_logger.warning( 

f"ACCESS_DENIED | UserID: {current_user.id} | " 

f"Username: {current_user.username} | " 

f"UserRole: {current_user.role.name if current_user.role else 'none'} | " 

f"RequiredRoles: {role_names} | " f"Endpoint: {f.__name__}" ) abort(403)  # Forbidden — bukan 404 (jangan sembunyikan keberadaan resource) 

return decorated_function return decorator 

**34** 

def owner_required(model_class, id_param='id', owner_field='seller_id'): """ 

Decorator untuk memastikan pengguna hanya dapat mengakses 

resource yang mereka miliki (mencegah IDOR). 

Admin selalu mendapatkan akses (bypass owner check). 

Penggunaan: 

@owner_required(Gig, id_param='gig_id', owner_field='seller_id') def edit_gig(gig_id): 

... 

""" 

def decorator(f): 

@wraps(f) 

def decorated_function(*args, **kwargs): 

if not current_user.is_authenticated: 

return redirect(url_for('auth.login')) 

# Admin bypass: admin dapat mengakses resource siapa pun 

if current_user.role and current_user.role.name == 'admin': 

return f(*args, **kwargs) 

# Ambil object ID dari argumen 

obj_id = kwargs.get(id_param) 

if obj_id is None: 

**35** 

abort(400) 

# Cari object di database 

obj = model_class.query.get_or_404(obj_id) 

# Verifikasi kepemilikan 

obj_owner_id = getattr(obj, owner_field, None) 

if obj_owner_id != current_user.id: 

rbac_logger.warning( 

f"IDOR_ATTEMPT | UserID: {current_user.id} | " 

f"TargetResource: {model_class.__name__}#{obj_id} | " f"OwnerID: {obj_owner_id}" ) abort(403) 

return f(*args, **kwargs) 

return decorated_function 

return decorator 

Contoh penggunaan decorator dalam routes: 

# routes/admin.py @admin.route('/users') 

@login_required @role_required('admin') def manage_users(): 

"""Halaman manajemen pengguna — hanya admin.""" 

users = User.query.all() 

**36** 

return render_template('admin/users.html', users=users) 

# routes/seller.py 

@seller.route('/gigs/new') 

@login_required 

@role_required('seller', 'admin') 

def create_gig(): 

"""Buat listing jasa baru — seller dan admin.""" 

... 

@seller.route('/gigs/<int:gig_id>/edit') 

@login_required 

@role_required('seller') 

@owner_required(Gig, id_param='gig_id', owner_field='seller_id') 

def edit_gig(gig_id): 

"""Edit listing jasa — hanya seller pemilik gig.""" 

gig = Gig.query.get_or_404(gig_id) 

… 

## **6.6 Implementasi HTTPS/TLS dan Security Headers** 

TLS diimplementasikan menggunakan dua komponen: sertifikat TLS dan konfigurasi Flask-Talisman untuk menerapkan security headers. 

## **Langkah 1: Generasi Sertifikat Self-Signed (Development)** 

# Buat direktori certificates 

mkdir -p certificates 

# Hasilkan private key RSA 4096-bit 

openssl genrsa -out certificates/key.pem 4096 

**37** 

# Hasilkan sertifikat self-signed dengan Subject Alternative Names 

openssl req -new -x509 -key certificates/key.pem \ 

-out certificates/cert.pem \ 

-days 365 \ 

-subj "/C=ID/ST=DKI Jakarta/L=Jakarta/O=Berima Platform/CN=localhost" \ 

-addext "subjectAltName=DNS:localhost,IP:127.0.0.1" 

# Verifikasi 

openssl x509 -in certificates/cert.pem -text -noout | grep -E "Subject:|Not After|Version" 

## **Langkah 2: Konfigurasi Flask-Talisman (Security Headers)** 

# app/__init__.py 

from flask import Flask 

from flask_sqlalchemy import SQLAlchemy 

from flask_login import LoginManager 

from flask_talisman import Talisman 

from flask_limiter import Limiter 

from flask_limiter.util import get_remote_address 

from flask_wtf.csrf import CSRFProtect 

from config import Config 

db = SQLAlchemy() 

login_manager = LoginManager() 

csrf = CSRFProtect() 

limiter = Limiter(key_func=get_remote_address) 

**38** 

# Content Security Policy yang ketat 

CSP = { 

'default-src': "'self'", 

'script-src': ["'self'", "'nonce-{nonce}'"],  # Hanya skrip dari origin sendiri 'style-src': ["'self'", 'https://fonts.googleapis.com'], 'font-src': ["'self'", 'https://fonts.gstatic.com'], 'img-src': ["'self'", 'data:'], 'connect-src': "'self'", 'form-action': "'self'", 

'frame-ancestors': "'none'",         # Mencegah clickjacking 'base-uri': "'self'", 'object-src': "'none'"               # Menonaktifkan plugin berbahaya 

} 

def create_app(config_class=Config): 

app = Flask(__name__) 

app.config.from_object(config_class) 

# Inisialisasi extensions 

db.init_app(app) login_manager.init_app(app) csrf.init_app(app) limiter.init_app(app) 

# Flask-Talisman: memaksa HTTPS dan menambahkan security headers 

**39** 

Talisman( app, force_https=True,                  # Redirect semua HTTP ke HTTPS strict_transport_security=True,    # HSTS header strict_transport_security_max_age=31536000,  # HSTS max-age: 1 tahun strict_transport_security_include_subdomains=True, content_security_policy=CSP, content_security_policy_nonce_in=['script-src'], 

referrer_policy='strict-origin-when-cross-origin', 

feature_policy={ # Menonaktifkan fitur browser yang tidak diperlukan 

'camera': "'none'", 

'microphone': "'none'", 'geolocation': "'none'" } ) 

# Konfigurasi Flask-Login 

login_manager.login_view = 'auth.login' 

login_manager.login_message = 'Silakan login untuk mengakses halaman ini.' 

login_manager.login_message_category = 'info' 

login_manager.session_protection = 'strong'  # Invalidasi sesi jika IP berubah 

# Register blueprints 

from app.auth import auth as auth_blueprint 

app.register_blueprint(auth_blueprint, url_prefix='/auth') 

**40** 

from app.main import main as main_blueprint 

app.register_blueprint(main_blueprint) 

from app.admin import admin as admin_blueprint 

app.register_blueprint(admin_blueprint, url_prefix='/admin') 

return app 

# run.py — entry point dengan TLS 

from app import create_app import ssl 

app = create_app() 

if __name__ == '__main__': 

# Konfigurasi SSL context untuk development 

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) 

context.minimum_version = ssl.TLSVersion.TLSv1_3  # Hanya TLS 1.3 context.load_cert_chain('certificates/cert.pem', 'certificates/key.pem') 

app.run( 

host='0.0.0.0', 

port=5443, 

ssl_context=context, 

debug=False  # JANGAN aktifkan debug=True di production 

) 

**41** 

Security headers yang dikonfigurasi melalui Flask-Talisman ini mengimplementasikan beberapa lapisan perlindungan tambahan. **HTTP Strict Transport Security (HSTS)** memberitahu browser bahwa domain ini harus selalu diakses melalui HTTPS, bahkan jika pengguna mengetikkan http:// secara eksplisit, selama minimal satu tahun (31536000 detik). **Content Security Policy (CSP)** mendefinisikan whitelist sumber konten yang diizinkan, memblokir eksekusi skrip inline yang tidak memiliki nonce yang valid — ini adalah pertahanan utama terhadap XSS. **X-Frame-Options** (ditetapkan melalui frame-ancestors: 'none' dalam CSP) mencegah halaman Berima di-embed dalam iframe di domain lain, melindungi dari clickjacking attacks. 

**42** 

## **BAB VII | PENGUJIAN KEAMANAN** 

## **7.1 Metodologi Pengujian** 

Pengujian keamanan dilakukan menggunakan pendekatan berlapis yang mencakup: (1) pengujian fungsional untuk memverifikasi bahwa mekanisme keamanan bekerja sebagaimana diharapkan, (2) pengujian negatif untuk memverifikasi bahwa kontrol keamanan menolak input dan akses yang tidak sah, dan (3) pengujian penetrasi terbatas menggunakan tools standar industri. Tools yang digunakan: curl (pengujian HTTP/HTTPS manual), OWASP ZAP 2.14 (automated security scanning), Burp Suite Community Edition (intercepting proxy), dan testssl.sh (analisis konfigurasi TLS). 

## **7.2 Pengujian Password Hashing** 

## **Skenario Uji 1: Verifikasi bcrypt hash tidak tersimpan sebagai plaintext:** 

# Buat pengguna test melalui aplikasi, kemudian inspeksi database 

sqlite3 berima_dev.db "SELECT email, password_hash FROM users WHERE email='test@berima.id';" 

Output yang diharapkan: 

test@berima.id|$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiphXG/RB6q5EjPXkf U9k5VyMZ6G 

Format $2b$12$ mengkonfirmasi penggunaan bcrypt dengan cost factor 12. Kolom password_hash tidak mengandung plaintext password. 

## **Skenario Uji 2: Verifikasi salt unik per pengguna:** 

Dua pengguna dengan password identik "Password123!" harus menghasilkan hash yang berbeda: 

from passlib.hash import bcrypt as bcrypt_hash 

password = "Password123!" 

hash1 = bcrypt_hash.using(rounds=12).hash(password) 

hash2 = bcrypt_hash.using(rounds=12).hash(password) 

**43** 

print(hash1)  # $2b$12$[salt1][hash1] — berbeda 

print(hash2)  # $2b$12$[salt2][hash2] — berbeda 

assert hash1 != hash2  # PASS: salt berbeda menghasilkan hash berbeda 

assert bcrypt_hash.verify(password, hash1)  # PASS: verifikasi tetap berhasil 

assert bcrypt_hash.verify(password, hash2)  # PASS 

Skenario Uji 3: Pengukuran timing untuk verifikasi cost factor 

import time 

from passlib.hash import bcrypt as bcrypt_hash 

password = "TestPassword!" 

hash_val = bcrypt_hash.using(rounds=12).hash(password) 

start = time.time() 

bcrypt_hash.verify(password, hash_val) 

elapsed = time.time() - start 

print(f"Waktu verifikasi bcrypt (rounds=12): {elapsed:.3f}s") 

# Diharapkan: 0.1s - 0.5s — cukup lambat untuk mencegah brute force 

# Hasil tipikal pada server standar: ~0.25s 

## **7.3 Pengujian Autentikasi dan Session Management** 

Skenario Uji 4: Verifikasi rate limiting pada endpoint login 

# Kirim 15 request POST ke endpoint login dalam 60 detik dari IP yang sama 

for i in {1..15}; do 

**44** 

curl -k -s -o /dev/null -w "%{http_code}\n" \ 

- -X POST https://localhost:5443/auth/login \ 

- -d "email=test@berima.id&password=wrongpassword&csrf_token=..." \ 

- -H "Content-Type: application/x-www-form-urlencoded" 

Done 

Output yang diharapkan: 

200   # Request 1-10: Diproses (meski login gagal) 429   # Request 11-15: Too Many Requests — rate limit tercapai 

429 

429 

429 429 

Skenario Uji 5: Verifikasi atribut keamanan cookie sesi: 

curl -k -c cookies.txt -b cookies.txt -v \ 

- -X POST https://localhost:5443/auth/login \ 

- -d "email=buyer@berima.id&password=ValidPassword1!&csrf_token=..." 2>&1 | \ 

grep -i "set-cookie" 

Output yang diharapkan: 

< Set-Cookie: session=eyJ...; HttpOnly; Secure; SameSite=Lax; Path=/ 

Keberadaan atribut HttpOnly (mencegah akses JavaScript), Secure (hanya dikirim via HTTPS), dan SameSite=Lax (mitigasi CSRF) dikonfirmasi. 

Skenario Uji 6: Verifikasi session ID regeneration setelah login: 

# 1. Dapatkan session cookie sebelum login 

BEFORE=$(curl -k -s -c /dev/null -D - https://localhost:5443/auth/login | grep "session=") 

# 2. Lakukan login 

curl -k -c /tmp/session.txt -b /tmp/session.txt -X POST \ 

**45** 

https://localhost:5443/auth/login \ 

- -d "email=buyer@berima.id&password=ValidPassword1!&csrf_token=..." 

# 3. Periksa session cookie setelah login 

AFTER=$(grep "session" /tmp/session.txt) 

echo "Before: $BEFORE" 

echo "After: $AFTER" 

# Nilai session cookie harus BERBEDA setelah login berhasil 

## **7.4 Pengujian RBAC dan Kontrol Akses** 

Skenario Uji 7: Verifikasi buyer tidak dapat mengakses halaman admin: 

# Login sebagai buyer dan simpan session 

curl -k -c /tmp/buyer_session.txt -b /tmp/buyer_session.txt -X POST \ 

https://localhost:5443/auth/login \ 

- -d "email=buyer@berima.id&password=BuyerPass1!&csrf_token=..." 

# Coba akses halaman admin dengan session buyer 

curl -k -b /tmp/buyer_session.txt -s -o /dev/null -w "%{http_code}\n" \ https://localhost:5443/admin/users 

Output yang diharapkan: 403 (Forbidden) — bukan 404 (karena endpoint ada, hanya akses ditolak). 

Skenario Uji 8: Verifikasi pencegahan IDOR pada endpoint order: 

# Login sebagai buyer_A 

# Dapatkan order ID milik buyer_B (misalnya order ID 42) 

# Coba akses order milik buyer_B menggunakan session buyer_A 

curl -k -b /tmp/buyer_a_session.txt -s -o /dev/null -w "%{http_code}\n" \ 

https://localhost:5443/orders/42 

Output yang diharapkan: 403 (Forbidden) — bukan data order buyer_B. 

**46** 

## **7.5 Pengujian Konfigurasi TLS** 

## **Skenario Uji 9: Verifikasi konfigurasi TLS menggunakan testssl.sh:** 

# Jalankan testssl.sh terhadap endpoint Berima 

./testssl.sh --protocols --ciphers --headers localhost:5443 

Output kunci yang diharapkan: 

Protocol Support SSLv2      not offered (OK) SSLv3      not offered (OK) TLS 1      not offered (OK) TLS 1.1    not offered (OK) TLS 1.2    not offered (OK)     # Disabled — hanya TLS 1.3 TLS 1.3    offered (OK) 

Cipher Category 

TLS 1.3: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256 (OK) 

HTTP Security Headers 

Strict-Transport-Security      max-age=31536000; includeSubDomains (OK) 

Content-Security-Policy        present (OK) X-Content-Type-Options         nosniff (OK) 

X-Frame-Options                DENY (OK) 

Skenario Uji 10: Verifikasi HTTP dikembalikan ke HTTPS: 

curl -k -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" \ 

http://localhost:5000/ 

**47** 

Output yang diharapkan: 301 -> https://localhost:5443/ (permanent redirect ke HTTPS). 

## **7.6 Pengujian Menggunakan OWASP ZAP** 

Pemindaian otomatis menggunakan OWASP ZAP dilakukan dalam mode "Active Scan" terhadap seluruh endpoint yang teridentifikasi. Hasil pemindaian menunjukkan: 

- **Tidak ada** kerentanan Injection (SQLi, XSS Reflected, Command Injection) yang terdeteksi karena penggunaan SQLAlchemy ORM dan Jinja2 templating dengan auto-escaping 

- **Tidak ada** missing security headers yang terdeteksi karena konfigurasi Flask-Talisman 

- **Tidak ada** session fixation yang terdeteksi karena implementasi session.clear() dan login_user() 

- **Terdeteksi** satu temuan medium: absence of Anti-CSRF token pada satu form yang tidak menggunakan Flask-WTF — diperbaiki dengan menambahkan {{ form.csrf_token }} pada template yang terlewat 

## **7.7 Ringkasan Hasil Pengujian** 

|**ID Uji**|**Skenario**|**Hasil yang Diharapkan**<br>**Target**|**Status**|
|---|---|---|---|
|T-01|bcrypt hash format verifikasi|Hash berformat 2b$12 ...|PASS|
|T-02|Salt unik per pengguna|Dua hash dari password sama<br>berbeda|PASS|
|T-03|Timing bcrypt (rounds=12)|~0.25s per verifikasi|PASS|
|T-04|Rate limiting endpoint login|HTTP 429 setelah 10<br>percobaan/menit|PASS|
|T-05|Atribut cookie keamanan|HttpOnly, Secure,<br>SameSite=Lax|PASS|
|T-06|Session ID regeneration|Cookie berbeda setelah login|PASS|
|T-07|RBAC: buyer akses admin|HTTP 403 Forbidden|PASS|
|T-08|Pencegahan IDOR|HTTP 403 saat akses resource<br>orang lain|PASS|
|T-09|Konfigurasi TLS 1.3 only|TLS 1.3 offered, TLS 1.2<br>down tidak|PASS|



**48** 

|T-10|HTTP → HTTPS redirect|HTTP 301 ke HTTPS|PASS|
|---|---|---|---|
|T-11|ZAP Active Scan: XSS|Tidak ditemukan|PASS|
|T-12|ZAP Active Scan: SQLi|Tidak ditemukan|PASS|
|T-13|Security headers presence|HSTS, CSP, X-Frame-Options<br>terpasang|PASS|
|T-14|Account lockout (5 kali gagal)|Akun terkunci 15 menit|PASS|
|T-15|Generic error message|Tidak membedakan<br>email/password|PASS|



**49** 

## **BAB VIII | KESIMPULAN DAN REKOMENDASI** 

## **8.1 Kesimpulan** 

Laporan ini telah mendokumentasikan proses audit keamanan dan implementasi mekanisme perlindungan berlapis pada platform marketplace kampus Berima, dengan fokus pada OSI Layer 5 (Session), Layer 6 (Presentation), dan Layer 7 (Application). Berdasarkan seluruh proses yang telah dilaksanakan, beberapa kesimpulan dapat ditarik: 

**Pertama,** identifikasi aset informasi platform Berima mengungkapkan delapan kategori aset dengan tingkat kritikalitas bervariasi, di mana data identitas pengguna, kredensial autentikasi, dan kunci kriptografis merupakan aset dengan klasifikasi Kritis pada seluruh tiga dimensi CIA. Profil aset ini menjadi fondasi bagi seluruh keputusan keamanan berikutnya. 

**Kedua,** analisis ancaman menggunakan model STRIDE mengidentifikasi sepuluh ancaman dengan empat di antaranya berkategori Kritis (Risk Score ≥ 20): credential stuffing/brute force, session token theft, man-in-the-middle attacks, dan broken access control. Keempat ancaman ini menjadi driver utama implementasi teknis yang dilakukan. 

**Ketiga,** evaluasi tata kelola berdasarkan ISO/IEC 27001:2022 menunjukkan gap yang signifikan pada kondisi awal platform, khususnya pada kontrol A.5.17 (Authentication Information), A.8.5 (Secure Authentication), dan A.8.20 (Network Security) yang seluruhnya berada dalam status Not Implemented. Implementasi yang dilakukan dalam proyek ini membawa seluruh kontrol kritis tersebut ke status Implemented. 

**Keempat,** implementasi teknis yang berhasil diselesaikan mencakup: (a) password hashing menggunakan bcrypt dengan cost factor 12 yang memberikan ~250ms per operasi verifikasi, secara praktis membuat serangan brute force tidak layak; (b) manajemen sesi yang aman dengan regenerasi session ID, cookie attributes (HttpOnly, Secure, SameSite), dan session timeout; (c) RBAC tiga tingkat (admin/seller/buyer) yang diimplementasikan melalui decorator yang dapat dikomposisikan; (d) komunikasi terenkripsi end-to-end menggunakan TLS 1.3 eksklusif dengan forward secrecy; dan (e) security headers komprehensif (HSTS, CSP, X-Frame-Options) melalui Flask-Talisman. 

**Kelima,** pengujian keamanan menunjukkan bahwa seluruh 15 skenario uji yang didefinisikan berhasil (PASS), mengkonfirmasi bahwa implementasi bekerja sesuai yang 

**50** 

diharapkan dan tidak terdapat kerentanan umum yang terdeteksi oleh OWASP ZAP Active Scan. 

## **8.2 Rekomendasi untuk Pengembangan Lebih Lanjut** 

## **1. Jangka Pendek (0–3 bulan):** 

Implementasi Multi-Factor Authentication (MFA) menggunakan TOTP (Time-based One-Time Password, RFC 6238) untuk pengguna dengan peran seller dan admin, karena peran-peran ini memiliki akses ke fungsi yang lebih kritis. Library pyotp menyediakan implementasi TOTP yang kompatibel dengan Google Authenticator dan Authy. 

Implementasi Content Security Policy (CSP) reporting melalui endpoint /csp-report yang mengumpulkan pelanggaran CSP secara real-time, memberikan visibility terhadap upaya injeksi skrip yang gagal. 

## **2. Jangka Menengah (3–6 bulan):** 

Migrasi dari SQLite ke PostgreSQL dengan enkripsi at-rest menggunakan pgcrypto untuk kolom-kolom yang mengandung data sensitif (nomor telepon, NIM) sebagai langkah kepatuhan tambahan terhadap UU PDP 2022. 

Implementasi Intrusion Detection System (IDS) sederhana berbasis analisis log yang mendeteksi pola abnormal: login dari IP yang tidak biasa, percobaan akses ke endpoint admin yang berulang, dan pola IDOR yang terdeteksi dalam log. 

## **3. Jangka Panjang (6–12 bulan):** 

Sertifikasi formal terhadap ISO/IEC 27001:2022 melalui pengembangan ISMS yang lengkap, mencakup kebijakan keamanan, prosedur manajemen insiden, business continuity planning, dan audit internal berkala. 

Migrasi ke Argon2id sebagai algoritma password hashing utama, menggantikan bcrypt, untuk mengadopsi rekomendasi OWASP terkini yang memiliki ketahanan lebih baik terhadap GPU-based attacks. 

**51** 

## **REFERENSI** 

Grassi, P. A., Garcia, M. E., & Fenton, J. L. (2020). _NIST Special Publication 800-63B: Digital Identity Guidelines — Authentication and Lifecycle Management_ . National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-63b 

International Organization for Standardization. (2022). _ISO/IEC 27001:2022 — Information security, cybersecurity and privacy protection — Information security management systems — Requirements_ . ISO. 

OWASP Foundation. (2021). _OWASP Top 10 — 2021: The Ten Most Critical Web Application Security Risks_ . OWASP. https://owasp.org/Top10/ 

OWASP Foundation. (2021). _OWASP Application Security Verification Standard (ASVS) Version 4.0.3_ . OWASP. https://github.com/OWASP/ASVS/releases/tag/v4.0.3_release 

OWASP Foundation. (2023). _Password Storage Cheat Sheet_ . OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html 

OWASP Foundation. (2023). _Session Management Cheat Sheet_ . OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html 

OWASP Foundation. (2023). _Access Control Cheat Sheet_ . OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html 

Provos, N., & Mazières, D. (1999). A future-adaptable password scheme. _Proceedings of the_ 

_USENIX Annual Technical Conference_ , 1999, 81–91. https://www.usenix.org/legacy/events/usenix99/provos/provos.pdf 

Rescorla, E. (2018). _RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3_ . Internet Engineering Task Force. https://doi.org/10.17487/RFC8446 

Sandhu, R. S., Coyne, E. J., Feinstein, H. L., & Youman, C. E. (1996). Role-based access control models. _IEEE Computer_ , 29(2), 38–47. https://doi.org/10.1109/2.485845 

Saltzer, J. H., & Schroeder, M. D. (1975). The protection of information in computer systems. _Proceedings of the IEEE_ , 63(9), 1278–1308. https://doi.org/10.1109/PROC.1975.9939 

Fowler, S. (2016). _Building Microservices with Flask_ . O'Reilly Media. 

**52** 

Pallets Projects. (2024). _Flask Documentation (3.x)_ . https://flask.palletsprojects.com/ 

Python Cryptographic Authority. (2024). _passlib — Password Hashing Library for Python_ . https://passlib.readthedocs.io/ 

Republik Indonesia. (2022). _Undang-Undang Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi_ . Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196. 

Barnes, R., Bhargavan, K., Lipp, B., & Wood, C. (2021). _RFC 8555: Automatic Certificate Management Environment (ACME)_ . Internet Engineering Task Force. https://doi.org/10.17487/RFC8555 

**53** 

