import platform
import os
import psutil
import socket
import wmi
import uuid
from datetime import datetime

def get_system_information():
    """Windows sistem, anakart ve ağ bilgilerini WMI ve yerleşik kütüphanelerle çeker."""
    c = wmi.WMI()
    
    # Temel İşletim Sistemi Bilgileri
    os_info = platform.uname()
    
    # Zaman Bilgileri (Son açılış ve çalışma süresi)
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    uptime = datetime.now() - boot_time
    uptime_str = f"{uptime.days} Gün, {uptime.seconds // 3600} Saat, {(uptime.seconds // 60) % 60} Dakika"
    
    # BIOS ve Anakart Bilgileri (WMI üzerinden)
    bios = c.Win32_BIOS()[0]
    board = c.Win32_BaseBoard()[0]
    
    # Ağ ve IP Bilgileri
    hostname = socket.gethostname()
    try:
        ipv4 = socket.gethostbyname(hostname)
    except socket.error:
        ipv4 = "Bulunamadı"
        
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                           for ele in range(0,8*6,8)][::-1])

    # Arayüze gönderilmek üzere verileri sözlük  formatında paketliyoruz
    data = {
        "Bilgisayar Adı": os_info.node,
        "Kullanıcı Adı": os.getlogin(),
        "İşletim Sistemi": f"{os_info.system} {os_info.release}",
        "Sürüm (Build)": os_info.version,
        "Mimari": os_info.machine,
        "Son Açılış (Last Boot)": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Çalışma Süresi (Uptime)": uptime_str,
        "Anakart Üreticisi": board.Manufacturer,
        "Anakart Modeli": board.Product,
        "Seri Numarası": board.SerialNumber,
        "BIOS Sürümü": bios.SMBIOSBIOSVersion,
        "BIOS Tarihi": bios.ReleaseDate[:8] if bios.ReleaseDate else "Bilinmiyor",
        "Hostname": hostname,
        "IPv4 Adresi": ipv4,
        "MAC Adresi": mac_address.upper()
    }
    
    return data