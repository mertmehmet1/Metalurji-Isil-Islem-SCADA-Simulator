import tkinter as tk 
from tkinter import ttk
from firin_simulator import SanalFirin
from ana_yazilim import PIDController, ReceteYöneticisi

# YENİ: Matplotlib kütüphanesini Tkinter arayüzne gömmek için gerekli modüller
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GrafikselScadaArayuz:
    def __init__(self,root):
        self.root = root
        self.root.title("Metalurji Gelişmiş SCADA & Grafik Paneli")
        self.root.geometry("800x500") # Grafiğe yer açmak için ekranı genişlettik
        self.root.configure(bg="#2c3e50")

        # 1. Altyapı Nesneleri
        self.firin = SanalFirin()
        self.firin.start()
        self.pid = PIDController(kp=0.8, ki=0.1, kd=0.05)
        self.recete = ReceteYöneticisi()

        # Grafik Veri Depoları (X ve Y eksenleri için listeler)
        self.zaman_verisi = []
        self.sicaklik_verisi = []
        self.hedef_verisi = []
        self.sayac = 0

        # ---- ANA DÜZEN (Pencereyi İkiye Bölüyoruz) ----
        # Sol taraf kontrol paneli, Sağ taraf canlı grafik olacak 
        self.sol_pencer = tk.Frame(root, bg="#2c3e50", width = 300)
        self.sol_pencer.pack(side="left", fill="y", padx=20,pady=10)

        self.sag_pencer = tk.Frame(root, bg="#34495e")
        self.sag_pencer.pack(side="right",fill="both",expand=True, padx=10,pady=10)

        # ---- SOL PANEL: KONTROL VE METİNLER ----
        self.title_label = tk.Label(self.sol_pencer, text="REÇETE KONTROLÜ", font=("Arial",12,"bold"), bg="#2c3e50", fg="#f1c40f")
        self.title_label.pack(pady=10)

        self.step_label = tk.Label(self.sol_pencer, text="Mevcut Adım: --", font=("Arial",11,"bold"), bg="#2c3e50", fg="#ecf0f1")
        self.step_label.pack(pady=5)

        self.time_label = tk.Label(self.sol_pencer, text="Kalan Süre: -- sn", font=("Arial",10), bg="#2c3e50", fg="#bdc3c7")
        self.time_label.pack(pady=5)

        separator = ttk.Separator(self.sol_pencer, orient='horizontal')
        separator.pack(fill='x',pady=15)

        self.temp_label = tk.Label(self.sol_pencer, text="-- \u00b0C", font=("Arial",28,"bold"), bg="#2c3e50", fg="#3498db")
        self.temp_label.pack(pady=10)

        self.setpoint_label = tk.Label(self.sol_pencer, text="Hedef: --\u00b0C", font=("Arial",11), bg="#2c3e50", fg="#2ecc71")
        self.setpoint_label.pack(pady=5)

        self.status_label = tk.Label(self.sol_pencer, text="Sistem: Başlatılıyor", font=("Arial",9,"italic"),bg="#2c3e50", fg="#bdc3c7")
        self.status_label.pack(pady=30)

        # ---- SAĞ PANEL: MATPLOTLIB CANLI GRAFİK ----
        # Bilgisayar Mühendisliğinde grafik nesnesi(Figure) oluşturma
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.fig.patch.set_facecolor("#34495e") # Grafiğin arka plan rengi 

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#2c3e50")
        self.ax.set_title("Canlı Isıl İşlem Eğrisi(Sıcaklık/Zaman)", color="white", fontsize=10)
        self.ax.tick_params(colors="white") # Eksen yazılarının rengi

        # Grafiği Tkinter penceresine gömme sihirbazı (Canvas)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.sag_pencer)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Kapanış Ayarı
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)

        # Ootomasyonu başlat
        self.otomasyon_dongusu()

    def otomasyon_dongusu(self):
        recete_durumu = self.recete.güncelle_zaman()
        mevcut_sicaklik = self.firin.get_temperature()
        guncel_hedef = self.recete.get_guncel_hedef()

        # Grafik için verileri listelere (Arrays) ekliyoruz
        self.sayac += 1
        self.zaman_verisi.append(self.sayac)
        self.sicaklik_verisi.append(mevcut_sicaklik)
        self.hedef_verisi.append(guncel_hedef)

        # Canlı Grafiği Çizdirme Mantığı
        self.ax.clear() # eski çizgiyi sil 
        self.ax.set_facecolor("#2c3e50")
        # Mevcut sıcaklığı Kırmızı,Reçete hedefini Kesikli Yeşil çizgi yapıyoruz
        self.ax.plot(self.zaman_verisi, self.sicaklik_verisi, label="Mevcut Sıcaklık", color="#e74c3c", linewidth=2)
        self.ax.plot(self.zaman_verisi, self.hedef_verisi, label="Reçete Hedefi",color="#2ecc71", linestyle="--",linewidth=1.5)
        self.ax.legend(loc="upper left") # Bilgilendirme kutusu
        self.ax.grid(True, color="#7f8c8d", alpha=0.3) # Arka plan kareleri 
        self.canvas.draw() # Grafiği ekranda güncelle

        if recete_durumu == "BITTI":
            self.firin.set_heater(False)
            self.step_label.config(text="REÇETE TAMAMLANDI!", fg="#2ecc71")
            self.time_label.config(text="İşlem bitti.")
            self.temp_label.config(fg="#3498db")
            self.status_label.config(text="Sistem: Güvenli Beklemede", fg="#bdc3c7")
            return
        
        # PID Kontrolü
        kontrol_sinyali = self.pid.calculate(guncel_hedef, mevcut_sicaklik)

        if kontrol_sinyali > 0:
            self.firin.set_heater(True)
            self.status_label.config(text=f"Sistem: ISITILIYOR (PID: {round(kontrol_sinyali,1)})", fg="#e74c3c")
            self.temp_label.config(fg="#e74c3c")

        else:
            self.firin.set_heater(False)
            self.status_label.config(text="Sistem: SOĞUTULUYOR / BEKLEMEDE", fg="#3498db")
            self.temp_label.config(fg="#3498db")

        # Metinleri Güncelle
        guncel_adim = self.recete.aktif_recete[self.recete.guncel_adim_index]
        self.step_label.config(text=f"Mevcut Adım: {guncel_adim['isim']}")
        self.time_label.config(text=f"Kalan Süre: {self.recete.adim_kalan_sure} sn")
        self.setpoint_label.config(text=f"Hedef: {guncel_hedef} \u00b0C")
        self.temp_label.config(text=f"{mevcut_sicaklik} \u00b0C")

        self.root.after(1000, self.otomasyon_dongusu)

    def on_closing(self):
        self.firin.stop()
        self.firin.join()
        self.root.destroy()

if __name__ == "__main__":
    pencere = tk.Tk()
    app = GrafikselScadaArayuz(pencere)
    pencere.mainloop()            















            
    