from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QFrame
from PySide6.QtCore import Qt, QThread, Signal
from core.network_info import get_basic_network, ping_host

# --- ARKAPLAN İŞÇİSİ (QTHREAD) ---
class PingWorker(QThread):
    # İşçi, bulduğu sonuçları arayüze iletmek için Sinyaller  kullanır
    update_signal = Signal(str, str) # (Sunucu Adı, ms Sonucu)
    finished_signal = Signal()       # İş bitti sinyali

    def run(self):
        # Ping atılacak sunucular
        targets = {
            "Google DNS (8.8.8.8)": "8.8.8.8",
            "Cloudflare (1.1.1.1)": "1.1.1.1"
        }
        
        for name, ip in targets.items():
            result = ping_host(ip)
            self.update_signal.emit(name, result) # Sonucu arayüze fırlat
            
        self.finished_signal.emit() # İşlem bitti

# --- ARAYÜZ ---
class NetworkView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("AĞ DURUMU VE BAĞLANTI TESTİ")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # 1. IP Bilgileri (Üst Kısım)
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #2D2D30; border: 1px solid #3E3E42; border-radius: 4px; padding: 15px;")
        info_layout = QVBoxLayout(info_frame)
        
        net_info = get_basic_network()
        
        lbl_local = QLabel(f"Yerel IP Adresi: <b>{net_info['local_ip']}</b>")
        lbl_public = QLabel(f"Public IP Adresi: <b>{net_info['public_ip']}</b>")
        lbl_local.setStyleSheet("color: #CCCCCC; font-size: 14px;")
        lbl_public.setStyleSheet("color: #CCCCCC; font-size: 14px;")
        
        info_layout.addWidget(lbl_local)
        info_layout.addWidget(lbl_public)
        layout.addWidget(info_frame)

        layout.addSpacing(20)

        # 2. Ping Testi Alanı (Alt Kısım)
        test_title = QLabel("GECİKME (PING) TESTİ")
        test_title.setStyleSheet("color: #38BDF8; font-size: 16px; font-weight: bold;")
        layout.addWidget(test_title)

        self.btn_ping = QPushButton("Testi Başlat")
        self.btn_ping.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ping.setFixedWidth(150)
        
        # Butona tıklanınca testi başlatan fonksiyonu bağla
        self.btn_ping.clicked.connect(self.start_ping_test)
        layout.addWidget(self.btn_ping)

        # Ping sonuçlarını yazacağımız tablo 
        self.ping_grid = QGridLayout()
        self.ping_grid.setSpacing(10)
        self.ping_labels = {} 
        
        layout.addLayout(self.ping_grid)
        layout.addStretch()

    def start_ping_test(self):
        """Butona basıldığında çalışır."""
        self.btn_ping.setEnabled(False) # Test sürerken butonu kilitle
        self.btn_ping.setText("Test Ediliyor...")
        
        # Eski sonuçları temizle
        for i in reversed(range(self.ping_grid.count())): 
            self.ping_grid.itemAt(i).widget().setParent(None)
        self.ping_labels.clear()

        # İşçiyi (QThread) başlat
        self.worker = PingWorker()
        self.worker.update_signal.connect(self.update_ping_result) # Sinyali fonksiyona bağla
        self.worker.finished_signal.connect(self.ping_test_finished)
        self.worker.start()

    def update_ping_result(self, server_name, result):
        """İşçi ping attıkça bu fonksiyon tetiklenir ve ekrana yazar."""
        row = len(self.ping_labels)
        
        lbl_name = QLabel(f"{server_name}:")
        lbl_name.setStyleSheet("color: #888888; font-weight: bold; font-size: 14px;")
        
        # Eğer sonuç milisaniye ise yeşil/mavi yaz, değilse kırmızı
        color = "#38BDF8" if "ms" in result else "#E51400"
        lbl_result = QLabel(result)
        lbl_result.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        
        self.ping_grid.addWidget(lbl_name, row, 0)
        self.ping_grid.addWidget(lbl_result, row, 1)
        
        self.ping_labels[server_name] = lbl_result

    def ping_test_finished(self):
        """Tüm pingler bitince butonu normale döndür."""
        self.btn_ping.setEnabled(True)
        self.btn_ping.setText("Testi Başlat")