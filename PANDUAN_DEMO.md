# Panduan Live Demo Keamanan Berima (Untuk 5 Anggota)

Selamat! Seluruh sistem pertahanan (WAF/IPS level aplikasi) dan skrip pengujian (pentest) sudah berhasil dikodekan. Ikuti panduan langkah demi langkah di bawah ini untuk merekam video demonstrasi yang memukau hari ini.

> [!IMPORTANT]
> **PERSIAPAN WAJIB SEBELUM DEMO (TIDAK PERLU DIREKAM):**
> 1. Buka terminal di folder `berima`.
> 2. Hentikan dulu server yang sedang menyala (Ctrl+C).
> 3. Jalankan `python seed_db.py` (untuk membuat database dan akun demo otomatis).
> 4. Jalankan kembali server dengan `python run.py`. Server akan berjalan di `https://127.0.0.1:5443`.

---

## 🎬 Skenario 1: Layer 5 & 7 - Pencegahan XSS & Pengamanan Cookie
**Oleh: Anggota 1**

1. Buka browser dan arahkan ke `https://127.0.0.1:5443/demo/xss` (Demo Mode) ATAU `https://127.0.0.1:5443/gig/create` (Blind Test - Fitur Asli - harus login sebagai penjual).
2. Jelaskan konsep XSS secara singkat kepada dosen ("XSS biasanya digunakan untuk mencuri session cookie").
3. Masukkan *payload* jahat ini ke dalam input judul atau deskripsi:
   `<h1>HACKED!</h1> <script>alert(document.cookie)</script>`
4. Klik **Kirim** / **Terbitkan Lapak**.
5. Tunjukkan hasilnya:
   - Pada simulasi rentan, skrip akan dieksekusi (teks membesar/muncul alert).
   - Di sistem Berima yang aman (baik di halaman `/demo/xss` maupun halaman detail lapak di `/gig/x`), teks di-render apa adanya karena perlindungan Jinja2 *Auto-escape* (Layer 7).
   - Jelaskan bahwa meskipun *script* JavaScript dipaksa jalan, kotak alert (jika muncul) tidak akan menampilkan nilai session cookie. Ini karena fitur keamanan **Layer 5**, yaitu flag `HttpOnly` pada session cookie yang memblokir akses JavaScript.

---

## 🎬 Skenario 2: Layer 5 & 6 - Transport Security (TLS) & Session Fixation
**Oleh: Anggota 2**

1. Buka halaman Login Berima (`https://127.0.0.1:5443/auth/login`).
2. Tekan **F12** untuk membuka Developer Tools, pilih tab **Network**. Refresh halaman.
3. Klik permintaan `login` pertama, buka tab **Headers**. 
   - Tunjukkan bagian *Response Headers*: `Strict-Transport-Security`.
   - Tunjukkan gembok HTTPS di URL bar browser. Jelaskan: *"Ini adalah perlindungan **Layer 6 (Presentation)** menggunakan TLS 1.3. Semua data dari klien ke server dienkripsi 100% sehingga bebas dari sadapan (Man-in-the-Middle)."*
4. Buka tab **Application** (Chrome/Edge) -> Cookies.
   - Tunjukkan nilai `session` ID yang panjang. Perhatikan beberapa karakter terakhirnya.
5. Lakukan login menggunakan akun `seller@berima.com` (Pass: `Seller123!`).
6. Lihat kembali tab Cookies, tunjukkan bahwa nilai `session` telah **berubah sepenuhnya**.
   - Jelaskan: *"Sistem Berima menghancurkan tiket sesi yang lama dan membuat yang baru saat login berhasil. Ini adalah mitigasi keamanan **Layer 5 (Session)** untuk mencegah serangan Session Fixation."*

---

## 🎬 Skenario 3: Layer 7 - Pencegahan SQL Injection
**Oleh: Anggota 3**

1. Buka URL `https://127.0.0.1:5443/demo/sqli` (Demo Mode) ATAU coba login di `https://127.0.0.1:5443/login` (Blind Test - Fitur Asli).
2. Jelaskan konsep SQL Injection: *"Penyerang memasukkan potongan perintah SQL ke dalam input email agar logika server berubah, misalnya memaksa nilai agar selalu TRUE."*
3. Masukkan teks persis seperti ini di input email: `admin@berima.com' OR '1'='1` (isi password bebas).
4. Tekan **Jalankan Query** (atau Login).
5. Jelaskan hasilnya:
   - Pada simulasi sistem yang rentan, serangan tersebut akan menembus database dan memunculkan *semua* email pengguna atau berhasil login tanpa password yang benar.
   - Namun, pada sistem **Berima yang sebenarnya**, serangan tersebut gagal/ditolak.
   - Jelaskan alasannya: *"Sistem kami menggunakan ORM SQLAlchemy. Seluruh input dari user diubah secara paksa menjadi tipe data literal (parameterized query), bukan dianggap sebagai instruksi logika SQL. Hal ini membuat aplikasi kami kebal terhadap injeksi klasik."*

---

## 🎬 Skenario 4: Layer 7 - IDS/IPS, Rate Limiting & Account Lockout
**Oleh: Anggota 4**

1. Buka 2 jendela agar bersebelahan: **Browser** (login sebagai `admin@berima.com` dan buka menu **Admin Panel**) dan **Terminal/Command Prompt**.
2. Pada Admin Panel, tunjukkan indikator **"IPS Engine Active"** berwarna merah.
3. Di terminal, jalankan perintah ini untuk simulasi *Brute Force* (tebak password berkali-kali):
   `python pentest/brute_force_demo.py`
4. Jelaskan apa yang terjadi di terminal:
   - *Script* mencoba ribuan *password* salah secara super cepat.
   - Di percobaan ke-5, server menolak merespon wajar dan langsung mengeluarkan status `HTTP 429 TOO MANY REQUESTS` (Batas login terlampaui).
5. Di browser (Admin Panel), tekan tombol **Refresh** pada tabel "Realtime Log".
6. Tunjukkan kepada dosen bahwa IPS aplikasi secara cerdas telah menangkap anomali tersebut dan mencatat log dengan *tag* kuning/merah: *"Percobaan login ke akun yang sedang TERKUNCI"*.

---

## 🎬 Skenario 5: Layer 7 - Broken Access Control & Proteksi IDOR
**Oleh: Anggota 5**

1. **Persiapan:** Pastikan ada *seller* yang sudah memiliki "Gig" bernomor ID 1.
2. Di browser utama, tunjukkan *Gig* tersebut.
3. Jelaskan konsepnya: *"Sebagai Buyer (Pembeli), kita seharusnya tidak bisa mengedit barang dagangan milik Seller (Penjual). Peretas (hacker) yang menemukan celah IDOR akan mencoba mengubah angka ID di URL (misal: /gig/edit/1) untuk memaksa masuk ke halaman edit milik orang lain."*
4. Buka terminal baru, dan jalankan simulasi peretas:
   `python pentest/idor_demo.py`
5. *Script* otomatis akan pura-pura login sebagai `buyer` dan mencoba mengirimkan permintaan modifikasi secara paksa (melewati *user interface* UI) langsung ke *endpoint* API backend milik `seller`.
6. Tunjukkan *output* di terminal:
   - Serangan **DIGAGALKAN** dengan respon `HTTP 403 FORBIDDEN`.
   - Jelaskan perlindungannya: *"Berima memiliki proteksi keamanan RBAC (Role-Based Access Control) dan Object-Level Verification menggunakan dekorator `@owner_required`. Backend memeriksa secara ketat apakah tiket sesi pengguna yang meminta modifikasi adalah pemilik sah dari aset (Gig) yang dimaksud. Jika bukan, koneksi diputus seketika. Hal ini juga terbukti dengan fitur pemesanan asli yang telah kami tambahkan."*

---
✨ **Penutup Video:**
Kembali tampilkan halaman *Admin Panel* Berima, dan sampaikan bahwa implementasi *Flask-Talisman, Flask-Limiter, Bcrypt,* dan ORM telah mematuhi standar *OWASP ASVS* dan pedoman teknis keamanan aplikasi *ISO/IEC 27001*.
