import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

potongan_kode = {
    "1. Fungsi": b'def sapa(nama):\n    return "Halo " + nama\n',
    "2. If-Else": b'if nilai >= 75:\n    status = "Lulus"\nelse:\n    status = "Ulang"\n',
    "3. Kelas": b'class Mahasiswa:\n    def info(self):\n        return self.nama\n',
}

for judul, kode in potongan_kode.items():
    print(f"=== {judul} ===")
    tree = parser.parse(kode)
    print(tree.root_node)
    print()

print("=== Cek Node Bernama vs Anonim (Potongan 1) ===")
tree_fungsi = parser.parse(potongan_kode["1. Fungsi"])
func_node = tree_fungsi.root_node.children[0]
print("Total children:", len(func_node.children))
print("Total named_children:", len(func_node.named_children))
for c in func_node.children:
    print(f"  {c.type!r:22} -> {'bernama' if c.is_named else 'anonim'}")

print("\nChild di dalam parameters:")
params_node = func_node.child_by_field_name("parameters")
for c in params_node.children:
    print(f"  {c.type!r:22} -> {'bernama' if c.is_named else 'anonim'}")

print("\n=== Uji Syntax Error (Hapus ':') ===")
kode_rusak = b'def sapa(nama)\n    return "Halo " + nama\n'
tree_rusak = parser.parse(kode_rusak)
print(tree_rusak.root_node)