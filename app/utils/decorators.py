import logging # 1. TAMBAHKAN IMPORT LOGGING DI PALING ATAS
from functools import wraps
from flask import abort, request # 2. TAMBAHKAN IMPORT REQUEST DI SINI
from flask_login import current_user
from app.models import Gig

# 3. KONEKSIKAN KE LOGGER SECURITY_AUDIT AGAR MASUK KE SECURITY.LOG
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
        
        # Memastikan objek (Gig) yang diakses/diedit benar-benar milik user yang sedang login
        # Pengecualian (Bypass) untuk role admin
        if gig.seller_id != current_user.id and current_user.role.name != 'admin':
            
            # 4. TAMBAHKAN REKAMAN ALARM IDS SEBELUM DI-ABORT
            security_logger.warning(
                f"IDS_ALERT | IDOR_ATTEMPT | IP: {request.remote_addr} | "
                f"User: {current_user.email} tried to manipulate Gig ID: {gig_id} | Action: Blocked By RBAC"
            )
            
            abort(403) # Mencegah manipulasi ID via parameter URL oleh user lain
            
        return f(*args, **kwargs)
    return decorated_function