from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from OBS_db import ogrenciler

class OgrenciEklePenceresi(QDialog):
    def __init__(self, liste_guncelle_fonksiyonu):
        super().__init__()
        self.setWindowTitle("Yeni Öğrenci Ekle")
        self.setGeometry(200, 200, 300, 150)

        self.liste_guncelle = liste_guncelle_fonksiyonu

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Öğrenci İsmi:")
        self.layout.addWidget(self.label)

        self.input_isim = QLineEdit()
        self.layout.addWidget(self.input_isim)

        self.kaydet_btn = QPushButton("Kaydet")
        self.kaydet_btn.clicked.connect(self.kaydet)
        self.layout.addWidget(self.kaydet_btn)

    def kaydet(self):
        isim = self.input_isim.text().strip()
        if isim:
            ogrenciler.insert_one({"isim": isim})
            self.liste_guncelle()
            self.accept()
