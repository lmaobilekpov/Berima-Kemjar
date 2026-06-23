import logging
from functools import wraps
from flask import abort, request
from flask_login import current_user
from app.models import Gig

# Hubungkan ke sistem pencatatan log utama agar langsung masuk ke Admin Panel
security_logger = logging.getLogger('security_audit')

def role_required(*role_names):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role.name not in role_names:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        gig_id = kwargs.get('gig_id')
        gig = Gig.query.get_or_404(gig_id)
        
        # CEK PROTEKSI IDOR: Jika user belum login ATALAU user yang login bukan pemilik/admin
        is_authenticated = current_user.is_authenticated
        
        if not is_authenticated or (gig.seller_id != current_user.id and current_user.role.name != 'admin'):
            
            # Tentukan identitas penyerang untuk laporan log
            user_identity = current_user.email if is_authenticated else "Anonymous/External Attacker"
            
            # KIRIM ALARM IDS KE FILE LOG UTAMA
            security_logger.warning(
                f"IDS_ALERT | IDOR_ATTEMPT | IP: {request.remote_addr} | "
                f"User: {user_identity} tried to manipulate Gig ID: {gig_id} | Action: Blocked By RBAC"
            )
            
            abort(403)  # Tolak paksa dengan error 403 Forbidden
            
        return f(*args, **kwargs)
    return decorated_function