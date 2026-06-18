from app import create_app
import ssl

app = create_app()

if __name__ == '__main__':
    # Untuk lingkungan lokal pengembangan (Development Environment):
    # Kita menggunakan konteks SSL 'adhoc' yang secara otomatis membuat sertifikat TLS self-signed
    # Ini memastikan seluruh payload data HTTP dienkripsi menjadi HTTPS (Layer 6)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Menolak koneksi SSL lama, mewajibkan penggunaan TLS minimal versi terkini (TLS 1.3)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    
    print("Membuka Platform Berima dengan Perlindungan TLS 1.3 di Port 5443...")
    app.run(host='127.0.0.1', port=5443, ssl_context='adhoc', debug=True)