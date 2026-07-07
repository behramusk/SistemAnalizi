from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame
from PySide6.QtCore import Qt
from gui.views.view_system import SystemInfoView
from gui.views.view_hardware import HardwareView
from gui.views.view_storage import StorageView
from gui.views.view_network import NetworkView
from gui.views.view_drivers import DriversView
from gui.views.view_update import UpdateView
from gui.views.view_security import SecurityView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistem Analizi")
        self.resize(1100, 700) 

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        self.setup_sidebar()
        self.setup_content_area()

    def setup_sidebar(self):
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebar_frame")
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(8)

        # Tüm butonları toplayacağımız liste
        self.menu_buttons = []

        # --- 1. KATEGORİ: SİSTEM ANALİZİ ---
        lbl_system = QLabel("Sistem Analizi")
        lbl_system.setObjectName("category_title")
        self.sidebar_layout.addWidget(lbl_system)

        self.btn_system_info = QPushButton("Sistem Bilgisi")
        self.btn_hardware = QPushButton("Donanım")
        self.btn_storage = QPushButton("Depolama")
        self.btn_network = QPushButton("Ağ Durumu")

        for btn in [self.btn_system_info, self.btn_hardware, self.btn_storage, self.btn_network]:
            self.menu_buttons.append(btn)
            self.sidebar_layout.addWidget(btn)

        # --- 2. KATEGORİ: YÖNETİM & GÜVENLİK ---
        self.sidebar_layout.addSpacing(15)
        lbl_manage = QLabel("Yönetim & Güvenlik")
        lbl_manage.setObjectName("category_title")
        self.sidebar_layout.addWidget(lbl_manage)

        self.btn_drivers = QPushButton("Sürücüler")
        self.btn_update = QPushButton("Windows Update")
        self.btn_security = QPushButton("Güvenlik")
        self.btn_software = QPushButton("Yüklü Yazılımlar")

        for btn in [self.btn_drivers, self.btn_update, self.btn_security, self.btn_software]:
            self.menu_buttons.append(btn)
            self.sidebar_layout.addWidget(btn)

        # --- 3. KATEGORİ: ARAÇLAR & RAPOR ---
        self.sidebar_layout.addSpacing(15)
        lbl_tools = QLabel("Araçlar & Rapor")
        lbl_tools.setObjectName("category_title")
        self.sidebar_layout.addWidget(lbl_tools)

        self.btn_health = QPushButton("Sistem Sağlığı")
        self.btn_export = QPushButton("Rapor Çıktısı")

        for btn in [self.btn_health, self.btn_export]:
            self.menu_buttons.append(btn)
            self.sidebar_layout.addWidget(btn)

        # Tüm butonlara aynı anda Checkable özelliği veriyoruz
        for btn in self.menu_buttons:
            btn.setCheckable(True)
            btn.setAutoExclusive(True)

        # İlk açılışta Sistem Bilgisi seçili gelsin
        self.btn_system_info.setChecked(True)

        self.sidebar_layout.addStretch()
        self.sidebar_frame.setFixedWidth(220)
        self.main_layout.addWidget(self.sidebar_frame) 

    def setup_content_area(self):
        self.content_frame = QFrame()
        self.content_frame.setObjectName("content_frame")
        self.content_layout = QVBoxLayout(self.content_frame)

        self.content_area = QStackedWidget()
        self.content_area.setObjectName("content_area")
        
        # Geçici Boş Sayfa
        self.temp_page = QLabel("- Sisteminizi analiz etmek için soldan bir modül seçin...")
        self.temp_page.setObjectName("placeholder_text")
        self.temp_page.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        #  Sistem Bilgisi Sayfası
        self.page_system = SystemInfoView()
        # Donanım sayfasını oluştur ve Yığın'a  ekle
        self.page_hardware = HardwareView()
        self.content_area.addWidget(self.page_hardware)
        
        # Donanım butonuna tıklandığında sayfayı değiştir
        self.btn_hardware.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page_hardware))
        
        # Sayfaları StackedWidget'a  ekliyoruz
        self.content_area.addWidget(self.temp_page)
        self.content_area.addWidget(self.page_system)
        
        self.content_layout.addWidget(self.content_area)
        self.main_layout.addWidget(self.content_frame)
        
        # Sinyal/Slot Bağlantısı: Butonlara tıklanınca sayfaları değiştir
        self.btn_system_info.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page_system))
        
        # Program ilk açıldığında Sistem Bilgisi sayfası görünsün
        self.content_area.setCurrentWidget(self.page_system)
        # Depolama sayfası
        self.page_storage = StorageView()
        self.content_area.addWidget(self.page_storage)
        
        self.btn_storage.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page_storage))

        # Ağ sayfası
        self.page_network = NetworkView()
        self.content_area.addWidget(self.page_network)
        
        self.btn_network.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page_network))

        # Sürücüler sayfası
        self.page_drivers = DriversView()
        self.content_area.addWidget(self.page_drivers)
        
        self.btn_drivers.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page_drivers))
        # Windows Update sayfası
        self.page_update = UpdateView()
        self.content_area.addWidget(self.page_update)
        
        self.btn_update.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page_update))
        # Güvenlik sayfası
        self.page_security = SecurityView()
        self.content_area.addWidget(self.page_security)
        
        self.btn_security.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page_security))