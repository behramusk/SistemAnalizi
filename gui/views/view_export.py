from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal
from utils.exporter import gather_all_data, export_to_txt, export_to_json

class GatherWorker(QThread):
    finished_signal = Signal(dict)

    def run(self):
        data = gather_all_data()
        self.finished_signal.emit(data)

class ExportView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("RAPOR ÇIKTISI (EXPORT)")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        self.lbl_status = QLabel("Tüm sistem verileri toplanıyor, lütfen bekleyin...")
        self.lbl_status.setStyleSheet("color: #FFB900; font-size: 14px; margin-bottom: 30px;")
        layout.addWidget(self.lbl_status)

        # Butonlar için yatay düzen
        btn_layout = QHBoxLayout()
        
        self.btn_txt = QPushButton("TXT Olarak Kaydet")
        self.btn_txt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_txt.setStyleSheet("background-color: #007ACC; color: white; border: none; padding: 10px; font-weight: bold;")
        self.btn_txt.setEnabled(False) # Veri toplanana kadar pasif
        self.btn_txt.clicked.connect(self.save_txt)
        
        self.btn_json = QPushButton("JSON Olarak Kaydet")
        self.btn_json.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_json.setStyleSheet("background-color: #2D2D30; color: #38BDF8; border: 1px solid #38BDF8; padding: 10px; font-weight: bold;")
        self.btn_json.setEnabled(False) # Veri toplanana kadar pasif
        self.btn_json.clicked.connect(self.save_json)

        btn_layout.addWidget(self.btn_txt)
        btn_layout.addWidget(self.btn_json)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.report_data = None
        
        # Arka planda veri toplamayı başlat
        self.worker = GatherWorker()
        self.worker.finished_signal.connect(self.data_ready)
        self.worker.start()

    def data_ready(self, data):
        self.report_data = data
        self.lbl_status.setText("Veriler başarıyla toplandı. Rapor formatını seçebilirsiniz.")
        self.lbl_status.setStyleSheet("color: #23D18B; font-size: 14px; margin-bottom: 30px;")
        self.btn_txt.setEnabled(True)
        self.btn_json.setEnabled(True)

    def save_txt(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "TXT Kaydet", "Sistem_Raporu.txt", "Text Files (*.txt)")
        if filepath:
            export_to_txt(filepath, self.report_data)
            QMessageBox.information(self, "Başarılı", "Rapor TXT olarak kaydedildi!")

    def save_json(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "JSON Kaydet", "Sistem_Raporu.json", "JSON Files (*.json)")
        if filepath:
            export_to_json(filepath, self.report_data)
            QMessageBox.information(self, "Başarılı", "Rapor JSON olarak kaydedildi!")