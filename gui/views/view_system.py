from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from core.system_info import get_system_information
from PySide6.QtCore import Qt

class SystemInfoView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Sayfa Başlığı
        title = QLabel("SİSTEM BİLGİSİ")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Verileri tablo gibi hizalamak için Grid  Layout kullanıldı
        grid = QGridLayout()
        grid.setSpacing(12)

        # Backend'den verileri çekiyoruz 
        data = get_system_information()

        # Çekilen verileri döngüyle ekrana yazdırıyoruz
        row = 0
        for key, value in data.items():
            # Sol taraftaki başlık 
            lbl_key = QLabel(f"{key}:")
            lbl_key.setStyleSheet("color: #888888; font-weight: bold; font-size: 13px;")
            
            # Sağ taraftaki değer 
            lbl_val = QLabel(str(value))
            lbl_val.setStyleSheet("color: #E0E0E0; font-size: 13px;")
            lbl_val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse) # Metin kopyalanabilsin

            grid.addWidget(lbl_key, row, 0)
            grid.addWidget(lbl_val, row, 1)
            row += 1

        layout.addLayout(grid)
        layout.addStretch() # İçerikleri yukarı yasla