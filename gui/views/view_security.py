from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame
from PySide6.QtCore import Qt
from core.security_info import get_security_status

class SecurityView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("SİSTEM GÜVENLİK BİLEŞENLERİ")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        # Güvenlik verileri milisaniyeler içinde çekildiği için QThread'e ihtiyaç duymadık
        status_data = get_security_status()

        self.add_row("Yüklü Antivirüs:", status_data["antivirus"], 0)
        self.add_row("Güvenlik Duvarı (Firewall):", status_data["firewall"], 1)
        self.add_row("Güvenli Önyükleme (Secure Boot):", status_data["secure_boot"], 2)
        self.add_row("TPM 2.0 Modülü:", status_data["tpm"], 3)
        self.add_row("BitLocker Şifreleme:", status_data["bitlocker"], 4)

        layout.addLayout(self.grid)

        # --- ALT BİLGİLENDİRME KUTUSU ---
        warning_frame = QFrame()
        warning_frame.setStyleSheet("background-color: #2D2D30; border: 1px solid #3E3E42; border-radius: 4px; padding: 15px; margin-top: 30px;")
        w_layout = QVBoxLayout(warning_frame)

        warning_text = QLabel("⚠️ Not: TPM ve BitLocker durumlarını sistem çekirdeğinden kesin olarak okuyabilmek için, programın 'Yönetici Olarak Çalıştır' seçeneğiyle açılması gerekmektedir.")
        warning_text.setStyleSheet("color: #FFB900; font-size: 13px; font-style: italic;")
        warning_text.setWordWrap(True)
        w_layout.addWidget(warning_text)

        layout.addWidget(warning_frame)
        layout.addStretch()

    def add_row(self, title_text, value_text, row):
        lbl_title = QLabel(title_text)
        lbl_title.setStyleSheet("color: #888888; font-weight: bold; font-size: 14px;")

        # Duruma göre dinamik renk ataması 
        color = "#E0E0E0" 
        val_upper = value_text.upper()

        if "AÇIK" in val_upper or "AKTİF" in val_upper:
            color = "#23D18B" # VS Code Yeşili (Güvenli)
        elif "KAPALI" in val_upper or "PASİF" in val_upper or "BULUNAMADI" in val_upper:
            color = "#E51400" # Kırmızı (Risk)
        elif "GEREKLİ" in val_upper or "OKUNAMADI" in val_upper:
            color = "#FFB900" # Sarı (Uyarı/Erişim Yok)
        elif value_text != "Bilinmiyor":
            color = "#23D18B" # Antivirüs adı yazıyorsa yeşil yap

        lbl_value = QLabel(value_text)
        lbl_value.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 15px;")

        self.grid.addWidget(lbl_title, row, 0)
        self.grid.addWidget(lbl_value, row, 1)