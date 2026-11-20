1. **PROPOSAL PROYEK: ARCHGUARD-TS (ONE-PAGER)**  
2. **Judul & Deskripsi Singkat**  
   **ArchGuard-TS:** Linter berbasis Tree-sitter untuk mengecek batasan arsitektur berlapis (*Layered Architecture*) dan keamanan log/query pada backend TypeScript enterprise (Express/NestJS).  
3. **Latar Belakang Masalah**  
   Pengembang sering melanggar batasan arsitektur (misal: *Controller* langsung memanggil *Repository*) atau meninggalkan console.log data sensitif. Hal ini merusak pemisahan tanggung jawab (*SoC*) dan memicu risiko keamanan yang kerap terlewat saat *code review* manual.  
4. **Keunggulan Solusi (Tree-sitter vs. AI/Grep)**  
   1\. **Deterministik & Bebas Biaya Token:** Berbeda dengan AI yang probabilistik dan berbiaya tinggi, Tree-sitter memberikan hasil konsisten tanpa biaya.  
   2\. **Cepat & Akurat:** Memahami struktur AST kode sehingga membedakan impor/eksekusi aktif dari komentar/string literal, cocok untuk pipeline CI/CD.  
5. **Spesifikasi Teknis & Target**  
   • **Bahasa/Framework Target:** TypeScript / JavaScript (Node.js — Express & NestJS).  
   • **Grammar:** tree-sitter-typescript & tree-sitter-javascript.  
   • **Aturan Utama:** Impor lintas-layer ilegal (Controller \$\\rightarrow\$ Repository), Pemanggilan log data sensitif, dan Konkatenasi SQL mentah.  
6. **Aturan & Contoh Query Tree-sitter (S-expression)**  
   • **Deteksi Impor Repository di Controller:**  
7. Scheme

```
(import_statement
  source: (string
    (string_fragment) @source_path)
  (#match? @source_path "repositories/"))
```

8. • **Deteksi Pemanggilan console.log:**

```
(call_expression
  function: (member_expression
    object: (identifier) @obj
    property: (property_identifier) @prop)
  (#eq? @obj "console")
  (#eq? @prop "log"))
```

9.   
10. **Output CLI & Evaluasi**  
    • **Bentuk Output:** CLI Python (archguard.py \<dir\>) dengan opsi \--json. Mengembalikan *exit code* 1 jika ditemukan pelanggaran guna memblokir CI/CD pipeline.  
    • **Rencana Evaluasi:** Pengujian pada 2 repositori open-source TypeScript dan *synthetic test suite*. Mengukur presisi melalui verifikasi manual pada 20 sampel acak.  
11. **Rencana Kerja 5 Minggu**  
    • **M1:** Spesifikasi aturan & pengumpulan dataset repositori.  
    • **M2:** Parser Tree-sitter & query impor lintas-layer.  
    • **M3:** Aturan deteksi log sensitif & raw SQL concatenation.  
    • **M4:** Formatter CLI, opsi JSON, dan unit testing.  
    • **M5:** Evaluasi skala penuh, dokumentasi, dan demo proyek.  
    • **Risiko & Mitigasi:** Perbedaan AST antara .ts dan .tsx dimitigasi dengan memisahkan handler language\_typescript() dan language\_tsx().

