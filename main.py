import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    # 1. Qt'nin arayüz motorunu başlatıyoruz
    app = QApplication(sys.argv)
    
    # 2. Ana penceremizi oluşturup ekranda görünür yapıyoruz
    window = MainWindow()
    window.show()
    
    # 3. Uygulamanın hemen kapanmamasını, biz "Çarpı" tuşuna basana kadar 
    # arka planda dinlemede kalmasını (sonsuz döngü) sağlıyoruz.
    sys.exit(app.exec())

if __name__ == "__main__":
    main()