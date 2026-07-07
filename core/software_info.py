import winreg

def get_installed_software():
    """Windows Kayıt Defterini (Registry) tarayarak yüklü programları bulur."""
    software_list = []
    
    # Taranacak Kayıt Defteri Yolları 
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    for root_key, path in registry_paths:
        try:
            key = winreg.OpenKey(root_key, path)
            # Alt klasör sayısını buluyoruz
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    try:
                        name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        
                        try:
                            version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                        except Exception:
                            version = "-"
                            
                        try:
                            date, _ = winreg.QueryValueEx(subkey, "InstallDate")
                            # Tarihi YYYYMMDD formatından YYYY-MM-DD'ye çeviriyoruz
                            if len(date) == 8:
                                date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
                        except Exception:
                            date = "Bilinmiyor"

                        # İsimsiz Windows güncellemelerini vb. filtreliyoruz
                        if name:
                            software_list.append({
                                "name": name,
                                "version": str(version),
                                "date": str(date)
                            })
                    except Exception:
                        pass
                    finally:
                        winreg.CloseKey(subkey)
                except Exception:
                    pass
            winreg.CloseKey(key)
        except Exception:
            pass

    # Aynı programın (32/64 bit karmaşası yüzünden) çift yazılmasını engellemek için isimleri tekilleştiriyoruz
    unique_software = {v['name']: v for v in software_list}.values()
    
    # İsimlerine göre alfabetik sıraya dizip döndürüyoruz
    return sorted(unique_software, key=lambda x: x['name'].lower())