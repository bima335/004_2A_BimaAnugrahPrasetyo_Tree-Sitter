import os
import sys as sistem
from pathlib import Path
from datetime import datetime, timedelta


def salam(nama: str, sapaan: str = "Halo"):
    """Mengembalikan teks sapaan untuk pengguna."""
    pesan = f"{sapaan}, {nama}!"
    print(pesan)
    return pesan


def hitung_luas(panjang, lebar):
    # Bukan docstring karena hanya komentar
    luas = panjang * lebar
    print("Luas dihitung:", luas)
    return luas


def tanpa_parameter():
    """Fungsi tanpa parameter sama sekali."""
    print("Selesai.")