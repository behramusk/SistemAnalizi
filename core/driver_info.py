import wmi
from datetime import datetime

# Gerçek donanımı olmayan, sanal/protokol katmanı sürücüleri.
# Bunların üreticisi yok, indirme sayfası yok, WMI'daki eski tarih
# yanıltıcı bir "Güncel Değil" uyarısına yol açıyor.
EXCLUDED_KEYWORDS = [
    "WAN Miniport",
    "Wi-Fi Direct Virtual Adapter",
    "Kernel Debug Network Adapter",
    "RAS Async Adapter",
    "Teredo",
    "isatap",
    "Microsoft ISATAP",
    "Virtual Ethernet",          # Hyper-V vb. sanal adaptörler
    "Bluetooth Device (Personal Area Network)",  # genelde sanal PAN arayüzü
]

def is_virtual_or_irrelevant(name: str, manufacturer: str, device_class: str) -> bool:
    """Sanal/anlamsız sürücüleri filtreler."""
    name_lower = (name or "").lower()

    # Kara listedeki anahtar kelimelerden biri geçiyorsa ele
    if any(keyword.lower() in name_lower for keyword in EXCLUDED_KEYWORDS):
        return True

    # NET sınıfında ve üretici Microsoft ise genelde sanal bir arayüzdür
    
    if device_class == "NET" and manufacturer == "Microsoft":
        return True

    return False


def get_critical_drivers():
    """Kritik donanım sürücülerini WMI üzerinden çeker ve analiz eder."""
    c = wmi.WMI()
    drivers = []

    target_classes = ['DISPLAY', 'MEDIA', 'NET', 'Bluetooth']

    try:
        for driver in c.Win32_PnPSignedDriver():
            if driver.DeviceClass not in target_classes or not driver.Manufacturer:
                continue

            device_name = driver.DeviceName or "Bilinmeyen Aygıt"

            # Sanal/anlamsız sürücüleri baştan ele
            if is_virtual_or_irrelevant(device_name, driver.Manufacturer, driver.DeviceClass):
                continue

            driver_date = "Bilinmiyor"
            status = "Bilinmiyor"
            color = "#888888"

            if driver.DriverDate:
                try:
                    date_str = driver.DriverDate.split('.')[0]
                    d_date = datetime.strptime(date_str, "%Y%m%d%H%M%S")
                    driver_date = d_date.strftime("%Y-%m-%d")

                    age_days = (datetime.now() - d_date).days

                    if age_days < 180:
                        status = "Güncel"
                        color = "#38BDF8"
                    elif age_days < 365:
                        status = "Eski Olabilir"
                        color = "#FFB900"
                    else:
                        status = "Güncel Değil"
                        color = "#E51400"
                except Exception:
                    pass

            drivers.append({
                "name": device_name,
                "manufacturer": driver.Manufacturer,
                "version": driver.DriverVersion or "-",
                "date": driver_date,
                "status": status,
                "color": color
            })
    except Exception:
        pass

    return drivers