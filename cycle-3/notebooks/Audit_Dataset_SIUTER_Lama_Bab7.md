# Audit awal dataset SIUTER lama untuk Bab 7

Tanggal pemeriksaan: 1 November 2026. Sumber: berkas `siuter_dataset.csv` yang disampaikan peneliti dalam percakapan. Pemeriksaan bersifat deskriptif; data sumber tidak diubah. Tidak ada baris mentah, alamat IP, sesi, atau identifier yang disalin ke catatan ini.

## Identitas dan isi

- SHA-256: `38bdd950cdab6fd5fc0c57cea1a408d4a3e7da326c6d5bbbf127bea2b81d4900`.
- 480.461 baris dan 32 kolom.
- Timestamp minimum 2025-11-24 21:44:33 dan maksimum 2026-04-11 08:03:50; zona waktu tidak dinyatakan di CSV. Semua timestamp terbaca oleh pandas. Baris tidak seluruhnya berurutan menurut waktu.
- Label `anomaly_label`: 0 = 456.743 dan 1 = 23.718 (4,937% dari seluruh baris).
- Kolom `anomaly_reason` tidak kosong pada 23.718 baris, persis sama dengan baris berlabel 1. Ini menunjukkan alasan dan label sangat terkait, bukan bukti bahwa input tersebut telah digunakan model.
- Ada 15.730 baris yang sama persis pada seluruh 32 kolom setelah kemunculan pertama. Catatan: baris identik tidak otomatis kejadian log yang sama; jangan hapus tanpa identitas sumber.
- Kolom `ip_address` kosong pada sekitar 98,5% baris, `session_id` 93,6%, dan `user_id_hash` 99,2%. Kosong dapat bersifat struktural, tidak otomatis bukti log tidak sah.

## Label dan fitur: pemeriksaan penuh dataset sebelum pembagian

| is_error | Label 0 | Label 1 |
|---|---:|---:|
| 0 | 456.687 | 2.096 |
| 1 | 56 | 21.622 |

Semua 21.622 baris dengan `log_level=ERROR` berlabel 1, sebagaimana 492 baris WARNING. Semua 56 baris EMERGENCY berlabel 0 pada dataset ini; makna tersebut harus ditelusuri dalam proses pembentukan label, bukan dianggap penilaian keamanan substantif. Nilai seperti `error_level`, `db_error_suspicious`, dan `warning_level` muncul dalam alasan label 1. Tabel adalah deskripsi seluruh data, bukan kinerja model atau hasil data uji independen.

## Pencocokan terhadap notebook Siklus 3

Notebook `ER_CyRIS_Siklus3_Corrected_Validation_v3_5_Gradio_Fixed2_UI.ipynb`, sumber https://drive.google.com/file/d/1P94yhtXiJzR5lrh2FSZsbCfDYq33C-87/view , mengonfigurasi label `anomaly_label`, timestamp `timestamp`, dan 11 fitur dasar: `is_dosen`, `semester_aktif`, `hour`, `minute`, `day_of_week`, `is_weekend`, `is_off_hours`, `is_error`, `has_context`, `sess_events_per_hour`, `ip_events_per_hour`. Seluruh 13 kolom wajib tersebut ditemukan dalam CSV. Kecocokan nama kolom belum membuktikan file identik dengan data yang dipakai pada run lama; memerlukan checksum atau manifest dan output lama.

Notebook menggunakan `anomaly_reason` sebagai metadata/referensi, bukan di daftar 11 fitur dasar. Namun `is_error`, `is_off_hours`, dan `ip_events_per_hour` berada di fitur dasar dan berpotensi merepresentasikan logika pembentukan label. Arah dan dampak hubungan ini pada kinerja harus diuji, bukan diasumsikan. Notebook juga memuat sel ablation yang secara eksplisit menghapus proxy tersebut; hasil aktual sel itu belum diverifikasi pada audit ini.

Notebook melakukan deteksi grup pola fitur yang memiliki label bertentangan dan deduplikasi sebelum pembagian temporal. Tinjau pengaturan dan dampak karena pemilihan berdasarkan keseluruhan data dapat menggunakan informasi periode masa depan. Kesamaan 11 fitur tidak identik dengan peristiwa duplikat.

## Keputusan ilmiah dan pekerjaan lanjutan

1. Pertahankan dataset ini sebagai arsip data lama dan kandidat reproduksi atau pengembangan; jangan sebut sebagai data baru/independen.
2. Telusuri kode pembentuk dataset privat, log asal, pengertian label, periode dan nilai per jam untuk mengetahui apakah penghitung memakai kejadian sesudah waktu prediksi. Template publik tidak membuktikan cara dataset ini dibentuk.
3. Bandingkan checksum dan ringkasan dataset dengan manifest keluaran notebook lama; cari hasil ablation terdahulu sebelum menjalankan ulang.
4. Untuk Bab 7 perlukan rancangan evaluasi terpisah: definisi label/acuan, pembagian waktu dan unit resampling, ketersediaan metadata sumber serta organisasi, penerapan M1–M6 terbaru, dan hasil aktual. Label berbasis operasi log tidak otomatis menjadi ground truth serangan atau risiko organisasi.
5. Jangan masukkan `anomaly_reason` sebagai fitur untuk memprediksi label yang dibentuk dari informasi tersebut. Evaluasi proxy fitur dengan ablation dan pembanding sederhana pada subset uji yang sama; laporkan bahwa hasil tetap mengacu ke label yang tersedia.
6. Identitas dan metadata organisasi perlu perlindungan; berkas mengandung alamat IP serta pengenal hashed, sehingga bukan otomatis anonim atau aman untuk dipublikasikan.

## Reproduksi ringkas (Python)

Gunakan salinan dataset di lingkungan yang aman dan berikan path yang benar. Perhitungan berikut tidak mengekspor isi data:

```python
import hashlib
import pandas as pd
p = 'siuter_dataset.csv'
with open(p, 'rb') as f:
    print('SHA256:', hashlib.file_digest(f, 'sha256').hexdigest())
df = pd.read_csv(p, low_memory=False)
print('shape:', df.shape)
t = pd.to_datetime(df['timestamp'], errors='coerce')
print('periode:', t.min(), t.max(), 'timestamp invalid:', t.isna().sum())
print('label:', df['anomaly_label'].value_counts(dropna=False))
print('label vs is_error:', pd.crosstab(df['is_error'], df['anomaly_label']))
print('label vs log_level:', pd.crosstab(df['log_level'], df['anomaly_label']))
print('reason vs label:', pd.crosstab(df['anomaly_reason'].fillna('[missing]'), df['anomaly_label']))
print('duplikat 32 kolom setelah pertama:', df.duplicated().sum())
print('missing (%):', (df.isna().mean() * 100).round(1))
```
