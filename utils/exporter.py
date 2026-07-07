import json
from datetime import datetime
from core.system_info import get_system_information
from core.hardware_info import get_static_hardware, get_dynamic_hardware
from core.storage_info import get_drives_info
from core.network_info import get_basic_network
from core.security_info import get_security_status
from core.health_score import calculate_health

def gather_all_data():
    """Tüm sistem verilerini toplayıp dev bir sözlük (dictionary) döndürür."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system": get_system_information(),
        "hardware_static": get_static_hardware(),
        "hardware_dynamic": get_dynamic_hardware(),
        "storage": get_drives_info(),
        "network": get_basic_network(),
        "security": get_security_status(),
        "health": calculate_health()
    }

def export_to_json(filepath, data):
    """Veriyi JSON formatında kaydeder."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def export_to_txt(filepath, data):
    """Veriyi okunabilir profesyonel bir TXT raporuna dönüştürür."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("="*50 + "\n")
        f.write(" " * 10 + "SİSTEM MERKEZİ - ANALİZ RAPORU\n")
        f.write("="*50 + "\n")
        f.write(f"Oluşturulma Tarihi: {data['timestamp']}\n\n")

        f.write("[ 1. SİSTEM SAĞLIĞI VE ÖZET ]\n")
        f.write(f"Skor: {data['health']['score']} / 100\n")
        for issue in data['health']['issues']:
            f.write(f"-> {issue}\n")
        f.write("\n")

        f.write("[ 2. SİSTEM BİLGİSİ ]\n")
        for k, v in data['system'].items():
            f.write(f"{k}: {v}\n")
        f.write("\n")

        f.write("[ 3. DONANIM ]\n")
        f.write(f"İşlemci: {data['hardware_static']['cpu_name']}\n")
        for i, gpu in enumerate(data['hardware_static']['gpus']):
            f.write(f"Ekran Kartı {i+1}: {gpu['model']} ({gpu['vram']})\n")
        f.write(f"Anlık RAM Kullanımı: %{data['hardware_dynamic']['ram_percent']}\n\n")

        f.write("[ 4. GÜVENLİK ]\n")
        for k, v in data['security'].items():
            f.write(f"{k.capitalize()}: {v}\n")
        f.write("\n")
        
        f.write("="*50 + "\n")
        f.write("Bu rapor Sistem Analizi aracı tarafından otomatik oluşturulmuştur.\n")