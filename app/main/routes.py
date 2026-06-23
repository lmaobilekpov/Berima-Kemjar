from app.utils.decorators import owner_required
import logging
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Gig, Order
from app.utils.decorators import owner_required
from app import db

security_logger = logging.getLogger('security_audit')

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/marketplace')
def explore_gigs():
    gigs = Gig.query.all()
    return render_template('marketplace.html', gigs=gigs)

@main_bp.route('/gig/<int:gig_id>')
def gig_detail(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    return render_template('gig_detail.html', gig=gig)

@main_bp.route('/about')
def about_page():
    return render_template('about.html')

@main_bp.route('/gig/edit/<int:gig_id>', methods=['GET', 'POST'])
#@login_required
@owner_required
def gig_edit(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    if request.method == 'POST':
        gig.title = request.form.get('title', gig.title)
        gig.description = request.form.get('description', gig.description)
        db.session.commit()
        flash('Gig berhasil diperbarui!', 'success')
        return redirect(url_for('main.gig_detail', gig_id=gig.id))
    return render_template('gig_edit.html', gig=gig)

@main_bp.route('/gig/create', methods=['GET', 'POST'])
# @login_required  <-- 1. MATIKAN INI DENGAN PAGAR AGAR BISA DIAKSES TANPA LOGIN
def gig_create():
    # 2. MODIFIKASI PENGECEKAN ROLE AGAR TIDAK CRASH SAAT USER BELUM LOGIN
    if not current_user.is_authenticated:
        # Jika belum login, kita bypass pengecekan role dan anggap dia Guest/Anonymous untuk keperluan simulasi
        pass
    elif current_user.role.name != 'seller' and current_user.role.name != 'admin':
        abort(403)
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        # LOGIKA DETEKSI IDS UNTUK CROSS-SITE SCRIPTING (XSS CHECK)
        xss_signatures = ["<script>", "javascript:", "alert(", "onerror="]
        if any(sig in (description or '').lower() for sig in xss_signatures) or any(sig in (title or '').lower() for sig in xss_signatures):
            
            # Tentukan identitas penyerang (Anonymous jika belum login)
            user_identity = current_user.email if current_user.is_authenticated else "Anonymous/External Attacker"
            
            # REKAMAN ALARM IDS AKAN MASUK KE ADMIN PANEL
            security_logger.warning(
                f"IDS_ALERT | XSS_ATTEMPT | IP: {request.remote_addr} | User: {user_identity} | "
                f"Payload: XSS Payload Detected in Gig Creation | Action: Sanitized By Jinja2 Auto-escape"
            )

        price = request.form.get('price', type=float) or 0.0
        
        # Siasati seller_id agar database tidak eror integrity constraint saat user anonim posting data
        active_seller_id = current_user.id if current_user.is_authenticated else 1 
        
        new_gig = Gig(
            title=title,
            description=description,
            price=price,
            seller_id=active_seller_id
        )
        db.session.add(new_gig)
        db.session.commit()
        flash('Lapak baru berhasil dibuat!', 'success')
        return redirect(url_for('main.explore_gigs'))
        
    return render_template('gig_create.html')

@main_bp.route('/gig/<int:gig_id>/order', methods=['POST'])
@login_required
def gig_order(gig_id):
    if current_user.role.name != 'buyer' and current_user.role.name != 'admin':
        flash('Hanya akun Buyer yang bisa memesan layanan.', 'danger')
        return redirect(url_for('main.gig_detail', gig_id=gig_id))
        
    gig = Gig.query.get_or_404(gig_id)
    new_order = Order(gig_id=gig.id, buyer_id=current_user.id, status='pending')
    db.session.add(new_order)
    db.session.commit()
    
    flash('Pesanan berhasil dibuat! Anda bisa memantaunya di Dasbor.', 'success')
    return redirect(url_for('auth.dashboard'))