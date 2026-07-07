from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistem Analizi")
        self.resize(1100, 700) 

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10) # Kenarlardan hafif boşluk
        self.main_layout.setSpacing(10) # Sol ve sağ panel arası boşluk
        
        self.setup_sidebar()
        self.setup_content_area()

    def setup_sidebar(self):
        # Sol Menü Çerçevesi
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebar_frame")
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(8) # Butonlar arası mesafe

        # 1. Kategori Başlığı 
        lbl_system = QLabel("Sistem Analizi")
        lbl_system.setObjectName("category_title")
        self.sidebar_layout.addWidget(lbl_system)

        # Menü Butonları
        self.btn_system_info = QPushButton("Sistem Bilgisi")
        self.btn_hardware = QPushButton("Donanım")
        self.btn_drivers = QPushButton("Sürücüler")

        for btn in [self.btn_system_info, self.btn_hardware, self.btn_drivers]:
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            self.sidebar_layout.addWidget(btn)

        self.btn_system_info.setChecked(True)

        # 2. Kategori Başlığı 
        self.sidebar_layout.addSpacing(15) # Araya biraz boşluk
        lbl_tools = QLabel("Araçlar & Rapor")
        lbl_tools.setObjectName("category_title")
        self.sidebar_layout.addWidget(lbl_tools)

        self.btn_update = QPushButton("Windows Update")
        self.btn_health = QPushButton("Sistem Sağlığı")
        
        for btn in [self.btn_update, self.btn_health]:
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()
        
        # Sol menü genişliğini sabitliyoruz 
        self.sidebar_frame.setFixedWidth(220)
        self.main_layout.addWidget(self.sidebar_frame) 

    def setup_content_area(self):
        # Sağ İçerik Alanı Çerçevesi
        self.content_frame = QFrame()
        self.content_frame.setObjectName("content_frame")
        self.content_layout = QVBoxLayout(self.content_frame)

        self.content_area = QStackedWidget()
        self.content_area.setObjectName("content_area")
        
        self.temp_page = QLabel("- Sisteminizi analiz etmek için soldan bir modül seçin...")
        self.temp_page.setObjectName("placeholder_text")
        self.temp_page.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.content_area.addWidget(self.temp_page)
        self.content_layout.addWidget(self.content_area)
        
        self.main_layout.addWidget(self.content_frame)