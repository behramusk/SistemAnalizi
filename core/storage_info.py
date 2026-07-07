import psutil
import os

def get_drives_info():
    """Sistemdeki tüm disk bölümlerini ve doluluk oranlarını çeker."""
    drives = []
    # Bilgisayardaki tüm disk bölümlerini  alındı
    for partition in psutil.disk_partitions():
        # CD-ROM veya okunamayan sürücüleri atlıyoruz
        if os.name == 'nt' and 'cdrom' in partition.opts:
            continue
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            drives.append({
                "device": partition.device,          # Örn: C:\
                "fstype": partition.fstype,          # Örn: NTFS
                "total": usage.total / (1024**3),    # GB cinsinden
                "used": usage.used / (1024**3),
                "free": usage.free / (1024**3),
                "percent": usage.percent
            })
        except PermissionError:
            # Sistem tarafından kilitlenmiş bir kurtarma diski varsa atla
            continue
            
    return drives

def get_folder_size(folder_path):
    """Verilen klasörün içindeki tüm dosyaların toplam boyutunu GB olarak hesaplar."""
    total_size = 0
    if not folder_path or not os.path.exists(folder_path):
        return 0
        
    try:
        for dirpath, _, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Kısayolları (symlink) hesaba katmamak için kontrol ediyoruz
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except Exception:
        pass # Erişim izni olmayan dosyaları atla
        
    return total_size / (1024**3)

def get_cleanup_info():
    """Çöp dosyaların (Temp ve Downloads) boyutlarını analiz eder."""
    user_profile = os.environ.get('USERPROFILE')
    temp_path = os.environ.get('TEMP')
    downloads_path = os.path.join(user_profile, 'Downloads') if user_profile else None
    
    temp_size = get_folder_size(temp_path)
    dl_size = get_folder_size(downloads_path)
    
    return {
        "temp_gb": temp_size,
        "downloads_gb": dl_size
    }