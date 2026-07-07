from core.storage_info import get_cleanup_info, get_drives_info
from core.hardware_info import get_dynamic_hardware
from core.security_info import get_security_status

def calculate_health():
    """Sistemdeki çeşitli metrikleri toplayıp 100 üzerinden bir sağlık skoru üretir."""
    score = 100
    issues = []
    
    # 1. Depolama Analizi
    cleanup = get_cleanup_info()
    if cleanup['temp_gb'] > 2.0:
        score -= 5
        issues.append("Sistemde 2 GB'tan fazla geçici (Temp) çöp dosya birikmiş.")
        
    drives = get_drives_info()
    for drive in drives:
        if drive['device'].startswith('C') and drive['percent'] > 90:
            score -= 15
            issues.append("C: (Sistem) sürücüsünde boş alan %10'un altına düşmüş, performans etkilenebilir.")
            
    # 2. Donanım (RAM) Analizi
    hw = get_dynamic_hardware()
    if hw['ram_percent'] > 85:
        score -= 10
        issues.append("RAM kullanımı çok yüksek (%85 üzeri). Arka planda çalışan uygulamaları kapatın.")
        
    # 3. Güvenlik Analizi
    sec = get_security_status()
    if "KAPALI" in sec['firewall'].upper() or "BİLİNMİYOR" in sec['firewall'].upper():
        score -= 15
        issues.append("Windows Güvenlik Duvarı (Firewall) kapalı veya çalışmıyor!")
        
    if "BULUNAMADI" in sec['antivirus'].upper() or "KAPALI" in sec['antivirus'].upper():
        score -= 15
        issues.append("Sistemde aktif bir Antivirüs koruması bulunamadı!")
        
    # Skor sınırlandırması ve renk ataması
    score = max(0, score) # Eksiye düşmemesi için
    
    color = "#23D18B" # Yeşil (İyi)
    if score < 60:
        color = "#E51400" # Kırmızı (Kötü)
    elif score < 85:
        color = "#FFB900" # Sarı (Dikkat)
        
    return {
        "score": score,
        "color": color,
        "issues": issues if issues else ["Sisteminiz harika durumda, hiçbir sorun tespit edilmedi!"]
    }