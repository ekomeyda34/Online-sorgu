from flask import Flask, render_template
from scraper import get_eczaneler, get_su_kesintileri, get_elektrik_kesintileri, get_akaryakit, get_doviz
import threading
import time

app = Flask(__name__)

# Verileri saklamak için
veriler = {
    "eczaneler": [],
    "su_kesintileri": [],
    "elektrik_kesintileri": [],
    "akaryakit": {},
    "doviz": {}
}

# Her 1 saatte bir verileri güncelle
def verileri_guncelle():
    while True:
        veriler["eczaneler"] = get_eczaneler()
        veriler["su_kesintileri"] = get_su_kesintileri()
        veriler["elektrik_kesintileri"] = get_elektrik_kesintileri()
        veriler["akaryakit"] = get_akaryakit()
        veriler["doviz"] = get_doviz()
        time.sleep(3600)  # 1 saat bekle

# Arka planda çalıştır
thread = threading.Thread(target=verileri_guncelle)
thread.daemon = True
thread.start()

# Ana sayfa
@app.route("/")
def ana_sayfa():
    return render_template("index.html", veriler=veriler)

if __name__ == "__main__":
    app.run(debug=True)
