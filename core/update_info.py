import wmi
import platform
import winreg
import win32com.client


def get_os_build_info():
    """İşletim sisteminin tam sürüm ve derleme (build) bilgisini döndürür."""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        build = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
        try:
            ubr = winreg.QueryValueEx(key, "UBR")[0]
        except FileNotFoundError:
            ubr = "?"
        try:
            display_version = winreg.QueryValueEx(key, "DisplayVersion")[0]  # örn: "23H2"
        except FileNotFoundError:
            display_version = ""
        winreg.CloseKey(key)

        os_info = platform.uname()
        version_str = f"{os_info.system} {os_info.release}"
        if display_version:
            version_str += f" {display_version}"
        version_str += f" (Build {build}.{ubr})"
        return version_str
    except Exception:
        # Registry okunamazsa eski yönteme geri düş
        os_info = platform.uname()
        return f"{os_info.system} {os_info.release} (Derleme: {os_info.version})"


def get_installed_updates():
    """WMI kullanarak sistemdeki yüklü Windows yamalarını (QuickFix) çeker."""
    c = wmi.WMI()
    updates = []

    try:
        for qfe in c.Win32_QuickFixEngineering():
            if qfe.HotFixID and qfe.HotFixID != "File 1":
                updates.append({
                    "kb": qfe.HotFixID,
                    "description": qfe.Description or "Windows Güncellemesi",
                    "date": qfe.InstalledOn or "Tarih Bilinmiyor",
                    "installer": qfe.InstalledBy or "Sistem (NT AUTHORITY)"
                })
    except Exception:
        pass

    updates.reverse()
    return updates


def check_pending_updates():
    """
    Windows Update Agent (WUA) COM API üzerinden henüz kurulmamış
    güncellemeleri sorgular. Bu işlem yavaştır (sunucuya bağlanır),
    bu yüzden mutlaka ayrı bir thread içinde çağrılmalı.
    """
    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()

        search_result = update_searcher.Search("IsInstalled=0 and Type='Software'")

        pending = []
        for i in range(search_result.Updates.Count):
            update = search_result.Updates.Item(i)

            kb_list = []
            try:
                for j in range(update.KBArticleIDs.Count):
                    kb_list.append(f"KB{update.KBArticleIDs.Item(j)}")
            except Exception:
                pass

            pending.append({
                "title": update.Title,
                "kb": ", ".join(kb_list) if kb_list else "-",
                "severity": update.MsrcSeverity or "Normal",
                "size_mb": round(update.MaxDownloadSize / (1024 * 1024), 1) if update.MaxDownloadSize else 0
            })

        return {"success": True, "count": search_result.Updates.Count, "updates": pending}

    except Exception as e:
        return {"success": False, "error": str(e), "count": 0, "updates": []}


def is_reboot_pending():
    """Sistemde yeniden başlatma bekleyen bir güncelleme olup olmadığını kontrol eder."""
    keys_to_check = [
        (winreg.HKEY_LOCAL_MACHINE,
         r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired"),
        (winreg.HKEY_LOCAL_MACHINE,
         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending"),
    ]

    for hive, path in keys_to_check:
        try:
            key = winreg.OpenKey(hive, path)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            continue
        except Exception:
            continue

    return False


def get_full_update_status():
    """
    Arayüzün tek bir çağrıda ihtiyaç duyduğu tüm bilgiyi toplar.
    UpdateWorker içinde bu fonksiyon çağrılacak.
    """
    return {
        "os_info": get_os_build_info(),
        "installed": get_installed_updates(),
        "pending": check_pending_updates(),
        "reboot_pending": is_reboot_pending()
    }