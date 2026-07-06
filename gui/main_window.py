from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Pencere başlığı ve varsayılan boyutu
        self.setWindowTitle("Sistem Analizi")
        self.resize(1000, 600) 

        # Ana kapsayıcı widgeti
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        #  yatay düzen olarak ayarlandı Sol menü ve Sağ içerik yan yana duracak
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Ekranın iki parçasını oluşturan fonksiyonlar
        self.setup_sidebar()
        self.setup_content_area()

    def setup_sidebar(self):
        # Sol menü dikey  bir liste olacak (Butonlar alt alta)
        self.sidebar_layout = QVBoxLayout()
        
        # Uygulama Başlığı
        self.logo_label = QLabel("<b>SİSTEM Analizi</b>")
        self.logo_label.setObjectName("logo_label")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(self.logo_label)

        #  3 adet menü butonu eklendi
        self.btn_system_info = QPushButton("Sistem Bilgisi")
        self.btn_hardware = QPushButton("Donanım")
        self.btn_drivers = QPushButton("Sürücüler")

        self.sidebar_layout.addWidget(self.btn_system_info)
        self.sidebar_layout.addWidget(self.btn_hardware)
        self.sidebar_layout.addWidget(self.btn_drivers)
        
        # Esnek boşluk: Butonları yukarı iter, aşağıdaki boşluğu otomatik doldurur
        self.sidebar_layout.addStretch()

        # Sol menüyü ana yatay düzene eklendi. 
        self.main_layout.addLayout(self.sidebar_layout, 1) 

    def setup_content_area(self):
        # QStackedWidget: Yeni pencere açmak yerine sayfaları üst üste koyar.
        self.content_area = QStackedWidget()
        
        # geçici yazı
        temp_page = QLabel("<h2>Sol taraftan bir menü seçin...</h2>")
        temp_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_area.addWidget(temp_page)

        # Sağ alan ana düzene eklendi
        self.main_layout.addWidget(self.content_area, 4)