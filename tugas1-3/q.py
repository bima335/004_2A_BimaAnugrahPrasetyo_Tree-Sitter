import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)


def jalankan_query(file_kode, file_scm):
    kode = open(file_kode, "rb").read()
    pola = open(file_scm, "r", encoding="utf-8").read()
    tree = parser.parse(kode)
    query = Query(PY, pola)
    cursor = QueryCursor(query)

    daftar_capture = [query.capture_name(i) for i in range(query.capture_count)]

    # Jika query menangkap @nama dan @params (Tugas 3 butir 1), gunakan matches()
    if "nama" in daftar_capture and "params" in daftar_capture:
        print(f"=== Hasil Matches: {file_scm} pada {file_kode} ===")
        for _, cap in cursor.matches(tree.root_node):
            nama_nodes = cap.get("nama", [])
            params_nodes = cap.get("params", [])
            if nama_nodes and params_nodes:
                nama = nama_nodes[0].text.decode(errors="replace")
                baris = nama_nodes[0].start_point[0] + 1
                jumlah_param = params_nodes[0].named_child_count
                print(f"Fungsi '{nama}' (baris {baris}) -> {jumlah_param} parameter")
    else:
        print(f"=== Hasil Captures: {file_scm} pada {file_kode} ===")
        hasil = cursor.captures(tree.root_node)
        for nama_capture, nodes in hasil.items():
            for n in nodes:
                teks = n.text.decode(errors="replace").strip()
                baris = n.start_point[0] + 1
                print(f"@{nama_capture:<10} baris {baris:<3}: {teks}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Penggunaan: python q.py <file_kode.py> <file_query.scm>")
        sys.exit(1)

    jalankan_query(sys.argv[1], sys.argv[2])