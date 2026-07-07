from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QThread, Signal
from core.health_score import calculate_health

class HealthWorker(QThread):
    finished_signal = Signal(dict)

    def run(self):
        result = calculate_health()
        self.finished_signal.emit(result)

class HealthView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("SİSTEM SAĞLIK RAPORU")
        title.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title)
        
        self.lbl_status = QLabel("Tüm sistem bileşenleri analiz ediliyor... Bu işlem 10-15 saniye sürebilir.")
        self.lbl_status.setStyleSheet("color: #FFB900; font-size: 14px; margin-top: 10px;")
        self.layout.addWidget(self.lbl_status)
        
        self.score_container = QWidget()
        self.score_layout = QVBoxLayout(self.score_container)
        self.layout.addWidget(self.score_container)
        
        self.layout.addStretch()
        
        self.worker = HealthWorker()
        self.worker.finished_signal.connect(self.display_score)
        self.worker.start()

    def display_score(self, result):
        self.lbl_status.hide()
        
        # 1. Dev Puan Skoru Gösterimi
        score_lbl = QLabel(f"{result['score']} / 100")
        score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_lbl.setStyleSheet(f"color: {result['color']}; font-size: 72px; font-weight: bold; margin-top: 20px;")
        self.score_layout.addWidget(score_lbl)
        
        # 2. Sorunlar ve Öneriler Listesi
        issues_frame = QFrame()
        issues_frame.setStyleSheet("background-color: #2D2D30; border: 1px solid #3E3E42; border-radius: 4px; padding: 20px; margin-top: 30px;")
        i_layout = QVBoxLayout(issues_frame)
        
        i_title = QLabel("Tespit Edilen Sorunlar / Öneriler:")
        i_title.setStyleSheet("color: #CCCCCC; font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        i_layout.addWidget(i_title)
        
        for issue in result['issues']:
            lbl_issue = QLabel(f"• {issue}")
            # Eğer sorun yok mesajı geldiyse yeşil, sorun varsa sarı yap
            text_color = "#23D18B" if "harika durumda" in issue else "#FFB900"
            lbl_issue.setStyleSheet(f"color: {text_color}; font-size: 14px;")
            lbl_issue.setWordWrap(True)
            i_layout.addWidget(lbl_issue)
            
        self.score_layout.addWidget(issues_frame)