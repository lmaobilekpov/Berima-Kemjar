import logging
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, abort, jsonify, send_file
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user
from app import limiter
from app.models import Order, Gig
from app.services.auth_service import AuthService
from app.utils.decorators import role_required

auth_bp = Blueprint('auth', __name__)

security_logger = logging.getLogger('security_audit')

class RegisterView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('auth.dashboard'))
        return render_template('register.html')

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('auth.dashboard'))
            
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role_name = request.form.get('role', '') # buyer atau seller
        
        success, message = AuthService.register(email, password, role_name, request.remote_addr)
        
        if not success:
            if message == "FORBIDDEN_ROLE":
                abort(400) # Bad Request langsung diputus
            flash(message, 'danger')
            return redirect(url_for('auth.register'))
            
        flash(message, 'success')
        return redirect(url_for('auth.login'))

class LoginView(MethodView):
    decorators = [limiter.limit("5 per minute", error_message="Batas login terlampaui. Silakan tunggu 1 menit.")]

    def get(self):
        if current_user.is_authenticated:
            if current_user.role.name == 'admin':
                return redirect(url_for('auth.admin_panel'))
            return redirect(url_for('auth.dashboard'))
        return render_template('login.html')

    def post(self):
        if current_user.is_authenticated:
            if current_user.role.name == 'admin':
                return redirect(url_for('auth.admin_panel'))
            return redirect(url_for('auth.dashboard'))
            
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user, error_msg = AuthService.login(email, password, request.remote_addr)
        
        if user:
            # MITIGASI UNTUK MEMISAHKAN LOGIN ADMIN: Admin harus login via /admin-portal/login
            if user.role.name == 'admin':
                flash("Admin tidak dapat login melalui portal publik.", "danger")
                security_logger.warning(f"SECURITY: Admin trying to login via public portal: {email} from {request.remote_addr}")
                return redirect(url_for('auth.login'))

            # MITIGASI SESSION FIXATION: Bersihkan session token lama sebelum login baru
            session.clear()
            login_user(user)
            
            return redirect(url_for('auth.dashboard'))
        else:
            # MITIGASI USER ENUMERATION: Pastikan pesan yang keluar selalu generik
            flash("Email atau kata sandi tidak valid.", "danger")
            return redirect(url_for('auth.login'))

class AdminLoginView(MethodView):
    decorators = [limiter.limit("5 per minute", error_message="Batas login terlampaui. Silakan tunggu 1 menit.")]

    def get(self):
        if current_user.is_authenticated:
            if current_user.role.name == 'admin':
                return redirect(url_for('auth.admin_panel'))
            return redirect(url_for('auth.dashboard'))
        return render_template('admin_login.html')

    def post(self):
        if current_user.is_authenticated:
            if current_user.role.name == 'admin':
                return redirect(url_for('auth.admin_panel'))
            return redirect(url_for('auth.dashboard'))
            
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user, error_msg = AuthService.login(email, password, request.remote_addr)
        
        if user:
            if user.role.name != 'admin':
                flash("Akses ditolak. Silakan gunakan portal login publik.", "danger")
                security_logger.warning(f"SECURITY: Non-admin user trying to access admin portal: {email} from {request.remote_addr}")
                return redirect(url_for('auth.admin_login'))
                
            session.clear()
            login_user(user)
            security_logger.info(f"SECURITY: Admin successfully logged in: {email} from {request.remote_addr}")
            return redirect(url_for('auth.admin_panel'))
        else:
            security_logger.warning(f"SECURITY: Failed admin login attempt for {email} from {request.remote_addr}")
            flash("Kredensial tidak valid.", "danger")
            return redirect(url_for('auth.admin_login'))

# Pendaftaran Class-Based Views
auth_bp.add_url_rule('/register', view_func=RegisterView.as_view('register'))
auth_bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
auth_bp.add_url_rule('/admin-portal/login', view_func=AdminLoginView.as_view('admin_login'))

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    user_email = current_user.email
    logout_user()
    session.clear() # Hancurkan server-side session token
    security_logger.info(f"LOGOUT: Pengguna {user_email} telah keluar dari sistem.")
    flash('Anda telah berhasil keluar dari sistem.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'seller':
        orders = Order.query.join(Order.gig).filter(Gig.seller_id == current_user.id).all()
    else:
        orders = Order.query.filter_by(buyer_id=current_user.id).all()
        
    return render_template('dashboard.html', orders=orders)

@auth_bp.route('/admin-panel')
@login_required
@role_required('admin')
def admin_panel():
    # Membaca log keamanan (Simulasi Dashboard IDS/IPS)
    logs = []
    try:
        with open('security.log', 'r') as f:
            # Mengambil 50 baris terakhir, dibalik agar yang terbaru di atas
            lines = f.readlines()
            logs = lines[-50:]
            logs.reverse()
    except FileNotFoundError:
        logs = ["File security.log belum terbuat. Log akan muncul setelah ada aktivitas keamanan."]
        
    return render_template('admin.html', security_logs=logs)

@auth_bp.route('/api/security-logs')
@login_required
@role_required('admin')
def api_security_logs():
    logs = []
    try:
        with open('security.log', 'r') as f:
            lines = f.readlines()
            logs = lines[-50:]
            logs.reverse()
    except FileNotFoundError:
        logs = ["File security.log belum terbuat. Log akan muncul setelah ada aktivitas keamanan."]
        
    return jsonify({'logs': logs})

@auth_bp.route('/admin-panel/logs/download')
@login_required
@role_required('admin')
def download_logs():
    log_path = os.path.abspath('security.log')
    if os.path.exists(log_path):
        return send_file(log_path, as_attachment=True)
    else:
        # Jika file belum ada, buat file kosong lalu download
        open('security.log', 'a').close()
        return send_file(log_path, as_attachment=True)

@auth_bp.route('/admin-panel/logs/clear', methods=['POST'])
@login_required
@role_required('admin')
def clear_logs():
    try:
        # Buka file mode 'w' akan menimpa isinya menjadi kosong
        with open('security.log', 'w') as f:
            pass
        security_logger.info(f"SECURITY: Admin {current_user.email} cleared the security logs.")
        flash("Log keamanan berhasil dikosongkan.", "success")
    except Exception as e:
        flash(f"Gagal mengosongkan log: {str(e)}", "danger")
        
    return redirect(url_for('auth.admin_panel'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        flash('Instruksi pengaturan ulang kata sandi telah dikirimkan ke email kampus Anda.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')