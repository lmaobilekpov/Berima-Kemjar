from app.utils.decorators import owner_required
from flask import Blueprint, render_template, request, render_template_string
from app.models import User
from app import db
import textwrap

demo_bp = Blueprint('demo', __name__, url_prefix='/demo')

# ==========================================
# SCENARIO 3: SQL INJECTION (Vulnerable vs Secure)
# ==========================================

@demo_bp.route('/sqli', methods=['GET', 'POST'])
def sqli_demo():
    query = ""
    result_vuln = None
    result_secure = None
    error_msg = None

    if request.method == 'POST':
        email_input = request.form.get('email', '')
        
        # VULNERABLE APPROACH (Raw SQL String Formatting)
        # Menggunakan raw string formatting sangat rentan terhadap SQLi
        try:
            query = f"SELECT * FROM user WHERE email = '{email_input}'"
            # Execute raw SQL directly
            result_vuln = db.session.execute(db.text(query)).fetchall()
        except Exception as e:
            error_msg = str(e)
            
        # SECURE APPROACH (ORM / Parameterized Query)
        # ORM secara otomatis membersihkan input dan memperlakukannya sebagai literal
        result_secure = User.query.filter_by(email=email_input).all()

    return render_template('sqli_demo.html', 
                           query=query, 
                           result_vuln=result_vuln, 
                           result_secure=result_secure,
                           error_msg=error_msg)

# ==========================================
# SCENARIO 1: CROSS-SITE SCRIPTING (XSS)
# ==========================================

@demo_bp.route('/xss', methods=['GET', 'POST'])
def xss_demo():
    comment = ""
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        
    # Flask Jinja2 secara default melakukan auto-escaping untuk mencegah XSS.
    # Untuk keperluan DEMO, kita menggunakan render_template_string dan |safe (VULNERABLE)
    # vs rendering biasa (SECURE)
    
    html = textwrap.dedent(f"""
    {{% extends "base.html" %}}
    {{% block content %}}
    <div class="max-w-4xl mx-auto mt-10 p-6 bg-white rounded shadow-md">
        <h2 class="text-2xl font-bold mb-6 text-indigo-700">Demo XSS (Layer 5/7)</h2>
        <form method="POST" class="mb-8">
            <label class="block text-gray-700 font-bold mb-2">Tinggalkan Komentar:</label>
            <textarea name="comment" class="w-full border rounded p-2" rows="3" placeholder="Coba masukkan payload: <script>alert(document.cookie)</script>"></textarea>
            <button type="submit" class="mt-2 bg-indigo-500 text-white px-4 py-2 rounded">Kirim</button>
        </form>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="p-4 border border-red-300 bg-red-50 rounded">
                <h3 class="font-bold text-red-700 mb-2">❌ Render Tanpa Sanitasi (Vulnerable)</h3>
                <p class="text-sm text-gray-600 mb-2">Menggunakan |safe filter</p>
                <div class="p-2 bg-white border">{{{{ comment|safe }}}}</div>
            </div>
            
            <div class="p-4 border border-green-300 bg-green-50 rounded">
                <h3 class="font-bold text-green-700 mb-2">✅ Render Dengan Jinja Auto-Escape (Secure)</h3>
                <p class="text-sm text-gray-600 mb-2">Perlindungan XSS bawaan</p>
                <div class="p-2 bg-white border">{{{{ comment }}}}</div>
            </div>
        </div>
        
        <div class="mt-8 p-4 bg-blue-50 border border-blue-200 rounded">
            <h3 class="font-bold text-blue-800">💡 Penjelasan Keamanan Layer 5 (Sesi)</h3>
            <p class="text-blue-900 text-sm mt-1">Jika XSS berhasil jalan, ia akan mencoba menampilkan cookie. Namun, karena <code>SESSION_COOKIE_HTTPONLY = True</code> diset pada <b>config.py</b>, Session ID tetap terlindungi dan tidak bisa dicuri oleh JavaScript.</p>
        </div>
    </div>
    {{% endblock %}}
    """)
    
    return render_template_string(html, comment=comment)
