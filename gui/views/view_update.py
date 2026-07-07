from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from core.update_info import get_full_update_status


# --- ARKAPLAN İŞÇİSİ ---
class UpdateWorker(QThread):
    finished_signal = Signal(dict)

    def run(self):
        result = get_full_update_status()
        self.finished_signal.emit(result)


# --- ARAYÜZ ---
class UpdateView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- ÜST KISIM (Başlık ve Yenile Butonu) ---
        top_layout = QHBoxLayout()

        title = QLabel("WINDOWS UPDATE GEÇMİŞİ")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        top_layout.addWidget(title)
        top_layout.addStretch()

        self.btn_refresh = QPushButton("Yenile")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setStyleSheet(
            "background-color: #2D2D30; color: #CCCCCC; border: 1px solid #3E3E42; padding: 5px 15px;"
        )
        self.btn_refresh.clicked.connect(self.start_scan)
        top_layout.addWidget(self.btn_refresh)

        layout.addLayout(top_layout)

        # OS Build Bilgisi (worker bitince doldurulacak)
        self.lbl_os = QLabel("Sürüm bilgisi alınıyor...")
        self.lbl_os.setStyleSheet("color: #E0E0E0; font-size: 14px; margin-top: 5px;")
        layout.addWidget(self.lbl_os)

        # --- ÖZET KUTUSU (Bekleyen güncelleme / reboot durumu) ---
        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet(
            "background-color: #252526; border: 1px solid #3E3E42; border-radius: 4px;"
        )
        summary_layout = QVBoxLayout(self.summary_frame)
        summary_layout.setContentsMargins(15, 10, 15, 10)

        self.lbl_pending = QLabel("Bekleyen güncellemeler kontrol ediliyor...")
        self.lbl_pending.setStyleSheet("color: #FFB900; font-size: 14px; font-weight: bold;")
        summary_layout.addWidget(self.lbl_pending)

        self.lbl_reboot = QLabel("")
        self.lbl_reboot.setStyleSheet("color: #888888; font-size: 13px;")
        summary_layout.addWidget(self.lbl_reboot)

        layout.addWidget(self.summary_frame)

        self.lbl_status = QLabel("")
        layout.addWidget(self.lbl_status)

        # --- TABLO YAPISI (Kurulu güncellemeler geçmişi) ---
        table_label = QLabel("Kurulu Güncelleme Geçmişi")
        table_label.setStyleSheet("color: #38BDF8; font-size: 13px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["KB Numarası", "Açıklama", "Kurulum Tarihi", "İşlem"])

        self.table.setStyleSheet("""
            QTableWidget { background-color: #252526; color: #CCCCCC; border: 1px solid #3E3E42; }
            QHeaderView::section { background-color: #2D2D30; color: #38BDF8; font-weight: bold; border: 1px solid #3E3E42; padding: 5px; }
            QTableWidget::item { padding: 5px; border-bottom: 1px solid #333333; }
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.start_scan()

    def start_scan(self):
        self.btn_refresh.setEnabled(False)
        self.btn_refresh.setText("Sorgulanıyor...")
        self.table.setRowCount(0)

        self.lbl_status.setText("Sistem yamaları (Hotfix) kontrol ediliyor...")
        self.lbl_status.setStyleSheet("color: #FFB900; font-size: 14px; margin-bottom: 10px;")

        self.lbl_pending.setText("Bekleyen güncellemeler kontrol ediliyor (bu biraz sürebilir)...")
        self.lbl_pending.setStyleSheet("color: #FFB900; font-size: 14px; font-weight: bold;")
        self.lbl_reboot.setText("")

        self.worker = UpdateWorker()
        self.worker.finished_signal.connect(self.populate_view)
        self.worker.start()

    def populate_view(self, result):
        self.btn_refresh.setEnabled(True)
        self.btn_refresh.setText("Yenile")

        # OS Build bilgisi
        self.lbl_os.setText(f"Mevcut Sürüm: <b>{result['os_info']}</b>")

        # Bekleyen güncellemeler
        pending = result["pending"]
        if pending["success"]:
            if pending["count"] == 0:
                self.lbl_pending.setText("✅ Sistem güncel, bekleyen güncelleme yok.")
                self.lbl_pending.setStyleSheet("color: #38BDF8; font-size: 14px; font-weight: bold;")
            else:
                self.lbl_pending.setText(f"⚠️ {pending['count']} adet bekleyen güncelleme bulundu!")
                self.lbl_pending.setStyleSheet("color: #E51400; font-size: 14px; font-weight: bold;")
        else:
            self.lbl_pending.setText("Bekleyen güncelleme kontrolü yapılamadı (Windows Update servisine erişilemedi).")
            self.lbl_pending.setStyleSheet("color: #888888; font-size: 14px;")

        # Reboot durumu
        if result["reboot_pending"]:
            self.lbl_reboot.setText("🔄 Bilgisayarın yeniden başlatılması gerekiyor.")
            self.lbl_reboot.setStyleSheet("color: #FFB900; font-size: 13px; font-weight: bold;")
        else:
            self.lbl_reboot.setText("Yeniden başlatma gerektiren bir işlem yok.")
            self.lbl_reboot.setStyleSheet("color: #888888; font-size: 13px;")

        # Kurulu güncelleme tablosu
        updates = result["installed"]
        self.lbl_status.setText(f"Sorgu tamamlandı. Sistemde {len(updates)} adet yama (Update) bulundu.")
        self.lbl_status.setStyleSheet("color: #38BDF8; font-size: 14px; margin-bottom: 10px;")

        self.table.setRowCount(len(updates))
        readonly_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        for row, upd in enumerate(updates):
            item_kb = QTableWidgetItem(upd['kb'])
            item_kb.setFlags(readonly_flags)
            item_kb.setForeground(Qt.GlobalColor.white)

            item_desc = QTableWidgetItem(upd['description'])
            item_desc.setFlags(readonly_flags)

            item_date = QTableWidgetItem(upd['date'])
            item_date.setFlags(readonly_flags)

            self.table.setItem(row, 0, item_kb)
            self.table.setItem(row, 1, item_desc)
            self.table.setItem(row, 2, item_date)

            btn_search = QPushButton("Katalogda Ara")
            btn_search.setStyleSheet(
                "background-color: #007ACC; color: white; border: none; padding: 5px; font-size: 12px;"
            )
            btn_search.setCursor(Qt.CursorShape.PointingHandCursor)

            search_query = f"https://www.catalog.update.microsoft.com/Search.aspx?q={upd['kb']}"
            btn_search.clicked.connect(lambda checked, q=search_query: QDesktopServices.openUrl(QUrl(q)))

            self.table.setCellWidget(row, 3, btn_search)