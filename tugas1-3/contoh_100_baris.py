import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Produk:
    kode: str
    nama: str
    harga: float
    stok: int
    kategori: str = "Umum"
    riwayat: List[str] = field(default_factory=list)

    def nilai_aset(self) -> float:
        return self.harga * self.stok

    def tambah_stok(self, jumlah: int, catatan: str = "") -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah penambahan stok harus positif")
        self.stok += jumlah
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.riwayat.append(f"[{waktu}] +{jumlah} ({catatan})")

    def kurangi_stok(self, jumlah: int) -> bool:
        if jumlah <= 0 or jumlah > self.stok:
            return False
        self.stok -= jumlah
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.riwayat.append(f"[{waktu}] -{jumlah}")
        return True


class Gudang:
    def __init__(self, nama_gudang: str):
        self.nama_gudang = nama_gudang
        self.katalog: Dict[str, Produk] = {}

    def daftarkan_produk(self, produk: Produk) -> None:
        if produk.kode in self.katalog:
            print(f"Peringatan: Produk {produk.kode} diperbarui.")
        self.katalog[produk.kode] = produk

    def cari_produk(self, kode: str) -> Optional[Produk]:
        return self.katalog.get(kode)

    def produk_stok_menipis(self, batas: int = 5) -> List[Produk]:
        return [p for p in self.katalog.values() if p.stok <= batas]

    def total_nilai_gudang(self) -> float:
        total = 0.0
        for item in self.katalog.values():
            total += item.nilai_aset()
        return total

    def ekspor_laporan_json(self, path_file: str) -> None:
        data = {
            "gudang": self.nama_gudang,
            "total_item": len(self.katalog),
            "total_aset": self.total_nilai_gudang(),
            "daftar": [
                {
                    "kode": p.kode,
                    "nama": p.nama,
                    "stok": p.stok,
                    "harga": p.harga,
                }
                for p in self.katalog.values()
            ],
        }
        try:
            with open(path_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Laporan berhasil disimpan ke {path_file}")
        except OSError as err:
            print(f"Gagal menulis file: {err}")


def jalankan_simulasi():
    gudang = Gudang("Gudang Utama Bandung")
    daftar_awal = [
        Produk("PRD-001", "Laptop Kerja 14 Inch", 12500000.0, 8, "Elektronik"),
        Produk("PRD-002", "Monitor IPS 24 Inch", 2100000.0, 3, "Elektronik"),
        Produk("PRD-003", "Keyboard Mekanikal", 750000.0, 15, "Aksesoris"),
        Produk("PRD-004", "Mouse Wireless", 250000.0, 2, "Aksesoris"),
    ]

    for p in daftar_awal:
        gudang.daftarkan_produk(p)

    target = gudang.cari_produk("PRD-002")
    if target is not None:
        target.tambah_stok(4, "Restock supplier")

    berhasil = gudang.kurangi_stok("PRD-004") if hasattr(gudang, "kurangi_stok") else False
    if not berhasil and target:
        target.kurangi_stok(1)

    menipis = gudang.produk_stok_menipis(batas=5)
    print(f"Jumlah produk stok menipis: {len(menipis)}")
    for item in menipis:
        print(f"- {item.kode}: {item.nama} (sisa {item.stok})")

    print(f"Total nilai aset: Rp{gudang.total_nilai_gudang():,.2f}")


if __name__ == "__main__":
    jalankan_simulasi()