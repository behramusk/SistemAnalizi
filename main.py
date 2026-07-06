import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # QSS  dosyasını okuyup tüm uygulamaya giydirdik
    try:
        with open("gui/styles.qss", "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Uyarı: styles.qss dosyası bulunamadı, varsayılan tema ile başlatılıyor.")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()