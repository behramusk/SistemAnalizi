import psutil
import wmi

def get_static_hardware():
    """Program açıldığında sadece 1 kez çalışır (Ağır WMI işlemleri)"""
    c = wmi.WMI()
    
    try:
        cpu = c.Win32_Processor()[0]
        cpu_name = cpu.Name.strip()
    except:
        cpu_name = "Bilinmeyen CPU"

    gpu_list = []
    try:
        gpus = c.Win32_VideoController()
        for gpu in gpus:
            if gpu.AdapterRAM:
                vram_bytes = int(gpu.AdapterRAM)
                
                
                # Ekran kartı yüksek RAM'e sahipse WMI bunu negatif okur.
                if vram_bytes < 0:
                    vram_bytes += (2**32) 
                
               
                vram_bytes = abs(vram_bytes) 
                
                vram_gb = vram_bytes / (1024**3)
            else:
                vram_gb = 0
            
            gpu_list.append({
                "model": gpu.Name,
                "vram": f"{vram_gb:.2f} GB",
                "driver": gpu.DriverVersion
            })
    except:
        pass 

    return {
        "cpu_name": cpu_name,
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "gpus": gpu_list
    }

def get_dynamic_hardware():
    """QTimer ile saniyede bir çalıştırılacak hafif psutil işlemleri"""
    ram = psutil.virtual_memory()
    
    return {
        "cpu_percent": psutil.cpu_percent(interval=None), 
        "ram_total": ram.total / (1024**3),
        "ram_used": ram.used / (1024**3),
        "ram_percent": ram.percent
    }