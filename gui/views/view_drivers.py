from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QColor
from core.driver_info import get_critical_drivers

# --- ARKAPLAN İŞÇİSİ ---
class DriverWorker(QThread):
    finished_signal = Signal(list)

    def run(self):
        drivers = get_critical_drivers()
        self.finished_signal.emit(drivers)

# --- ARAYÜZ ---
class DriversView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- ÜST KISIM: BAŞLIK VE YENİLE BUTONU ---
        top_layout = QHBoxLayout()
        
        title = QLabel("SÜRÜCÜ (DRIVER) YÖNETİMİ")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        top_layout.addWidget(title)
        
        top_layout.addStretch() # Başlık sola, buton sağa yaslansın
        
        self.btn_refresh = QPushButton("Tekrar Tara")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setStyleSheet("background-color: #2D2D30; color: #CCCCCC; border: 1px solid #3E3E42; padding: 5px 15px;")
        self.btn_refresh.clicked.connect(self.start_scan)
        top_layout.addWidget(self.btn_refresh)
        
        layout.addLayout(top_layout)
        
        # --- DURUM ETİKETİ VE TABLO ---
        self.lbl_status = QLabel("")
        layout.addWidget(self.lbl_status)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Aygıt Adı", "Üretici", "Versiyon & Tarih", "Durum", "İşlem"])
        
        self.table.setStyleSheet("""
            QTableWidget { background-color: #252526; color: #CCCCCC; border: 1px solid #3E3E42; }
            QHeaderView::section { background-color: #2D2D30; color: #38BDF8; font-weight: bold; border: 1px solid #3E3E42; padding: 5px; }
            QTableWidget::item { padding: 5px; border-bottom: 1px solid #333333; }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        # İlk açılışta taramayı başlat
        self.start_scan()

    def start_scan(self):
        """Taramayı başlatan veya sıfırlayan fonksiyon."""
        self.btn_refresh.setEnabled(False)
        self.btn_refresh.setText("Taranıyor...")
        self.table.setRowCount(0) # Eski verileri temizle
        
        self.lbl_status.setText("Sistem taranıyor, sürücüler bulunuyor... Lütfen bekleyin.")
        self.lbl_status.setStyleSheet("color: #FFB900; font-size: 14px; margin-bottom: 10px;")
        
        self.worker = DriverWorker()
        self.worker.finished_signal.connect(self.populate_table)
        self.worker.start()

    def populate_table(self, drivers):
        """İşçi işini bitirince tabloyu güvenli bir şekilde doldurur."""
        self.btn_refresh.setEnabled(True)
        self.btn_refresh.setText("Tekrar Tara")
        
        self.lbl_status.setText(f"Tarama tamamlandı. Toplam {len(drivers)} kritik sürücü bulundu.")
        self.lbl_status.setStyleSheet("color: #38BDF8; font-size: 14px; margin-bottom: 10px;")
        
        self.table.setRowCount(len(drivers))
        
        # HÜCRE DÜZENLENEMEZLİK (ReadOnly) BAYRAĞI
        readonly_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        
        for row, drv in enumerate(drivers):
            item_name = QTableWidgetItem(drv['name'])
            item_name.setFlags(readonly_flags)
            
            item_mfg = QTableWidgetItem(drv['manufacturer'])
            item_mfg.setFlags(readonly_flags)
            
            item_ver = QTableWidgetItem(f"{drv['version']} ({drv['date']})")
            item_ver.setFlags(readonly_flags)
            
            item_status = QTableWidgetItem(drv['status'])
            item_status.setFlags(readonly_flags)
            # DÜZELTME: QTableWidgetItem için QColor kullanılır
            item_status.setForeground(QColor(drv['color'])) 

            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_mfg)
            self.table.setItem(row, 2, item_ver)
            self.table.setItem(row, 3, item_status)
            
            # İşlem Butonu
            btn_search = QPushButton("Web'de Ara")
            btn_search.setStyleSheet("background-color: #007ACC; color: white; border: none; padding: 5px; font-size: 12px;")
            btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
            
            search_query = f"https://www.google.com/search?q={drv['manufacturer']} {drv['name']} driver download"
            btn_search.clicked.connect(lambda checked, q=search_query: QDesktopServices.openUrl(QUrl(q)))
            
            self.table.setCellWidget(row, 4, btn_search)