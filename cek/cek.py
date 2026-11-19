import sys
from pathlib import Path
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
from tree_sitter import Language, Parser, Query, QueryCursor

PY_LANG = Language(tspython.language())
JS_LANG = Language(tsjavascript.language())

parser_py = Parser(PY_LANG)
parser_js = Parser(JS_LANG)

# Query untuk Python
Q_PY_TODO = Query(PY_LANG, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_PY_FUNC = Query(PY_LANG, "(function_definition name: (identifier) @nama) @fungsi")

# Query untuk JavaScript (Pengayaan)
Q_JS_TODO = Query(JS_LANG, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_JS_FUNC = Query(
    JS_LANG,
    """
    [
      (function_declaration name: (identifier) @nama) @fungsi
      (method_definition name: (property_identifier) @nama) @fungsi
    ]
    """,
)

FOLDER_ABAIKAN = {".git", "venv", ".venv", "__pycache__", "node_modules", ".idea", ".vscode"}
BATAS_BARIS_FUNGSI = 30


def cari_error_pertama(node):
    """Mencari node pertama yang is_error atau is_missing secara rekursif (DFS)."""
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error_pertama(child)
        if hasil is not None:
            return hasil
    return None


def cek_file(path: Path):
    ekstensi = path.suffix.lower()
    if ekstensi == ".py":
        parser = parser_py
        q_todo = Q_PY_TODO
        q_func = Q_PY_FUNC
    elif ekstensi == ".js":
        parser = parser_js
        q_todo = Q_JS_TODO
        q_func = Q_JS_FUNC
    else:
        return

    tree = parser.parse(path.read_bytes())
    root = tree.root_node

    # Fitur 1: Komentar TODO atau FIXME
    hasil_todo = QueryCursor(q_todo).captures(root).get("c", [])
    for node in hasil_todo:
        baris = node.start_point[0] + 1
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO/FIXME] {path}:{baris}: {teks}")

    # Fitur 2: Fungsi lebih dari 30 baris
    for _, cap in QueryCursor(q_func).matches(root):
        fungsi_nodes = cap.get("fungsi", [])
        nama_nodes = cap.get("nama", [])
        if fungsi_nodes and nama_nodes:
            f_node = fungsi_nodes[0]
            n_node = nama_nodes[0]
            jumlah_baris = f_node.end_point[0] - f_node.start_point[0] + 1
            if jumlah_baris > BATAS_BARIS_FUNGSI:
                nama_fungsi = n_node.text.decode(errors="replace")
                baris_mulai = f_node.start_point[0] + 1
                print(
                    f"[FUNGSI PANJANG] {path}:{baris_mulai}: "
                    f"fungsi '{nama_fungsi}' panjangnya {jumlah_baris} baris (> {BATAS_BARIS_FUNGSI})"
                )

    # Fitur 3: File dengan syntax error
    if root.has_error:
        node_err = cari_error_pertama(root)
        if node_err is not None:
            baris_err = node_err.start_point[0] + 1
            kolom_err = node_err.start_point[1]
            jenis = f"MISSING {node_err.type}" if node_err.is_missing else "ERROR"
            print(f"[SYNTAX ERROR] {path}:{baris_err}:{kolom_err}: ditemukan node {jenis}")
        else:
            print(f"[SYNTAX ERROR] {path}: pohon mengandung error sintaks")


def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python cek.py <folder_target>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: Folder '{target}' tidak ditemukan.")
        sys.exit(1)

    total_file = 0
    for pola in ("*.py", "*.js"):
        for path in target.rglob(pola):
            if any(bagian in FOLDER_ABAIKAN for bagian in path.parts):
                continue
            total_file += 1
            cek_file(path)

    print(f"\nSelesai memindai {total_file} file di '{target}'.")


if __name__ == "__main__":
    main()