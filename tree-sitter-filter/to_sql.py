import json
import subprocess


def parse_ke_sexpr_atau_json(query_filter: str):
    """Menggunakan CLI tree-sitter untuk mem-parse query menjadi pohon XML/S-expr atau memakai binding Python."""
    pass

def ast_to_sql(node):
    tipe = node.type

    if tipe == "query":
        return ast_to_sql(node.named_children[0])

    if tipe == "parenthesized":
        sql, params = ast_to_sql(node.named_children[0])
        return f"({sql})", params

    if tipe == "not_expression":
        operand = node.child_by_field_name("operand")
        sql, params = ast_to_sql(operand)
        return f"NOT ({sql})", params

    if tipe in ("and_expression", "or_expression"):
        op_sql = "AND" if tipe == "and_expression" else "OR"
        left_sql, left_params = ast_to_sql(node.child_by_field_name("left"))
        right_sql, right_params = ast_to_sql(node.child_by_field_name("right"))
        return f"{left_sql} {op_sql} {right_sql}", left_params + right_params

    if tipe == "comparison":
        kolom = node.child_by_field_name("field").text.decode()
        op = node.child_by_field_name("operator").text.decode()
        val = ekstrak_nilai(node.child_by_field_name("value"))
        return f"{kolom} {op} ?", [val]

    if tipe == "contains_expression":
        kolom = node.child_by_field_name("field").text.decode()
        val = ekstrak_nilai(node.child_by_field_name("value"))
        return f"{kolom} LIKE ?", [f"%{val}%"]

    if tipe == "in_expression":
        kolom = node.child_by_field_name("field").text.decode()
        value_list = node.child_by_field_name("values")
        vals = [ekstrak_nilai(c) for c in value_list.named_children]
        placeholders = ", ".join(["?"] * len(vals))
        return f"{kolom} IN ({placeholders})", vals

    raise ValueError(f"Node tidak dikenal: {tipe}")


def ekstrak_nilai(node):
    teks = node.text.decode()
    if node.type == "string":
        return teks[1:-1]  # buang tanda kutip luar
    if node.type == "number":
        return float(teks) if "." in teks else int(teks)
    if node.type == "boolean":
        return teks == "true"
    return teks


if __name__ == "__main__":
    import tree_sitter_filter as tsfilter
    from tree_sitter import Language, Parser

    parser = Parser(Language(tsfilter.language()))
    contoh = b'status in ("open", "pending") and (priority >= 2 or title contains "invoice")'
    tree = parser.parse(contoh)

    where_clause, params = ast_to_sql(tree.root_node)
    print("Input DSL :", contoh.decode())
    print("SQL WHERE :", f"WHERE {where_clause}")
    print("Parameter :", params)