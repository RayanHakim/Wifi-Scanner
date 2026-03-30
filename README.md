# 📡 Wifi Scanner - Windows 11 Network Reconnaissance Tool

**Wifi Scanner** adalah aplikasi berbasis Python dan Tkinter yang dirancang untuk melakukan pemindaian jaringan nirkabel di sekitar pada sistem operasi Windows 11. Proyek ini mendemonstrasikan implementasi *security bypass* terhadap pembatasan akses lokasi (*Location Services*) yang ketat pada versi Windows terbaru.

## 🚀 Fitur Utama

* **Dual-Engine Scanning:** Menggunakan kombinasi PowerShell dan `netsh` untuk mendapatkan daftar SSID secara *real-time*.
* **Smart Fallback Logic:** Jika akses pemindaian langsung ditolak oleh Windows Defender/Privacy Policy, sistem otomatis beralih membaca *Cache Profil* jaringan yang tersimpan.
* **Multi-threaded GUI:** Proses pemindaian berjalan di latar belakang (asynchronous) sehingga antarmuka tetap responsif.
* **Brute Force Simulator:** Modul edukasi untuk mendemonstrasikan cara kerja algoritma permutasi karakter (A-Z, 0-9).

## 🧠 Konsep & Tantangan Teknis

### 🛡️ Windows 11 Privacy Bypass
Pada Windows 11, pemindaian Wi-Fi dikategorikan sebagai data lokasi sensitif. Program ini berhasil menangani error `ValueError: NULL pointer access` dan `Access is Denied` dengan cara:
1. Melakukan elevasi hak akses (Admin Privileges).
2. Memanfaatkan perintah PowerShell tingkat tinggi untuk berinteraksi dengan **WLAN API**.



### 🐢 CPU vs GPU Cracking (The Bottleneck)
Proyek ini membuktikan secara empiris bahwa melakukan *brute-force* WPA2 menggunakan **CPU (Python Mode)** adalah tidak efisien karena:
* **Key Stretching:** Algoritma PBKDF2 memaksa 4.096 iterasi untuk setiap satu kata.
* **Python GIL:** Membatasi proses komputasi hanya pada satu core prosesor.

Untuk performa maksimal, disarankan menggunakan **RTX 2050 (GPU)** melalui alat seperti **Hashcat** yang mampu bekerja secara paralel.



## 🛠️ Instalasi & Penggunaan

1. Clone repositori ini:
   ```bash
   git clone [https://github.com/username/wifi-scanner.git](https://github.com/username/wifi-scanner.git)
