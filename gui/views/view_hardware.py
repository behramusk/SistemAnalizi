from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QProgressBar
from PySide6.QtCore import Qt, QTimer
from core.hardware_info import get_static_hardware, get_dynamic_hardware

class HardwareView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("DONANIM VE CANLI İZLEME")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        self.grid = QGridLayout()
        self.grid.setSpacing(15)

        # 1. Statik Verileri Ekrana Yazdırıyoruz
        self.static_data = get_static_hardware()
        
        self.add_row("İşlemci (CPU):", f"{self.static_data['cpu_name']} ({self.static_data['cpu_cores']} Core / {self.static_data['cpu_threads']} Thread)", 0)
        
        # Ekran kartlarını listele birden fazlla olabilir ...
        row = 1
        for i, gpu in enumerate(self.static_data['gpus']):
            self.add_row(f"Ekran Kartı (GPU {i+1}):", f"{gpu['model']} | {gpu['vram']} VRAM | Sürücü: {gpu['driver']}", row)
            row += 1

        # 2. Canlı İlerleme Çubukları 
        self.add_row("Anlık CPU Kullanımı:", "", row)
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.grid.addWidget(self.cpu_bar, row, 1)
        
        row += 1
        self.add_row("Anlık RAM Kullanımı:", "", row)
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.grid.addWidget(self.ram_bar, row, 1)

        # RAM Detay Metni
        row += 1
        self.ram_lbl = QLabel("Hesaplanıyor...")
        self.ram_lbl.setStyleSheet("color: #888888; font-size: 12px;")
        self.grid.addWidget(self.ram_lbl, row, 1)

        layout.addLayout(self.grid)
        layout.addStretch()

        # 3. Zamanlayıcıyı (QTimer) Başlat 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_live_data)
        self.timer.start(1000)

    def add_row(self, key_text, val_text, row):
        """Grid'e hızlı satır eklemek için yardımcı fonksiyon"""
        lbl_key = QLabel(key_text)
        lbl_key.setStyleSheet("color: #888888; font-weight: bold; font-size: 13px;")
        
        lbl_val = QLabel(val_text)
        lbl_val.setStyleSheet("color: #E0E0E0; font-size: 13px;")
        lbl_val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        self.grid.addWidget(lbl_key, row, 0)
        self.grid.addWidget(lbl_val, row, 1)

    def update_live_data(self):
        """Zamanlayıcı tarafından saniyede bir çağrılan canlı güncelleme fonksiyonu"""
        live = get_dynamic_hardware()
        
        self.cpu_bar.setValue(int(live['cpu_percent']))
        self.ram_bar.setValue(int(live['ram_percent']))
        
        self.ram_lbl.setText(f"Kullanılan: {live['ram_used']:.1f} GB / Toplam: {live['ram_total']:.1f} GB")