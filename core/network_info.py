import socket
import subprocess
import urllib.request

def get_basic_network():
    """Yerel ve Public IP adreslerini bulur."""
    # Yerel IP'yi bulmanın en güvenilir yolu dışarıya sahte bir bağlantı açmaktır
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1 (Bağlantı Yok)"

    # Public IP'yi api.ipify.org üzerinden çekiyoruz (Arayüz kasmasın diye 2 saniye kısıtlama koyduk)
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=2) as response:
            public_ip = response.read().decode('utf-8')
    except Exception:
        public_ip = "Çevrimdışı / Zaman Aşımı"

    return {"local_ip": local_ip, "public_ip": public_ip}

def ping_host(host):
    """Verilen adrese 1 adet CMD ping'i atar ve sonucu (ms) döndürür."""
    # Windows için komut: ping -n 1 8.8.8.8
    command = ['ping', '-n', '1', host]
    try:
        # Konsol penceresi açılmadan arka planda komutu çalıştırır
        output = subprocess.check_output(
            command, 
            stderr=subprocess.STDOUT, 
            universal_newlines=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # CMD çıktısının içinden süreyi ayıkladık
        for word in output.split():
            if word.startswith('zaman=') or word.startswith('time='):
                return word.split('=')[1]
        return "Zaman Aşımı"
    except Exception:
        return "Başarısız"