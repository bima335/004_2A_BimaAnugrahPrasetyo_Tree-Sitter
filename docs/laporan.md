LAPORAN TUGAS AWAL: MEMAHAMI TREE-SITTER

* Nama: Bima Anugrah Prasetyo  
* NIM: 251524004  
* Repositori : [https\://github.com/bima335/004\_2A\_BimaAnugrahPrasetyo\_Tree-Sitter](https://github.com/bima335/004_2A_BimaAnugrahPrasetyo_Tree-Sitter)   
* Catatan: Output dicantumkan pada file terpisah agar bisa memenuhi syarat maksimal 3 halaman.

### 1\. Ringkasan Pelaksanaan & Hasil Tiap Tugas

#### Tugas 1 — Membaca Pohon (tugas1-3/t1.py)

* Pelaksanaan: Melakukan parsing pada 3 potongan kode Python (fungsi sapa, percabangan if/else, dan kelas Mahasiswa) menggunakan tree-sitter-python.  
* Perbandingan Prediksi vs Aktual: Struktur hierarki besar (module [![\\rightarrow][image1]](https://saxarona.github.io/mathjax-viewer/?input=%5Crightarrow#0) function\_definition / if\_statement / class\_definition) dan label *field* (name:, parameters:, body:, condition:, consequence:, alternative:) sesuai dengan prediksi tulisan tangan. Perbedaan kecil ditemukan pada node (string), yang di versi grammar terbaru memecah isinya menjadi (string\_start), (string\_content), dan (string\_end).  
* Node Bernama vs Anonim & Error Recovery: Pada function\_definition, children berjumlah 5 (mencakup token literal anonim "def" dan ":"), sedangkan named\_children hanya berjumlah 3 (identifier, parameters, block). Ketika titik dua : dihapus pada definisi fungsi, parser tetap melanjutkan proses parsing dan menyisipkan node (MISSING ":").

#### Tugas 2 — Penjelajah Node (tugas1-3/jelajah.py)

* Pelaksanaan: Mengimplementasikan fungsi traversal rekursif Preorder (DFS) untuk mencetak seluruh node bernama lengkap dengan indentasi kedalaman, posisi \[baris:kolom\] (berbasis 1), dan nama *field*. Skrip diuji secara bertahap mulai dari kecil.py hingga file simulasi inventaris sepanjang 115 baris (contoh\_100\_baris.py) serta dibandingkan dengan mode pengayaan TreeCursor (--cursor).

#### Tugas 3 — Query Pertama (tugas1-3/q.py & \*.scm)

* Pelaksanaan: Setelah memeriksa struktur AST lewat jelajah.py, disusun empat file query S-expression: fungsi.scm (menangkap pasangan @nama dan @params menggunakan matches() untuk menghitung named\_child\_count), print\_calls.scm (memfilter pemanggilan print dengan predikat \#eq?), imports.scm (menangani import, import ... as ..., dan from ... import ...), serta pengayaan docstring.scm. Seluruh output pada uji\_t3.py cocok dengan hitungan manual (3 fungsi, 3 pemanggilan print, 4 modul impor, dan 2 docstring).

#### Tugas 4 — Grammar DSL Filter (tree-sitter-filter/grammar.js)

* Pelaksanaan: Membangun grammar bahasa query filter untuk halaman admin aplikasi enterprise yang mendukung tipe data string, angka, boolean, operator perbandingan (=, \!=, \>, \<, \>=, \<=), operator logika (and, or, not), pengelompokan tanda kurung, serta operator in (in\_expression \+ value\_list) dan contains (contains\_expression). Prioritas operator diatur melalui prec.left (or level 1, and level 2, not level 3\) dan word: \$ \=\> \$.identifier agar kata kunci tidak tertukar dengan nama kolom. Seluruh 7 kasus uji pada test/corpus/dasar.txt lulus saat dijalankan dengan tree-sitter test.

#### Tugas 5 — Highlight DSL Filter (tree-sitter-filter/queries/highlights.scm)

* Pelaksanaan: Mengatur direktori parser pada konfigurasi CLI (tree-sitter init-config) dan menghubungkan ekstensi .filter dengan queries/highlights.scm di tree-sitter.json. Aturan capture diterapkan untuk kata kunci (@keyword), operator (@operator), string (@string), angka (@number), boolean (@constant.builtin), dan nama kolom (@property), menghasilkan pewarnaan sintaks yang akurat pada contoh.filter.

#### Tugas 6 — Mini Proyek CLI Pemeriksa Kode (cek/cek.py)

* Pelaksanaan: Membangun skrip CLI cek.py untuk memindai file .py (dan pengayaan .js) secara rekursif serta melaporkan komentar TODO/FIXME, fungsi dengan panjang \> 30 baris, dan file yang memiliki error sintaks (root\_node.has\_error disertai pencarian DFS lokasi baris ERROR/MISSING pertama). Pengujian dilakukan pada folder lokal uji/ dan repositori open source pallets/click, serta diverifikasi secara manual pada 2 file acak dengan tingkat kecocokan 100%.

### 2\. Kendala Teknis dan Solusinya

| No | Tugas | Kendala yang Dihadapi | Solusi yang Diterapkan |
| :---- | :---- | :---- | :---- |
| 1 | Tugas 2 | Label *field* (left:, right:) awalnya tidak muncul saat mencetak anak node. | Menggunakan enumerate(node.children) sebelum memfilter node.is\_named agar indeks yang dikirim ke node.field\_name\_for\_child(i) tetap sesuai dengan posisi asli seluruh child. |
| 2 | Tugas 4 | Muncul pesan *Unresolved conflict* saat menambahkan aturan or\_expression bersamaan dengan and\_expression. | Menambahkan prioritas dan asosiativitas kiri menggunakan prec.left(1, ...) pada or\_expression dan prec.left(2, ...) pada and\_expression. |
| 3 | Tugas 4 | Gagal mengompilasi binding Python lokal (pip install \--no-build-isolation \-e .) karena ModuleNotFoundError: No module named 'setuptools'. | Menginstal setuptools dan wheel, serta menyediakan alternatif parsing menggunakan tree-sitter parse \--xml via subprocess pada skrip pengayaan to\_sql.py. |
| 4 | Tugas 5 | tree-sitter highlight contoh.filter awalnya tidak menampilkan warna karena parser belum dikenali CLI. | Memperbaiki path parser-directories di config.json agar menunjuk ke folder induk (004\_2A\_BimaAnugrahPrasetyo\_Tree-Sitter) dan memastikan file-types: \["filter"\] tercantum di tree-sitter.json. |

### 3\. Catatan Penggunaan AI

Dalam pengerjaan rangkaian tugas ini, AI digunakan sebagai asisten konsultasi penulisan kode dan debugging. Sesuai ketentuan verifikasi kritis, berikut adalah catatan permintaan, temuan kesalahan pada keluaran AI, dan bukti pembuktiannya:

* Tugas 3 (q.py — Penyesuaian API py-tree-sitter 0.25):  
  * Permintaan ke AI: Meminta kerangka skrip q.py yang secara otomatis mendeteksi apakah file .scm menggunakan mode matches() atau captures() berdasarkan nama capture di dalam query.  
  * Kesalahan/Kekurangan AI yang Ditemukan: AI menyarankan pengecekan if "nama" in query.capture\_names and "params" in query.capture\_names:. Pada pustaka py-tree-sitter versi 0.25+, properti query.capture\_names sudah dihapus/tidak tersedia.  
  * Bukti Verifikasi: Saat python q.py uji\_t3.py fungsi.scm dijalankan di PowerShell, muncul error AttributeError: 'tree\_sitter.Query' object has no attribute 'capture\_names'. Did you mean: 'capture\_name'?. Kode kemudian diperbaiki dengan melakukan iterasi indeks \[query.capture\_name(i) for i in range(query.capture\_count)\], yang setelah dijalankan ulang berhasil mengekstrak seluruh fungsi dan jumlah parameternya dengan benar.  
* Tugas 4 (to\_sql.py — Asumsi Ketersediaan Modul Binding Lokal):  
  * Permintaan ke AI: Meminta kode pengayaan untuk mengonversi AST bahasa filter menjadi klausa SQL WHERE berparameter (?).  
  * Kesalahan/Kekurangan AI yang Ditemukan: AI langsung menulis import tree\_sitter\_filter as tsfilter seolah-olah grammar lokal otomatis terdaftar sebagai paket Python setelah tree-sitter generate, padahal grammar custom harus dikompilasi dan di-install terlebih dahulu ke environment Python.  
  * Bukti Verifikasi: Eksekusi python to\_sql.py menghasilkan ModuleNotFoundError: No module named 'tree\_sitter\_filter'. Masalah diverifikasi dan diselesaikan dengan memasang paket lokal maupun memanfaatkan output XML dari CLI tree-sitter parse \--xml.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAICAYAAADwdn+XAAAAI0lEQVR4XmNgIAFINFj8RxcjCVBsAAgMDkMoMmDgNIMANgMAtP8OeZu9DgEAAAAASUVORK5CYII=>