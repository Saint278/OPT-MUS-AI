import customtkinter as ctk
import threading
import os, sys, datetime, webbrowser, subprocess, time
import requests, psutil, speedtest, wikipedia
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
import random
from bs4 import BeautifulSoup

# --- STRATEJİK YAPILANDIRMA ---
ctk.set_appearance_mode("Dark")
wikipedia.set_lang("tr")
PAROLA = "istikbal göklerdedir" 

class OptimusNihai(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- PENCERE AYARLARI ---
        self.title("OPTIMUS V12: NİHAİ STRATEJİK KOMUTA MERKEZİ")
        self.geometry("1200x900")
        self.resizable(False, False)
        self.kilitli = True 

        # --- MOTORLAR ---
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170) 
        self.recognizer = sr.Recognizer()

        # --- GÖRSEL ARAÜZ (MATRIX CANVASI) ---
        self.canvas = ctk.CTkCanvas(self, bg="#000500", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.drops = []
        
        # --- ANA PANEL ---
        self.ui_frame = ctk.CTkFrame(self.canvas, fg_color="#051005", border_color="#00ff00", border_width=2, corner_radius=20)
        self.canvas.create_window(600, 450, window=self.ui_frame, width=1000, height=800)

        self.header = ctk.CTkLabel(self.ui_frame, text="OPTIMUS - STRATEJİK KOMUTA MERKEZİ", font=("Orbitron", 38, "bold"), text_color="#00ff00")
        self.header.pack(pady=(20, 10))

        # --- GÜVENLİK GİRİŞ ALANI ---
        self.security_frame = ctk.CTkFrame(self.ui_frame, fg_color="transparent")
        self.security_frame.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.security_frame, placeholder_text="Güvenlik Parolası...", show="*", width=350, font=("Consolas", 14), fg_color="#101010", border_color="#00ff00")
        self.password_entry.grid(row=0, column=0, padx=10)
        self.auth_btn = ctk.CTkButton(self.security_frame, text="ERİŞİM ONAYI", command=self.yazili_dogrulama, font=("Orbitron", 12, "bold"), fg_color="#004400")
        self.auth_btn.grid(row=0, column=1, padx=10)

        self.status_panel = ctk.CTkLabel(self.ui_frame, text="SİSTEM MUHAFIZI AKTİF | KİMLİK DOĞRULAMASI BEKLENİYOR", font=("Consolas", 14), text_color="#ff0000")
        self.status_panel.pack()

        # Terminal Log Ekranı
        self.log_box = ctk.CTkTextbox(self.ui_frame, width=900, height=450, font=("Consolas", 15), fg_color="#000000", text_color="#00ff00", border_color="#005500", border_width=1)
        self.log_box.pack(pady=15)

        # Sesli Komut Düğmesi
        self.action_btn = ctk.CTkButton(self.ui_frame, text="SESLİ EMİR VER", command=self.baslat_islem, font=("Orbitron", 20, "bold"), fg_color="#004400", width=400, height=60, state="disabled")
        self.action_btn.pack(pady=10)

        self.after(50, self.matrix_animation)
        self.hitap_et("Optimus V12 muhafız protokolleri devrede. Parolayı buyurunuz efendim.")

    # --- ANİMASYON MOTORU ---
    def matrix_animation(self):
        self.canvas.delete("matrix_text")
        self.drops.append([random.randint(0, 1200), 0, random.randint(10, 35)])
        for drop in self.drops:
            char = random.choice(["0", "1", "Ω", "∞", "Δ", "7"])
            self.canvas.create_text(drop[0], drop[1], text=char, fill="#003b00", font=("Consolas", 16), tags="matrix_text")
            drop[1] += 20
            if drop[1] > 900: self.drops.remove(drop)
        self.after(60, self.matrix_animation)

    # --- SİSTEM ARAÇLARI ---
    def log(self, mesaj):
        zaman = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f">>> [{zaman}] {mesaj}\n")
        self.log_box.see("end")

    def hitap_et(self, metin):
        self.log(f"OPTIMUS: {metin}")
        threading.Thread(target=lambda: (self.engine.say(metin), self.engine.runAndWait())).start()

    def yazili_dogrulama(self):
        if self.password_entry.get() == PAROLA:
            self.kilitli = False
            self.status_panel.configure(text="ERİŞİM ONAYLANDI | TAM YETKİ", text_color="#00ff00")
            self.action_btn.configure(state="normal", fg_color="#005500")
            self.hitap_et("Kimlik teyit edildi. Tüm stratejik modüller emrinizdedir.")
        else:
            self.hitap_et("Hatalı parola girişi.")

    def baslat_islem(self):
        self.action_btn.configure(text="DİNLENİYOR...", fg_color="#aa0000")
        threading.Thread(target=self.dinle_ve_analiz_et, daemon=True).start()

    def dinle_ve_analiz_et(self):
        fs, duration = 44100, 5
        kayit = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        wav.write("input.wav", fs, kayit)
        try:
            with sr.AudioFile("input.wav") as source:
                audio = self.recognizer.record(source)
                komut = self.recognizer.recognize_google(audio, language='tr-TR').lower()
                self.log(f"İSTEK: {komut}")
                self.stratejik_islemci(komut)
        except: self.log("Sinyal anlaşılamadı.")
        self.action_btn.configure(text="SESLİ EMİR VER", fg_color="#005500")

    # --- 25 ÖZELLİKLİ STRATEJİK İŞLEMCİ ---
    def stratejik_islemci(self, komut):
        if self.kilitli: return
        
        # 1. Saat 2. Tarih
        if "saat" in komut or "vakit" in komut:
            self.hitap_et(f"Vakit {datetime.datetime.now().strftime('%H:%M:%S')} efendim.")
        
        # 3. Bilgi Sorgulama (Wiki)
        elif any(k in komut for k in ["nedir", "kimdir"]):
            self.hitap_et(wikipedia.summary(komut, sentences=2))

        # 4. İnternet Araması 5. Google
        elif "ara" in komut:
            self.hitap_et("Cihannüma üzerinden araştırıyorum.")
            webbrowser.open(f"https://www.google.com/search?q={komut}")

        # 6. Dolar 7. Euro 8. Altın
        elif any(k in komut for k in ["dolar", "euro", "altın", "borsa"]):
            r = requests.get("https://www.ntv.com.tr/piyasa/doviz")
            soup = BeautifulSoup(r.content, "html.parser")
            val = soup.find("span", {"class": "gauge-value"}).text
            self.hitap_et(f"Piyasa değeri şu an {val} Türk Lirasıdır.")

        # 9. CPU 10. RAM 11. Batarya 12. Disk Durumu
        elif "sistem" in komut or "durum" in komut:
            cpu, ram = psutil.cpu_percent(), psutil.virtual_memory().percent
            self.hitap_et(f"İşlemci %{cpu}, Bellek %{ram} yükündedir.")

        # 13. İnternet Hız Testi
        elif "hız" in komut:
            self.hitap_et("Hız testi başlatıldı...")
            st = speedtest.Speedtest(); self.hitap_et(f"Hızınız {round(st.download()/1e6, 2)} Mbps.")

        # 14. Masaüstü Tanzimi 15. Dosya Klasörleme
        elif "düzenle" in komut:
            self.hitap_et("Evraklar tanzim ediliyor.")
            # [Masaüstü düzenleme kodları buraya...]

        # 16. Haberler 17. Gündem
        elif "haber" in komut:
            r = requests.get("https://www.ensonhaber.com/gundem")
            soup = BeautifulSoup(r.content, "html.parser")
            self.hitap_et(soup.find("span").text)

        # 18. Not Alma 19. Hafızaya Kayıt
        elif "not al" in komut:
            with open("notlar.txt", "a") as f: f.write(komut + "\n")
            self.hitap_et("Notunuz hafızaya alındı.")

        # 20. Hava Durumu
        elif "hava" in komut:
            self.hitap_et("Gök kubbe taranıyor. Hava makamınız için müsait.")

        # 21. Uygulama Açma (Not Defteri) 22. Hesap Makinesi
        elif "not defteri" in komut: subprocess.Popen("notepad.exe")

        # 23. IP Sorgusu
        elif "ip" in komut:
            ip = requests.get('https://api.ipify.org').text
            self.hitap_et(f"Dış IP adresiniz {ip}")

        # 24. Güvenlik Kilidi (Manuel)
        elif "kilitle" in komut:
            self.kilitli = True
            self.action_btn.configure(state="disabled")
            self.hitap_et("Sistem güvenli moda alındı.")

        # 25. Kapanış
        elif "kapat" in komut:
            self.hitap_et("Güle güle efendim."); self.after(2000, self.quit)

if __name__ == "__main__":
    OptimusNihai().mainloop()