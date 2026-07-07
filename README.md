# Sistem Analizi 

Sistem Analizi, Windows işletim sistemleri için geliştirilmiş; donanım, ağ, güvenlik ve yazılım envanterini asenkron (Multithreading) mimariyle tarayan, hafif ve kapsamlı bir  yönetim ve izleme aracıdır.

## Temel Özellikler

* **Canlı Donanım İzleme:** QTimer destekli asenkron CPU ve RAM kullanımı takibi.
* **Akıllı Depolama Analizi:** Sistem disklerini tarama ve gereksiz (Temp/Downloads) dosyalar için temizlik önerileri.
* **Gelişmiş Ağ Testi:** Arka planda çalışan ping motoru ve Public/Local IP tespiti.
* **Güvenlik Röntgeni:** WMI ve Registry üzerinden TPM 2.0, Secure Boot, BitLocker, Firewall ve Antivirüs durum kontrolleri (Sezgisel risk renklendirmesi ile).
* **Patch Management:** Microsoft COM API üzerinden bekleyen güncellemeleri kontrol etme ve yüklü KB yamalarının geçmişini listeleme.
* **Yazılım Envanteri:** Windows Registry üzerinden hızlı ve güvenli yüklü program taraması ve dinamik filtreleme.
* **Sistem Sağlığı Skoru (Health Score):** Tüm metrikleri toplayarak 100 üzerinden akıllı puanlama yapan özel algoritma.
* **Raporlama:** Verileri kurumsal IT sistemleri için JSON veya okunabilir TXT formatında dışa aktarma (Export).

## 🛠️ Kurulum ve Kullanım

Bu araç, sistemde hiçbir bağımlılık gerektirmeden "Portable" (Taşınabilir) olarak çalışacak şekilde tasarlanmıştır.

1. Sağ taraftaki **[Releases]** bölümünden uygulamanın son sürümünü (`SistemAnalizi.exe`) indirin.
2. İndirdiğiniz `.exe` dosyasına çift tıklayarak çalıştırın.
*(Not: TPM ve BitLocker gibi donanımsal çekirdek verilerini okuyabilmek için uygulamayı "Yönetici Olarak Çalıştır"manız önerilir).*

## 💻 Geliştiriciler İçin (Kaynak Kodu)

Projeyi kendi ortamınızda derlemek isterseniz:

```bash
# Gerekli kütüphaneleri kurun
pip install psutil wmi PySide6

# Projeyi çalıştırın
python main.py