from app import db, login_manager
from flask_login import UserMixin
from passlib.hash import bcrypt
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False) # admin, seller, buyer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=True)
    major = db.Column(db.String(50), nullable=True, default="IF '24")
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    # Atribut untuk Kebijakan Penguncian Akun (Account Lockout Policy)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    role = db.relationship('Role', backref='users')

    # --- IMPLEMENTASI LAYER 6: PASSWORD HASHING DENGAN BCRYPT COST 12 ---
    def set_password(self, password):
        # Mengubah teks polos menjadi digest hash menggunakan bcrypt (work factor/rounds=12)
        self.password_hash = bcrypt.using(rounds=12).hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    # --- ATURAN LOCKOUT (Mencegah Online Brute Force) ---
    def is_locked(self):
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def increment_failed_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5: # Kunci setelah 5 kali gagal
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()

class Gig(db.Model):
    # Model data transaksi jasa (Gig) untuk pengujian IDOR
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    delivery = db.Column(db.String(50), nullable=True, default="1-3 Hari")
    revisions = db.Column(db.String(50), nullable=True, default="1x Revisi")
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    seller = db.relationship('User', backref='gigs')

class Order(db.Model):
    # Model transaksi pemesanan (Order)
    id = db.Column(db.Integer, primary_key=True)
    gig_id = db.Column(db.Integer, db.ForeignKey('gig.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default="pending") # pending, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    gig = db.relationship('Gig', backref='orders')
    buyer = db.relationship('User', backref='orders_as_buyer')