from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit
from PySide6.QtCore import Qt, QThread, Signal
from core.software_info import get_installed_software

# --- ARKAPLAN İŞÇİSİ ---
class SoftwareWorker(QThread):
    finished_signal = Signal(list)

    def run(self):
        software = get_installed_software()
        self.finished_signal.emit(software)

# --- ARAYÜZ ---
class SoftwareView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- ÜST KISIM (Başlık ve Arama Kutusu) ---
        top_layout = QHBoxLayout()
        
        title = QLabel("YÜKLÜ YAZILIMLAR")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        top_layout.addWidget(title)
        
        top_layout.addStretch()
        
        #  Arama  Çubuğu
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Program ara...")
        self.search_box.setFixedWidth(250)
        self.search_box.setStyleSheet("""
            QLineEdit { background-color: #2D2D30; color: #CCCCCC; border: 1px solid #3E3E42; padding: 5px; }
            QLineEdit:focus { border: 1px solid #007ACC; }
        """)
        # Yazı yazıldıkça filter_table fonksiyonunu tetikler
        self.search_box.textChanged.connect(self.filter_table)
        top_layout.addWidget(self.search_box)
        
        layout.addLayout(top_layout)
        
        self.lbl_status = QLabel("Kayıt defteri (Registry) taranıyor, lütfen bekleyin...")
        self.lbl_status.setStyleSheet("color: #FFB900; font-size: 14px; margin-bottom: 10px; margin-top: 5px;")
        layout.addWidget(self.lbl_status)

        # --- TABLO YAPISI ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Program Adı", "Versiyon", "Kurulum Tarihi"])
        
        self.table.setStyleSheet("""
            QTableWidget { background-color: #252526; color: #CCCCCC; border: 1px solid #3E3E42; }
            QHeaderView::section { background-color: #2D2D30; color: #38BDF8; font-weight: bold; border: 1px solid #3E3E42; padding: 5px; }
            QTableWidget::item { padding: 5px; border-bottom: 1px solid #333333; }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        # Taramayı Başlat
        self.worker = SoftwareWorker()
        self.worker.finished_signal.connect(self.populate_table)
        self.worker.start()

    def populate_table(self, software_list):
        """İşçi bittikten sonra tabloyu doldurur."""
        self.lbl_status.setText(f"Tarama tamamlandı. Sistemde yüklü {len(software_list)} program bulundu.")
        self.lbl_status.setStyleSheet("color: #38BDF8; font-size: 14px; margin-bottom: 10px; margin-top: 5px;")
        
        self.table.setRowCount(len(software_list))
        readonly_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        
        for row, sw in enumerate(software_list):
            item_name = QTableWidgetItem(sw['name'])
            item_name.setFlags(readonly_flags)
            
            item_ver = QTableWidgetItem(sw['version'])
            item_ver.setFlags(readonly_flags)
            
            item_date = QTableWidgetItem(sw['date'])
            item_date.setFlags(readonly_flags)
            
            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_ver)
            self.table.setItem(row, 2, item_date)

    def filter_table(self, text):
        """Arama kutusuna yazılan metne göre satırları gizler veya gösterir."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                # Metin küçük harfe çevrilip eşleşme aranıyor
                match = text.lower() in item.text().lower()
                self.table.setRowHidden(row, not match)