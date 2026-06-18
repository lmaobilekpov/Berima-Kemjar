import logging
import re
from app import db
from app.models import User, Role
from passlib.hash import bcrypt

security_logger = logging.getLogger('security_audit')

# Pre-computed dummy hash with the same work factor (cost=12)
# Used to mitigate timing attacks during login enumeration
DUMMY_HASH = bcrypt.using(rounds=12).hash("dummy_password_for_timing_protection_123!@#")

class AuthService:
    
    @staticmethod
    def _dummy_hash_verify(password):
        """
        Perform a constant-time hashing operation for non-existent users
        to prevent Timing Attack User Enumeration.
        """
        # Verifikasi terhadap dummy hash agar waktu komputasi (CPU time)
        # sama dengan ketika memverifikasi user yang benar-benar ada.
        return bcrypt.verify(password, DUMMY_HASH)

    @staticmethod
    def is_password_strong(password):
        # OWASP ASVS: Minimal 8 karakter, memiliki angka dan huruf
        if len(password) < 8:
            return False
        if not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password):
            return False
        return True

    @staticmethod
    def login(email, password, ip_address):
        """
        Handles the authentication business logic.
        Returns a tuple: (User object if successful else None, Error message if any)
        """
        user = User.query.filter_by(email=email).first()
        generic_error_msg = "Email atau password yang Anda masukkan tidak valid."

        if user:
            # 1. Cek Apakah Akun Sedang Terkunci (Account Lockout Policy)
            if user.is_locked():
                security_logger.warning(f"AKSES DITOLAK: Percobaan login ke akun yang sedang TERKUNCI: {email} dari IP {ip_address}")
                return None, "Akun Anda dikunci sementara (15 menit) karena terlalu banyak gagal login."
                
            # 2. Verifikasi Password Aman via Bcrypt
            if user.check_password(password):
                user.reset_failed_attempts()
                security_logger.info(f"AUTENTIKASI BERHASIL: Pengguna {email} berhasil login dari IP {ip_address}")
                return user, None
            else:
                # Password Salah
                user.increment_failed_attempts()
                security_logger.warning(f"AUTENTIKASI GAGAL: Password salah untuk akun {email} dari IP {ip_address}. Percobaan gagal ke-{user.failed_login_attempts}")
                return None, generic_error_msg
        else:
            # Email Tidak Ditemukan
            security_logger.warning(f"USER ENUMERATION DETECTED: Email tidak terdaftar mencoba masuk: {email} dari IP {ip_address}")
            
            # PROTEKSI TIMING ATTACK:
            # Tetap lakukan komputasi hash meskipun user tidak ditemukan
            AuthService._dummy_hash_verify(password)
            
            return None, generic_error_msg

    @staticmethod
    def register(email, password, role_name, ip_address):
        """
        Handles user registration business logic.
        Returns a tuple: (Boolean success, Message string)
        """
        # 1. Validasi Input Inputan Kosong
        if not email or not password or not role_name:
            return False, "Semua kolom wajib diisi."
            
        # 2. Validasi Kekuatan Password (OWASP ASVS Requirement)
        if not AuthService.is_password_strong(password):
            return False, "Password tidak memenuhi syarat! Minimal 8 karakter, mengandung kombinasi huruf dan angka."
            
        # 3. Pencegahan Duplikasi Akun
        if User.query.filter_by(email=email).first():
            return False, "Email sudah terdaftar di sistem."
            
        # 4. Proteksi Hak Akses (Mencegah Tampering Parameter Admin)
        selected_role = Role.query.filter_by(name=role_name).first()
        if not selected_role or role_name == 'admin':
            security_logger.warning(f"KECURANGAN DETEKSI: Percobaan pendaftaran privilese ADMIN ilegal dari IP {ip_address} menggunakan email: {email}")
            return False, "FORBIDDEN_ROLE" # Penanda khusus untuk di-abort di controller
            
        # Simpan user baru ke database
        new_user = User(email=email, role=selected_role)
        new_user.set_password(password) 
        db.session.add(new_user)
        db.session.commit()
        
        return True, "Registrasi berhasil! Silakan masuk ke akun Anda."
