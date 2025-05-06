import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Chrome tarayıcıyı başlat (arka planda çalışsın)
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# 1️⃣ Nöbetçi Eczaneleri Çek
def get_eczaneler(ilce="kadikoy"):
    try:
        driver.get(f"https://www.eczaneler.gen.tr/nobetci-{ilce}")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        eczaneler = []
        for eczane in soup.select(".table.table-hover tr")[1:6]:  # İlk 5 eczane
            ad = eczane.select("td")[1].text.strip()
            adres = eczane.select("td")[2].text.strip()
            telefon = eczane.select("td")[3].text.strip()
            eczaneler.append({"ad": ad, "adres": adres, "telefon": telefon})
        
        return eczaneler
    except:
        return []

# 2️⃣ Su Kesintileri Çek (İSKİ)
def get_su_kesintileri():
    try:
        url = "https://www.iski.istanbul/web/tr-TT/kesinti"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        kesintiler = []
        for kesinti in soup.select(".kesinti-listesi .card")[:5]:  # İlk 5 kesinti
            bolge = kesinti.select(".card-title")[0].text.strip()
            tarih = kesinti.select(".card-text")[0].text.strip()
            kesintiler.append({"bolge": bolge, "tarih": tarih})
        
        return kesintiler
    except:
        return []

# 3️⃣ Elektrik Kesintileri Çek (TEDAŞ)
def get_elektrik_kesintileri():
    try:
        driver.get("https://www.tedas.gov.tr/kesinti-bilgisi")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        kesintiler = []
        for kesinti in soup.select(".kesinti-listesi .card")[:5]:  # İlk 5 kesinti
            ilce = kesinti.select(".card-title")[0].text.strip()
            saat = kesinti.select(".card-text")[0].text.strip()
            kesintiler.append({"ilce": ilce, "saat": saat})
        
        return kesintiler
    except:
        return []

# 4️⃣ Akaryakıt Fiyatları Çek (Petrol Ofisi)
def get_akaryakit():
    try:
        url = "https://www.petrolofisi.com.tr/akaryakit-fiyatlari"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        fiyatlar = {
            "benzin": soup.select(".benzin-fiyat")[0].text.strip(),
            "dizel": soup.select(".dizel-fiyat")[0].text.strip()
        }
        return fiyatlar
    except:
        return {}

# 5️⃣ Döviz Kurları Çek (TCMB)
def get_doviz():
    try:
        url = "https://www.tcmb.gov.tr/kurlar/today.xml"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        kurlar = {
            "dolar": soup.select("currency[kod='USD'] forexbuying")[0].text,
            "euro": soup.select("currency[kod='EUR'] forexbuying")[0].text
        }
        return kurlar
    except:
        return {}

# Tarayıcıyı kapat
driver.quit()
