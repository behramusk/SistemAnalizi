from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QProgressBar, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from core.storage_info import get_drives_info, get_cleanup_info

class StorageView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- 1. DİSKLER BÖLÜMÜ ---
        title = QLabel("DEPOLAMA BİRİMLERİ")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(15)

        drives = get_drives_info()
        row = 0
        
        for drive in drives:
            # Disk Adı 
            lbl_drive = QLabel(f"Sürücü {drive['device']} [{drive['fstype']}]:")
            lbl_drive.setStyleSheet("color: #888888; font-weight: bold; font-size: 13px;")
            
            # İlerleme Çubuğu
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(int(drive['percent']))
            
            # Kritik doluluk uyarısı 
            if drive['percent'] > 90:
                bar.setStyleSheet("QProgressBar::chunk { background-color: #E51400; }")

            # Detay Metni
            lbl_detail = QLabel(f"Boş: {drive['free']:.1f} GB / Toplam: {drive['total']:.1f} GB")
            lbl_detail.setStyleSheet("color: #E0E0E0; font-size: 12px;")
            
            grid.addWidget(lbl_drive, row, 0)
            grid.addWidget(bar, row, 1)
            
            row += 1
            grid.addWidget(QLabel(""), row, 0) # Boşluk
            grid.addWidget(lbl_detail, row, 1)
            row += 1

        layout.addLayout(grid)
        
        # --- 2. TEMİZLİK ANALİZİ BÖLÜMÜ ---
        layout.addSpacing(30)
        cleanup_title = QLabel("TEMİZLİK ANALİZİ VE ÖNERİLER")
        cleanup_title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(cleanup_title)

        cleanup_frame = QFrame()
        cleanup_frame.setStyleSheet("background-color: #2D2D30; border: 1px solid #3E3E42; border-radius: 4px; padding: 15px;")
        cleanup_layout = QVBoxLayout(cleanup_frame)

        # Temizlik hesaplaması disk hızına göre 1-2 saniye sürebileceğinden uyarı ver
        cleanup_layout.addWidget(QLabel("Sistemdeki geçici dosyalar hesaplandı:"))

        cleanup_data = get_cleanup_info()
        temp_gb = cleanup_data['temp_gb']
        dl_gb = cleanup_data['downloads_gb']

        lbl_temp = QLabel(f"• Temp (Geçici) Klasörü Boyutu: <b>{temp_gb:.2f} GB</b>")
        lbl_dl = QLabel(f"• İndirilenler Klasörü Boyutu: <b>{dl_gb:.2f} GB</b>")
        lbl_temp.setStyleSheet("color: #CCCCCC; font-size: 14px;")
        lbl_dl.setStyleSheet("color: #CCCCCC; font-size: 14px;")
        
        cleanup_layout.addWidget(lbl_temp)
        cleanup_layout.addWidget(lbl_dl)

        # Akıllı Öneri Mantığı
        if temp_gb > 2.0:
            lbl_advice = QLabel("💡 Öneri: Temp klasörünüz çok fazla yer kaplıyor. Windows Ayarları -> Sistem -> Depolama üzerinden temizlemeniz önerilir.")
            lbl_advice.setStyleSheet("color: #FFB900; font-weight: bold; margin-top: 10px;")
            cleanup_layout.addWidget(lbl_advice)

        layout.addWidget(cleanup_frame)
        layout.addStretch()