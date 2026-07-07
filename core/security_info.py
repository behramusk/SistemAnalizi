import wmi
import subprocess
import winreg

def get_security_status():
    """İşletim sisteminin ve donanımın temel güvenlik politikalarını analiz eder."""
    status = {
        "antivirus": "Bilinmiyor",
        "firewall": "Bilinmiyor",
        "secure_boot": "Desteklenmiyor / Kapalı",
        "tpm": "Bulunamadı / Yetki Yok",
        "bitlocker": "Bilinmiyor / Yetki Yok"
    }

    # 1. Antivirüs Durumu (SecurityCenter2 üzerinden okuma)
    try:
        c = wmi.WMI(namespace="root\\SecurityCenter2")
        av_list = [av.displayName for av in c.AntivirusProduct()]
        if av_list:
            status["antivirus"] = " , ".join(av_list)
        else:
            status["antivirus"] = "Bulunamadı"
    except Exception:
        status["antivirus"] = "Okunamadı"

    # 2. Güvenlik Duvarı 
    try:
        output = subprocess.check_output(
            ["netsh", "advfirewall", "show", "currentprofile", "state"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            encoding="utf-8"
        )
        if "ON" in output.upper() or "AÇIK" in output.upper():
            status["firewall"] = "Açık"
        else:
            status["firewall"] = "Kapalı"
    except Exception:
        status["firewall"] = "Okunamadı"

    # 3. Secure Boot (Güvenli Önyükleme) Durumu (Kayıt Defterinden)
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"System\CurrentControlSet\Control\SecureBoot\State")
        value, _ = winreg.QueryValueEx(reg_key, "UEFISecureBootEnabled")
        status["secure_boot"] = "Açık" if value == 1 else "Kapalı"
        winreg.CloseKey(reg_key)
    except Exception:
        status["secure_boot"] = "Desteklenmiyor"

    # 4. TPM 2.0 Durumu (Yönetici yetkisi gerektirebilir)
    try:
        c_tpm = wmi.WMI(namespace="root\\CIMV2\\Security\\MicrosoftTpm")
        tpm = c_tpm.Win32_Tpm()[0]
        status["tpm"] = "Aktif" if tpm.IsEnabled_InitialValue else "Pasif"
    except Exception:
        status["tpm"] = "Yönetici İzni Gerekli"

    # 5. BitLocker Durumu (Yönetici yetkisi gerektirir)
    try:
        c_bit = wmi.WMI(namespace="root\\CIMV2\\Security\\MicrosoftVolumeEncryption")
        volumes = c_bit.Win32_EncryptableVolume()
        # ProtectionStatus == 1 ise disk şifrelenmiştir
        encrypted = [v.DriveLetter for v in volumes if v.ProtectionStatus == 1]
        
        if encrypted:
            status["bitlocker"] = f"Açık ({', '.join(encrypted)})"
        else:
            status["bitlocker"] = "Kapalı"
    except Exception:
        status["bitlocker"] = "Yönetici İzni Gerekli"

    return status