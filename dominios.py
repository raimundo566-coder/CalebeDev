# ARQUIVO: dominios.py
# Aqui ficam apenas as DEFINIÇÕES (Quem é o quê).

import webbrowser
import time


class PontoTuristico:
    def __init__(self, nome, tipo, gps_tuple, desc_pt, desc_en, eh_secreto):
        self.nome = nome
        self.tipo = tipo
        self.gps = gps_tuple
        self.desc_pt = desc_pt
        self.desc_en = desc_en
        self.secreto = eh_secreto

    def mostrar_na_tela(self, idioma):
        print("--------------------------------------------------")
        if self.secreto:
            print("💎 LOCAL SECRETO / SECRET SPOT 💎")

        print(f"📍 {self.nome} | Tipo: {self.tipo}")

        if idioma == "EN":
            print(f"📝 Info: {self.desc_en}")
        else:
            print(f"📝 Info: {self.desc_pt}")

        print(f"🛰️ GPS Fixo: {self.gps}")

    def abrir_no_mapa(self):
        # Link corrigido para funcionar melhor
        link = f"https://www.google.com/maps/search/?api=1&query={self.gps[0]},{self.gps[1]}"
        print(f"\n🚀 Abrindo rota para {self.nome}...")
        time.sleep(1.5)
        webbrowser.open(link)