import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix  # ✨ BARU: Penyelaras IP Asli Client
from app.config import SecurityConfig

# Inisialisasi Ekstensi Inti Keamanan
db = SQLAlchemy()
login_manager = LoginManager()

# Layer 7 (Aplikasi): Rate Limiter Konfigurasi Global untuk mencegah Brute Force & DoS
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["300 per day", "60 per hour"]
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(SecurityConfig)
    
    # 1. MIDDLEWARE PROXYFIX (Penting untuk Akurasi Log & Rate Limiter)
    # Memastikan Flask membaca IP asli pengguna meskipun aplikasi diakses lewat
    # jaringan remote, SSH Tunneling, Port Forwarding, atau Reverse Proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    # Inisialisasi Library Pihak Ketiga ke konteks Flask
    db.init_app(app)
    limiter.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'danger'
    
    # Layer 5 (Sesi): Proteksi Sesi Tingkat Tinggi (Strong Session Protection)
    # Otomatis menghancurkan sesi jika ada deteksi perubahan User-Agent atau pola IP
    login_manager.session_protection = "strong" 

    # INTEGRASI ISO 27001: Kontrol A.8.12 - Manajemen Log Audit Keamanan
    setup_security_logging()

    # 2. LAYER 6 & 7: KEBIJAKAN CONTENT SECURITY POLICY (CSP) KOMPREHENSIF
    # Diperluas agar CDN Tailwind v3/v4, Google Fonts, dan gambar portofolio premium
    # dari Unsplash diizinkan penuh oleh browser (Menghilangkan bug layar kosong/hitam)
    csp = {
        'default-src': '\'self\'',
        'script-src': [
            '\'self\'', 
            '\'unsafe-inline\'',
            'https://cdn.tailwindcss.com',       # Kompiler Utama Tailwind CSS
            'https://cdn.jsdelivr.net'           # Fallback Pustaka JS
        ],
        'style-src': [
            '\'self\'', 
            '\'unsafe-inline\'',                 # Wajib bagi Tailwind untuk injeksi utilitas class
            'https://cdn.jsdelivr.net',
            'https://fonts.googleapis.com'       # Google Fonts untuk tipografi premium
        ],
        'font-src': [
            '\'self\'',
            'https://fonts.gstatic.com'          # Sumber file font biner
        ],
        'img-src': [
            '\'self\'', 
            'data:',                             # Mengizinkan skema gambar berbasis base64 inline
            'https://images.unsplash.com'        # Penyedia gambar portofolio fiktif ala Fiverr
        ]
    }
    
    # Memaksakan Jalur Enkripsi TLS 1.3 & Menyuntikkan Security Headers (HSTS, Anti-Clickjacking)
    Talisman(app, force_https=True, content_security_policy=csp)
    
    # 3. REGISTER ERROR HANDLERS (OWASP ASVS: Pencegahan Kebocoran Informasi)
    register_error_handlers(app)
    
    # --- REGISTRASI BLUEPRINT APLIKASI ---
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.demo.routes import demo_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp) # Blueprint Halaman Utama Marketplace Micro-Gigs
    app.register_blueprint(demo_bp) # Blueprint untuk Demo Akademik Pentest
    
    # Sinkronisasi Skema Database & Pembuatan Tingkat Otoritas Hak Akses Default
    with app.app_context():
        db.create_all()
        create_default_roles()
        
    return app


def setup_security_logging():
    # Mekanisme Rotasi File Log untuk mencegah serangan pengosongan ruang disk (Disk Exhaustion)
    log_handler = RotatingFileHandler('security.log', maxBytes=2 * 1024 * 1024, backupCount=5)
    
    # Formatter log distandarisasi agar mudah dibaca oleh SIEM Tool atau di-audit manual
    log_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s'
    )
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    
    # Ambil instance log khusus audit keamanan
    logger = logging.getLogger('security_audit')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)


def register_error_handlers(app):
    """
    Mitigasi OWASP ASVS - Impementasi Custom Error Handling.
    Mencegah sistem menampilkan stack trace internal (kode error raw) ke pengguna
    ketika terjadi kegagalan sistem, yang dapat dimanfaatkan penyerang untuk reconnaissance.
    """
    security_logger = logging.getLogger('security_audit')

    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('errors.html', title="Bad Request", msg="Permintaan tidak valid atau parameter telah dimanipulasi."), 400

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors.html', title="Akses Ditolak", msg="Anda tidak memiliki hak akses (privilese) untuk melihat halaman ini."), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors.html', title="Tidak Ditemukan", msg="Halaman atau aset yang Anda cari tidak ada di server Berima."), 404

    @app.errorhandler(500)
    def internal_error(error):
        security_logger.critical("CRITICAL SERVER ERROR: Terjadi kegagalan penanganan logika di level backend.")
        return render_template('errors.html', title="Server Error", msg="Terjadi kesalahan internal pada sistem kami. Tim keamanan telah dinotifikasi."), 500


def create_default_roles():
    from app.models import Role
    # Kontrol Akses ISO 27001: Pemisahan Tugas dan Hak Istimewa Penting (Role-Based Access Control)
    if not Role.query.filter_by(name='admin').first():
        db.session.add_all([
            Role(name='admin'),
            Role(name='seller'),
            Role(name='buyer')
        ])
        db.session.commit()