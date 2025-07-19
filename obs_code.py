from OBS_db import ogrenciler, notlar

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QListWidget, QStackedWidget, QLabel, QTableWidget, QLineEdit, QHBoxLayout, QTableWidgetItem
)
from obs_ınterface import OgrenciEklePenceresi
from bson import ObjectId

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Öğrenci Bilgi Sistemi")
        self.setGeometry(100, 100, 600, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.ana_sayfa_widget = QWidget()
        self.detay_sayfa_widget = QWidget()

        self.init_ana_sayfa()
        self.init_detay_sayfa()

        self.stack.addWidget(self.ana_sayfa_widget)   # index 0
        self.stack.addWidget(self.detay_sayfa_widget) # index 1

        self.stack.setCurrentIndex(0)

    def init_ana_sayfa(self):
        self.student_list = QListWidget()
        self.student_list.itemDoubleClicked.connect(self.ac_not_sayfasi)

        self.ekle_buton = QPushButton("Öğrenci Ekle")
        self.ekle_buton.clicked.connect(self.ogrenci_ekle)

        layout = QVBoxLayout()
        layout.addWidget(self.student_list)
        layout.addWidget(self.ekle_buton)

        self.ana_sayfa_widget.setLayout(layout)

        self.ogrencileri_yukle()

    def init_detay_sayfa(self):
        self.label_isim = QLabel("Öğrenci Bilgisi")
        self.geri_buton = QPushButton("Geri Dön")
        self.geri_buton.clicked.connect(self.ana_sayfaya_don)

        # 🔸 Not Tablosu
        self.not_tablosu = QTableWidget()
        self.not_tablosu.setColumnCount(6)
        self.not_tablosu.setHorizontalHeaderLabels(["Ders", "Vize", "Final", "Ort.", "Harf", "Durum"])

        # 🔸 Not Ekleme Alanları
        self.input_ders = QLineEdit()
        self.input_ders.setPlaceholderText("Ders Adı")

        self.input_vize = QLineEdit()
        self.input_vize.setPlaceholderText("Vize Notu")

        self.input_final = QLineEdit()
        self.input_final.setPlaceholderText("Final Notu")

        self.kaydet_not_btn = QPushButton("Notu Kaydet")
        self.kaydet_not_btn.clicked.connect(self.not_kaydet)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_isim)
        layout.addWidget(self.not_tablosu)

        hbox = QHBoxLayout()
        hbox.addWidget(self.input_ders)
        hbox.addWidget(self.input_vize)
        hbox.addWidget(self.input_final)
        hbox.addWidget(self.kaydet_not_btn)
        layout.addLayout(hbox)

        layout.addWidget(self.geri_buton)
        self.detay_sayfa_widget.setLayout(layout)

    def ogrencileri_yukle(self):
        self.student_list.clear()
        for ogrenci in ogrenciler.find():
            self.student_list.addItem(f"{ogrenci['_id']} - {ogrenci['isim']}")

    def ogrenci_ekle(self):
        pencere = OgrenciEklePenceresi(self.ogrencileri_yukle)
        pencere.exec_()

    def ac_not_sayfasi(self, item):
        satir = item.text()
        self.secili_ogrenci_id, isim = satir.split(" - ", 1)
        self.label_isim.setText(f"Öğrenci: {isim}")
        self.notlari_goster()
        self.stack.setCurrentIndex(1)

    def notlari_goster(self):
        self.not_tablosu.setRowCount(0)
        filtre = {"ogrenci_id": ObjectId(self.secili_ogrenci_id)}
        for not_belge in notlar.find(filtre):
            satir = self.not_tablosu.rowCount()
            self.not_tablosu.insertRow(satir)
            self.not_tablosu.setItem(satir, 0, QTableWidgetItem(not_belge["ders_adi"]))
            self.not_tablosu.setItem(satir, 1, QTableWidgetItem(str(not_belge["vize"])))
            self.not_tablosu.setItem(satir, 2, QTableWidgetItem(str(not_belge["final"])))
            self.not_tablosu.setItem(satir, 3, QTableWidgetItem(str(not_belge["ortalama"])))
            self.not_tablosu.setItem(satir, 4, QTableWidgetItem(not_belge["harf"]))
            self.not_tablosu.setItem(satir, 5, QTableWidgetItem(not_belge["durum"]))

    def not_kaydet(self):
        ders = self.input_ders.text().strip()
        try:
            vize = int(self.input_vize.text())
            final = int(self.input_final.text())
        except ValueError:
            print("Hatalı not girişi")
            return

        ort = round((vize * 0.4) + (final * 0.6))
        harf = self.harf_hesapla(ort)
        durum = "Geçti" if ort >= 60 else "Kaldı"

        belge = {
            "ogrenci_id": ObjectId(self.secili_ogrenci_id),
            "ders_adi": ders,
            "vize": vize,
            "final": final,
            "butunleme": None,
            "ortalama": ort,
            "harf": harf,
            "durum": durum
        }

        notlar.insert_one(belge)
        self.notlari_goster()

        self.input_ders.clear()
        self.input_vize.clear()
        self.input_final.clear()

    def harf_hesapla(self, ort):
        if ort >= 90:
            return "AA"
        elif ort >= 85:
            return "BA"
        elif ort >= 80:
            return "BB"
        elif ort >= 75:
            return "CB"
        elif ort >= 60:
            return "CC"
        elif ort >= 50:
            return "DC"
        elif ort >= 40:
            return "DD"
        else:
            return "FF"

    def ana_sayfaya_don(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
