import tkinter as tk
from tkinter import messagebox
import subprocess
import itertools
import string
import time
import threading

class WifiScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Scanner")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")
        self.is_bruteforcing = False

        # --- UI ELEMENTS ---
        lbl_title = tk.Label(root, text="Network Scanner", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        lbl_title.pack(pady=10)

        self.wifi_listbox = tk.Listbox(root, font=("Consolas", 12), width=50, height=8, bg="#34495e", fg="white")
        self.wifi_listbox.pack(pady=10)

        self.btn_scan = tk.Button(root, text="Scan Wi-Fi Sekitar", command=self.start_scan_thread, bg="#27ae60", fg="white", font=("Arial", 12))
        self.btn_scan.pack(pady=5)

        self.btn_attack = tk.Button(root, text="Simulasi Kombinasi", command=self.start_simulation, bg="#e74c3c", fg="white", font=("Arial", 12))
        self.btn_attack.pack(pady=10)

        self.log_text = tk.Text(root, height=10, width=65, bg="black", fg="#2ecc71", font=("Consolas", 10))
        self.log_text.pack(pady=10)
        self.log("Sistem siap. Menggunakan PowerShell/CMD Engine.")

    def log(self, message):
        """Fungsi untuk menulis log ke terminal GUI"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_scan_thread(self):
        self.wifi_listbox.delete(0, tk.END)
        self.log("Memulai pemindaian jaringan...")
        # Jalankan di thread agar GUI tidak freeze
        threading.Thread(target=self.scan_wifi_cmd, daemon=True).start()

    def scan_wifi_cmd(self):
        """Membaca daftar Wi-Fi menggunakan PowerShell/netsh dengan fallback logic"""
        try:
            # Langkah 1: Mencoba scan LIVE menggunakan PowerShell (lebih powerful)
            self.log("Mencoba Live Scan...")
            process = subprocess.run(
                ["powershell", "-Command", "netsh wlan show networks"], 
                capture_output=True, 
                text=True, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            output = process.stdout
            networks = []

            # Cek jika live scan gagal atau kosong (Access Denied)
            if process.returncode != 0 or "SSID" not in output:
                self.log("⚠️ Live scan ditolak/gagal. Mencoba membaca cache profil...")
                # Langkah 2: Fallback ke profil yang tersimpan (Profiles)
                process = subprocess.run(
                    ["powershell", "-Command", "netsh wlan show profiles"], 
                    capture_output=True, 
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                output = process.stdout
            
            # Parsing output (baik dari networks maupun profiles)
            for line in output.split('\n'):
                if ":" in line:
                    parts = line.split(':')
                    # Cari kata kunci SSID (Live) atau Profil (Cache)
                    if any(key in parts[0] for key in ["SSID", "Profil", "Profile", "Profil Pengguna"]):
                        ssid = parts[1].strip()
                        if ssid:
                            networks.append(ssid)

            # Update tampilan di thread utama
            self.root.after(0, self.update_list, networks)

        except Exception as e:
            self.log(f"❌ Kesalahan Sistem: {e}")

    def update_list(self, networks):
        if networks:
            # Membersihkan duplikat dan mengurutkan
            unique_networks = sorted(set(networks))
            for net in unique_networks:
                self.wifi_listbox.insert(tk.END, f"📡 {net}")
            self.log(f"Selesai. Ditemukan {len(unique_networks)} SSID.")
        else:
            self.log("⚠️ Tidak ada jaringan yang bisa dibaca.")
            self.log("Pastikan 'WLAN AutoConfig' di Services.msc berstatus RUNNING.")

    def start_simulation(self):
        selected = self.wifi_listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih Wi-Fi dulu dari kotak di atas!")
            return
        
        if self.is_bruteforcing: return
        self.is_bruteforcing = True
        target = self.wifi_listbox.get(selected[0])
        self.log(f"\n[!] Simulasi kombinasi untuk: {target}")
        threading.Thread(target=self.run_permutation_loop, daemon=True).start()

    def run_permutation_loop(self):
        """Simulasi logika brute force (Edukasi)"""
        chars = string.ascii_lowercase + string.digits
        count = 0
        # Mencoba kombinasi 4 karakter
        for guess_tuple in itertools.product(chars, repeat=4):
            guess = "".join(guess_tuple)
            count += 1
            if count % 100 == 0:
                # Menghapus log terakhir agar tidak menumpuk (efek animasi terminal)
                self.log_text.delete("end-2l", "end-1l")
                self.log(f"Mencoba kombinasi: {guess}")
                time.sleep(0.01)
            
            # Batasan simulasi agar tidak membebani laptop
            if count > 5000:
                self.log("\n[STOP] Simulasi selesai. Brute force dihentikan.")
                self.log("Gunakan GPU (Hashcat) untuk kecepatan jutaan kombinasi/detik.")
                break
        self.is_bruteforcing = False

if __name__ == "__main__":
    root = tk.Tk()
    app = WifiScannerApp(root)
    root.mainloop()