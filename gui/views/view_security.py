from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame
from PySide6.QtCore import Qt, QThread, Signal
from core.security_info import get_security_status

class SecurityWorker(QThread):
    finished_signal = Signal(dict)

    def run(self):
        status_data = get_security_status()
        self.finished_signal.emit(status_data)

class SecurityView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("SİSTEM GÜVENLİK BİLEŞENLERİ")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        
        self.lbl_status = QLabel("Güvenlik politikaları analiz ediliyor, lütfen bekleyin...")
        self.lbl_status.setStyleSheet("color: #FFB900; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(self.lbl_status)

        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        layout.addLayout(self.grid)

        warning_frame = QFrame()
        warning_frame.setStyleSheet("background-color: #2D2D30; border: 1px solid #3E3E42; border-radius: 4px; padding: 15px; margin-top: 30px;")
        w_layout = QVBoxLayout(warning_frame)

        warning_text = QLabel("⚠️ Not: TPM ve BitLocker durumlarını sistem çekirdeğinden kesin olarak okuyabilmek için, programın 'Yönetici Olarak Çalıştır' seçeneğiyle açılması gerekmektedir.")
        warning_text.setStyleSheet("color: #FFB900; font-size: 13px; font-style: italic;")
        warning_text.setWordWrap(True)
        w_layout.addWidget(warning_text)

        layout.addWidget(warning_frame)
        layout.addStretch()

        # Arka plan işçisini başlat
        self.worker = SecurityWorker()
        self.worker.finished_signal.connect(self.populate_data)
        self.worker.start()

    def populate_data(self, status_data):
        self.lbl_status.hide() # Yükleniyor yazısını gizle
        
        self.add_row("Yüklü Antivirüs:", status_data["antivirus"], 0)
        self.add_row("Güvenlik Duvarı (Firewall):", status_data["firewall"], 1)
        self.add_row("Güvenli Önyükleme (Secure Boot):", status_data["secure_boot"], 2)
        self.add_row("TPM 2.0 Modülü:", status_data["tpm"], 3)
        self.add_row("BitLocker Şifreleme:", status_data["bitlocker"], 4)

    def add_row(self, title_text, value_text, row):
        lbl_title = QLabel(title_text)
        lbl_title.setStyleSheet("color: #888888; font-weight: bold; font-size: 14px;")

        color = "#E0E0E0" 
        val_upper = value_text.upper()

        if "AÇIK" in val_upper or "AKTİF" in val_upper:
            color = "#23D18B" 
        elif "KAPALI" in val_upper or "PASİF" in val_upper or "BULUNAMADI" in val_upper:
            color = "#E51400" 
        elif "GEREKLİ" in val_upper or "OKUNAMADI" in val_upper:
            color = "#FFB900" 
        elif value_text != "Bilinmiyor":
            color = "#23D18B" 

        lbl_value = QLabel(value_text)
        lbl_value.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 15px;")

        self.grid.addWidget(lbl_title, row, 0)
        self.grid.addWidget(lbl_value, row, 1)