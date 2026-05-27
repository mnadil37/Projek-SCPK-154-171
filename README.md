# 📸 SPK Pemilihan Kamera Digital Metode AHP

Sistem Pendukung Keputusan (SPK) berbasis web untuk memberikan rekomendasi kamera digital terbaik khusus bagi kebutuhan *traveling* dan *vlogging*. Sistem ini dibangun menggunakan arsitektur metode hibrida **Analytic Hierarchy Process (AHP)** dan **Simple Additive Weighting (SAW)**.

## 👥 Anggota Kelompok Praktikum SCPK IF-I
* **Munadhil Mutawakkil** (123240154)
* **Mufid Dhamarjati Kusuma** (123240171)

## 📖 Latar Belakang
Pemilihan kamera digital yang ideal untuk mobilitas tinggi sering kali membingungkan konsumen karena adanya *trade-off* spesifikasi (misalnya: kamera beresolusi tinggi umumnya lebih berat dan mahal). Proyek ini bertujuan untuk mengatasi *paradox of choice* tersebut dengan menghitung secara matematis berbagai variabel (harga, berat, dimensi, resolusi, dll) berdasarkan preferensi prioritas masing-masing pengguna.

## 📊 Dataset & Pemodelan Sistem

Untuk menghasilkan rekomendasi yang akurat dan berbasis fakta, sistem ini menggunakan himpunan data (*dataset*) sekunder spesifikasi teknis kamera digital yang bersumber dari platform repositori data publik, **Kaggle**. Data mentah tersebut telah melalui tahap pra-pemrosesan (*data cleaning*) ke dalam file `camera_dataset_cleaned.csv` untuk membuang nilai kosong (*null*) dan memastikan integritas data komputasi.

### 1. Kriteria Objektif (Pool Kriteria)
Sistem menyediakan **12 kriteria teknis** yang diklasifikasikan ke dalam dua sifat keputusan (*Cost* dan *Benefit*). Pada saat penggunaan, pengguna diwajibkan memilih **tepat 5 kriteria** yang paling mewakili kebutuhan personal mereka untuk diproses ke dalam matriks pembobotan AHP:

| No | Atribut Kriteria | Sifat | Deskripsi |
| :---: | :--- | :---: | :--- |
| 1 | **Price** | Cost | Harga beli perangkat kamera (semakin murah semakin ramah anggaran). |
| 2 | **Weight** | Cost | Berat fisik total termasuk baterai (semakin ringan semakin *travel-friendly*). |
| 3 | **Dimensions** | Cost | Ukuran dimensi bodi kamera (semakin kecil semakin ringkas dibawa). |
| 4 | **Zoom wide (W)** | Cost | Jarak sudut pandang lensa terlebar (angka lebih kecil berarti bidang pandang lebih luas). |
| 5 | **Normal focus range** | Cost | Jarak minimum fokus standar (semakin kecil semakin cepat mengunci objek). |
| 6 | **Macro focus range** | Cost | Jarak minimum fokus khusus makro (semakin kecil semakin detail untuk objek mini). |
| 7 | **Effective pixels** | Benefit | Resolusi sensor utama dalam Megapixel (semakin tinggi semakin tajam gambar). |
| 8 | **Zoom tele (T)** | Benefit | Jangkauan zoom maksimal (semakin besar kemampuan potret jarak jauh tanpa pecah). |
| 9 | **Max resolution** | Benefit | Ukuran dimensi resolusi foto tertinggi yang dapat dihasilkan. |
| 10 | **Low resolution** | Benefit | Opsi resolusi foto terendah yang berguna untuk menghemat kapasitas memori. |
| 11 | **Storage included** | Benefit | Kapasitas memori internal bawaan dari pabrik. |
| 12 | **Release date** | Benefit | Tahun rilis kamera (semakin baru membawa teknologi prosesor yang lebih mutakhir). |

### 2. Alternatif Keputusan
Alternatif yang diolah di dalam sistem merupakan model-model kamera digital riil dari berbagai produsen yang terdaftar di dalam dataset. Agar proses komputasi perankingan SAW berjalan lebih terarah, sistem menyediakan fitur *filtering* dinamis di mana pengguna dapat membatasi data alternatif berdasarkan tahun rilis, batas harga maksimal, atau menggunakan filter cepat seperti *"Top 20 Kamera Termurah"* dan *"Top 20 Resolusi Tertinggi"*.

## ✨ Fitur Utama
* **Kriteria Dinamis:** Pengguna bebas memilih kombinasi 5 kriteria prioritas dari 12 pilihan yang tersedia.
* **Pembobotan AHP Terintegrasi:** Menggunakan Skala Saaty (1-9) untuk membandingkan kriteria secara berpasangan, dilengkapi dengan uji otomatis *Consistency Ratio* (CR ≤ 0.1).
* **Perankingan Cepat dengan SAW:** Mengeliminasi proses perbandingan alternatif yang panjang dengan mengeksekusi matriks normalisasi (*Cost/Benefit*) secara langsung pada data spesifikasi riil alternatif.
* **Transparansi Perhitungan:** Antarmuka menampilkan visualisasi proporsi bobot (Donut Chart) serta tabel detail hasil perkalian matriks normalisasi ($R$) dengan bobot prioritas ($W$) hingga memunculkan skor akhir.

## 🛠️ Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python
* **Framework Web:** Streamlit
* **Pengolahan Data:** Pandas, NumPy
* **Visualisasi Grafis:** Matplotlib & Seaborn
