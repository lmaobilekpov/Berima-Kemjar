import os
from app import create_app, db
from app.models import User, Role, Gig, Order

app = create_app()

def seed():
    with app.app_context():
        # Drop all tables and recreate them to ensure schema is fresh
        db.drop_all()
        db.create_all()
        
        # Pastikan role ada
        admin_role = Role(name='admin')
        seller_role = Role(name='seller')
        buyer_role = Role(name='buyer')
        db.session.add_all([admin_role, seller_role, buyer_role])
        db.session.commit()
        
        # Buat Admin
        admin = User(email='admin@berima.com', username='Administrator', role=admin_role, major="SYSADMIN")
        admin.set_password('AdminBerima123!')
        db.session.add(admin)
            
        # Buat Sellers
        sellers = []
        seller_data = [
            ("seller@berima.com", "SellerPro", "IF '24", "Seller123!"),
            ("afif_fadhilah@berima.com", "Afif Fadhilah", "SI '23", "Seller123!"),
            ("jehezkiel_h@berima.com", "Jehezkiel H", "SD '23", "Seller123!"),
            ("adam_dorman@berima.com", "Adam Dorman", "IF '24", "Seller123!"),
        ]
        
        for email, uname, major, pwd in seller_data:
            s = User(email=email, username=uname, role=seller_role, major=major)
            s.set_password(pwd)
            db.session.add(s)
            sellers.append(s)
            
        # Buat Buyers
        buyer = User(email='buyer@berima.com', username='BuyerKeren', role=buyer_role, major="MK '25")
        buyer.set_password('Buyer123!')
        db.session.add(buyer)
        db.session.commit()
            
        # Buat Gigs
        gigs_data = [
            {
                "title": "Slicing Figma ke Tailwind CSS (Responsif)",
                "description": "Jasa konversi desain Figma projek HMIF ke HTML/Tailwind CSS rapi & bersih. Saya menggunakan best practice agar kode mudah dibaca dan responsif di semua perangkat.",
                "price": 150000.0,
                "delivery": "1-3 Hari",
                "revisions": "2x Revisi",
                "seller_id": sellers[0].id
            },
            {
                "title": "Debugging & Koding Struktur Data (C++ / Java)",
                "description": "Bantu perbaiki error/bug code praktikum Linked List, Tree, dan Pointer kamu. Akan saya berikan komentar penjelasan di setiap baris yang diperbaiki.",
                "price": 90000.0,
                "delivery": "1 Hari (Kilat)",
                "revisions": "Sampai Bug Fix",
                "seller_id": sellers[1].id
            },
            {
                "title": "Analisis Data Skripsi Kuantitatif (Python / SPSS)",
                "description": "Olah data kuesioner metodologi riset atau bab 4 skripsi jurusan FIK. Termasuk uji validitas, reliabilitas, dan regresi linear.",
                "price": 250000.0,
                "delivery": "3-5 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[2].id
            },
            {
                "title": "Desain Topologi Jaringan Cisco Packet Tracer",
                "description": "Konfigurasi routing statis/dinamis, VLAN, dan subnetting untuk tugas Jarkom. Dikerjakan dengan file .pkt siap kumpul.",
                "price": 75000.0,
                "delivery": "1-2 Hari",
                "revisions": "2x Revisi",
                "seller_id": sellers[3].id
            },
            {
                "title": "Pembuatan PPT Interaktif untuk Presentasi Kelas",
                "description": "Desain slide presentasi yang menarik dan profesional dengan animasi untuk presentasi perkuliahan.",
                "price": 40000.0,
                "delivery": "1 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[0].id
            },
            {
                "title": "Web Scraping Data Shopee / Twitter untuk Analisis",
                "description": "Membantu mengambil data publik dari media sosial untuk keperluan dataset analisis sentimen.",
                "price": 180000.0,
                "delivery": "2-3 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[1].id
            },
            {
                "title": "Konfigurasi Server & Deploy Aplikasi dengan Docker",
                "description": "Membantu setup Docker compose dan optimasi environment Ubuntu server untuk web app.",
                "price": 120000.0,
                "delivery": "1-2 Hari",
                "revisions": "Sampai Berhasil",
                "seller_id": sellers[2].id
            },
            {
                "title": "Desain UI/UX Mockup Aplikasi Web atau Mobile",
                "description": "Buat Hi-Fi mockup prototipe aplikasi Figma lengkap dengan wireframing standar industri modern.",
                "price": 150000.0,
                "delivery": "3-4 Hari",
                "revisions": "3x Revisi",
                "seller_id": sellers[3].id
            },
            {
                "title": "Bimbingan Instalasi OS Linux Dual-Boot",
                "description": "Membantu partisi harddisk dan instalasi OS Linux berdampingan dengan Windows aman sentosa.",
                "price": 50000.0,
                "delivery": "1 Hari",
                "revisions": "Konsultasi Penuh",
                "seller_id": sellers[0].id
            },
            {
                "title": "Pembuatan Skema Database & Normalisasi Form",
                "description": "Analisis dan normalisasi skema (ERD) dari 1NF sampai 3NF untuk tugas mata kuliah Basis Data.",
                "price": 60000.0,
                "delivery": "1-2 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[1].id
            },
            {
                "title": "Pemrograman Script Web Automation di Python",
                "description": "Membuat bot otomatis untuk form botting, crawling web data, dan web automation dengan Selenium.",
                "price": 130000.0,
                "delivery": "2 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[2].id
            },
            {
                "title": "Pembuatan Dokumen UML untuk Laporan Proyek",
                "description": "Diagram Class, Use Case, Sequence, dan Activity untuk melengkapi bab 3 dokumen teknis.",
                "price": 85000.0,
                "delivery": "2 Hari",
                "revisions": "2x Revisi",
                "seller_id": sellers[3].id
            },
            {
                "title": "Setup REST API Dasar via Express.js & MongoDB",
                "description": "Bikin struktur endpoint CRUD Auth dasar beserta JWT Token untuk framework backend modern.",
                "price": 125000.0,
                "delivery": "2-3 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[0].id
            },
            {
                "title": "Deploy Project Mahasiswa ke Hosting Cloud",
                "description": "Bantuin ngatasi error dependencies project Next.js atau API Python ketika mau naik ke cloud.",
                "price": 60000.0,
                "delivery": "1 Hari",
                "revisions": "Sampai Tuntas",
                "seller_id": sellers[1].id
            },
            {
                "title": "Proofreading Terjemahan Abstrak Tugas Akhir",
                "description": "Terjemahkan abstrak makalah ke bahasa Inggris yang gramatikalis standar jurnal internasional.",
                "price": 40000.0,
                "delivery": "1 Hari",
                "revisions": "Free Konsultasi",
                "seller_id": sellers[2].id
            },
            {
                "title": "Hitung Big O Kompleksitas Algoritma",
                "description": "Hitung notasi Big-O (Time & Space Complexity) algoritma program untuk laporan Struktur Data.",
                "price": 45000.0,
                "delivery": "1 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[3].id
            },
            {
                "title": "Bikin WA Bot API untuk Reminder Jadwal",
                "description": "Membuat bot WA ringan menggunakan pustaka baileys untuk blast pengingat jadwal kuliah.",
                "price": 100000.0,
                "delivery": "3 Hari",
                "revisions": "Bug Fix 3 Hari",
                "seller_id": sellers[0].id
            },
            {
                "title": "Desain Logo Vektor Event & Organisasi",
                "description": "Desain logo original dengan software vector, include file AI / EPS / SVG beserta varian warna.",
                "price": 95000.0,
                "delivery": "3 Hari",
                "revisions": "3x Revisi",
                "seller_id": sellers[1].id
            },
            {
                "title": "Pembersihan Data (Cleansing) untuk Algoritma ML",
                "description": "Merapikan dataset mentah di Pandas DataFrame, drop / fillna missing values, standar komputasi datamining.",
                "price": 85000.0,
                "delivery": "2 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[2].id
            },
            {
                "title": "Review Kutipan Pustaka & Auto-Formatting Mendeley",
                "description": "Audit sitasi tugas kampus dan styling daftar pustaka supaya langsung rapi IEEE / APA format.",
                "price": 50000.0,
                "delivery": "1 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[3].id
            },
            {
                "title": "Sertifikasi dan Pengujian Penetrasi Website (Pentest)",
                "description": "Scan celah vulnerabilitas (OWASP Top 10) menggunakan BurpSuite, nmap dan berikan laporan keamanan dasar.",
                "price": 250000.0,
                "delivery": "4 Hari",
                "revisions": "1x Revisi",
                "seller_id": sellers[0].id
            },
            {
                "title": "Pembuatan Grafis Animasi Feed Media Sosial Hima",
                "description": "Desain konten motion grafis untuk keperluan post feed instagram organisasi / event lomba.",
                "price": 75000.0,
                "delivery": "2 Hari",
                "revisions": "2x Revisi",
                "seller_id": sellers[1].id
            },
            {
                "title": "Setting Load Balancer & DNS Nginx Web Server",
                "description": "Optimasi Nginx menjadi Load Balancer dan Reverse Proxy supaya web aplikasi bisa traffic berat.",
                "price": 145000.0,
                "delivery": "2 Hari",
                "revisions": "Sampai Clear",
                "seller_id": sellers[2].id
            }
        ]
        
        for g_data in gigs_data:
            gig = Gig(**g_data)
            db.session.add(gig)
            
        db.session.commit()
        print("Database berhasil di-seed dengan data interaktif. Siap untuk demo!")

if __name__ == '__main__':
    seed()
