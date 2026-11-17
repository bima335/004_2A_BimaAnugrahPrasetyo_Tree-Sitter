import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

    for i, child in enumerate(node.children):
        if not child.is_named:
            continue
        nama_field = node.field_name_for_child(i)
        jelajah(child, kedalaman + 1, nama_field)


def jelajah_cursor(tree):
    cursor = tree.walk()
    kedalaman = 0
    selesai = False

    while not selesai:
        node = cursor.node
        if node.is_named:
            baris, kolom = node.start_point
            field = cursor.field_name
            label = f"{field}: " if field else ""
            print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

        if cursor.goto_first_child():
            if node.is_named:
                kedalaman += 1
            continue

        if cursor.goto_next_sibling():
            continue

        while True:
            if not cursor.goto_parent():
                selesai = True
                break
            if cursor.node.is_named:
                kedalaman -= 1
            if cursor.goto_next_sibling():
                break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python jelajah.py <file.py> [--cursor]")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        tree = parser.parse(f.read())

    if "--cursor" in sys.argv:
        jelajah_cursor(tree)
    else:
        jelajah(tree.root_node)