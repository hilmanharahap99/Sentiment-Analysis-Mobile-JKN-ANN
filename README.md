# Analisis Sentimen Mobile JKN Menggunakan Artificial Neural Network (ANN)

## Deskripsi Proyek

Proyek ini merupakan implementasi penelitian analisis sentimen terhadap ulasan pengguna aplikasi **Mobile JKN** yang diperoleh dari Google Play Store. Penelitian ini bertujuan untuk mengklasifikasikan opini pengguna ke dalam tiga kategori sentimen, yaitu positif, negatif, dan netral menggunakan metode **Artificial Neural Network (ANN)**.

Penelitian ini berfokus pada perbandingan dua teknik penanganan ketidakseimbangan data (*class imbalance*), yaitu **Random Oversampling (ROS)** dan **Class Weight**, untuk mengetahui pengaruh keduanya terhadap performa klasifikasi model ANN.

## Tujuan Penelitian

- Menganalisis sentimen pengguna terhadap aplikasi Mobile JKN.
- Mengklasifikasikan ulasan ke dalam kategori positif, negatif, dan netral.
- Membangun model klasifikasi menggunakan Artificial Neural Network (ANN).
- Membandingkan performa Random Oversampling (ROS) dan Class Weight.
- Mengevaluasi hasil klasifikasi berdasarkan metrik pengujian model.

## Metodologi Penelitian

Tahapan penelitian yang dilakukan meliputi:

1. **Pengumpulan Data** – Mengambil data ulasan pengguna aplikasi Mobile JKN dari Google Play Store.
2. **Preprocessing Data** – Melakukan pembersihan teks melalui case folding, cleaning, tokenization, normalisasi, stopword removal, dan stemming.
3. **Exploratory Data Analysis (EDA)** – Menganalisis distribusi sentimen dan karakteristik data ulasan.
4. **Feature Extraction** – Mengubah teks menjadi representasi numerik menggunakan TF-IDF.
5. **Data Splitting** – Membagi dataset menjadi data pelatihan dan pengujian dengan rasio 80:20.
6. **Model Development** – Membangun model klasifikasi menggunakan Artificial Neural Network (ANN).
7. **Penanganan Imbalanced Data** – Menerapkan Random Oversampling (ROS) dan Class Weight sebagai dua pendekatan eksperimen yang berbeda.
8. **Evaluasi Model** – Mengukur performa model menggunakan Accuracy, Precision, Recall, F1-Score, dan Confusion Matrix.

## Perbandingan Hasil Akurasi Model

Berikut merupakan hasil pengujian model ANN menggunakan dua teknik penanganan ketidakseimbangan data.

| Metode | Akurasi |
|---|---:|
| ANN + Random Oversampling (ROS) | **94,62%** |
| ANN + Class Weight | **80,45%** |

### Visualisasi Perbandingan Akurasi

- Random Oversampling (ROS): 94,62%
- Class Weight: 80,45%

Berdasarkan hasil pengujian, model ANN dengan teknik Random Oversampling memperoleh akurasi sebesar **94,62%**, sedangkan model ANN dengan teknik Class Weight memperoleh akurasi sebesar **80,45%**.

Terdapat selisih akurasi sebesar 14,17 poin persentase antara kedua pendekatan. Hasil tersebut menunjukkan bahwa Random Oversampling memberikan performa akurasi yang lebih tinggi dibandingkan Class Weight pada eksperimen penelitian ini.

## Tools dan Teknologi

Beberapa tools dan library yang digunakan dalam penelitian ini:

- **Python** – Bahasa pemrograman utama.
- **Google Colab / Jupyter Notebook** – Lingkungan pengembangan dan eksperimen.
- **Pandas** – Pengolahan dan manipulasi dataset.
- **NumPy** – Komputasi numerik.
- **Scikit-learn** – Preprocessing, TF-IDF, pembagian data, dan evaluasi model.
- **TensorFlow / Keras** – Pembangunan dan pelatihan model ANN.
- **NLTK / Sastrawi** – Pemrosesan teks bahasa Indonesia.
- **Matplotlib / Seaborn** – Visualisasi data dan hasil evaluasi.
- **WordCloud** – Visualisasi kata yang sering muncul dalam ulasan.

## Metrik Evaluasi

Evaluasi performa model dilakukan menggunakan beberapa metrik berikut:

- **Accuracy:** Mengukur persentase prediksi yang benar dari keseluruhan data pengujian.
- **Precision:** Mengukur ketepatan hasil prediksi pada setiap kelas sentimen.
- **Recall:** Mengukur kemampuan model dalam menemukan data yang benar pada setiap kelas.
- **F1-Score:** Mengukur keseimbangan antara Precision dan Recall.
- **Confusion Matrix:** Menampilkan perbandingan antara hasil prediksi dan label aktual.

## Kesimpulan

Berdasarkan hasil eksperimen, model Artificial Neural Network (ANN) dengan teknik Random Oversampling memperoleh akurasi sebesar **94,62%**, sedangkan model dengan teknik Class Weight memperoleh akurasi sebesar **80,45%**.

Dengan demikian, Random Oversampling menunjukkan hasil akurasi yang lebih tinggi dibandingkan Class Weight dalam penelitian analisis sentimen ulasan aplikasi Mobile JKN.

Penelitian ini merupakan bagian dari studi akademik di bidang Machine Learning dan Natural Language Processing (NLP), khususnya dalam penerapan Artificial Neural Network untuk analisis sentimen.
