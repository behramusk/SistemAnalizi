import sys
import os
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def resource_path(relative_path):
    """ PyInstaller'ın oluşturduğu geçici klasörün (MEIPASS) yolunu bulur. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    
    # Tema dosyasını artık dinamik yolla okuyoruz
    qss_path = resource_path("gui/styles.qss")
    
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Uyarı: Tema dosyası bulunamadı: {qss_path}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()