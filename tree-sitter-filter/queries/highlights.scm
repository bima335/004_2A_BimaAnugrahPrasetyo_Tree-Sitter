; Kata kunci logika & operator kata
[
  "and"
  "or"
  "not"
  "in"
  "contains"
] @keyword

; Operator perbandingan
[
  "="
  "!="
  ">"
  "<"
  ">="
  "<="
] @operator

; Nilai literal
(string) @string
(number) @number
(boolean) @constant.builtin

; Nama field pada berbagai ekspresi
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)

; Tanda baca
[
  "("
  ")"
  ","
] @punctuation.delimiter