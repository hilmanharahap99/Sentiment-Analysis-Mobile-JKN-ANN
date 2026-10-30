
!pip install google-play-scraper pandas openpyxl -q

import pandas as pd
import numpy as np
import time
import re
from datetime import datetime
from google_play_scraper import app, reviews, Sort
import matplotlib.pyplot as plt
import seaborn as sns

print("="*80)
print(" SCRAPING ULASAN APLIKASI MOBILE JKN")
print("   Google Play Store")
print("="*80)

PACKAGE_NAME = 'app.bpjs.mobile'  
TARGET_REVIEWS = 1500  
LANGUAGE = 'id'  
COUNTRY = 'id' 

print(f"\n Konfigurasi Scraping:")
print(f"   • Nama Package: {PACKAGE_NAME}")
print(f"   • Target Data: {TARGET_REVIEWS} ulasan")
print(f"   • Bahasa: Indonesia")
print(f"   • Negara: Indonesia")

def clean_text(text):
    """
    Membersihkan teks ulasan dari karakter tidak perlu
    """
    if pd.isna(text) or text is None:
        return ''
    
    text = str(text)
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def get_sentiment_label(rating):
    """
    Mengkonversi rating menjadi label sentimen
    """
    if rating >= 4:
        return 'positive'
    elif rating <= 2:
        return 'negative'
    else:
        return 'neutral'


print("\n Memulai proses scraping.....")
print("-"*80)

try:
    # 1. Ambil informasi aplikasi terlebih dahulu
    print("\n Mengambil informasi aplikasi...")
    app_info = app(PACKAGE_NAME, lang=LANGUAGE, country=COUNTRY)
    
    print(f"\n Informasi Aplikasi:")
    print(f"   • Nama Aplikasi : {app_info['title']}")
    print(f"   • Developer    : {app_info['developer']}")
    print(f"   • Rating       : {app_info['score']} ")
    print(f"   • Total Ulasan : {app_info['ratings']:,} ulasan")
    print(f"   • Minimal Android: {app_info.get('androidVersion', 'N/A')}")
    
    # 2. Scraping ulasan
    print(f"\n Mengambil {TARGET_REVIEWS} ulasan terbaru...")
    print("   (Proses ini membutuhkan waktu 2-3 menit)")
    
    all_reviews = []
    continuation_token = None
    
    while len(all_reviews) < TARGET_REVIEWS:
        remaining = TARGET_REVIEWS - len(all_reviews)
        batch_size = min(500, remaining) 
        
        print(f"   → Mengambil ulasan ke-{len(all_reviews)+1} hingga {len(all_reviews)+batch_size}...")
        
        try:
            if continuation_token:
                batch, continuation_token = reviews(
                    PACKAGE_NAME,
                    continuation_token=continuation_token,
                    lang=LANGUAGE,
                    country=COUNTRY,
                    sort=Sort.NEWEST,
                    count=batch_size
                )
            else:
                batch, continuation_token = reviews(
                    PACKAGE_NAME,
                    lang=LANGUAGE,
                    country=COUNTRY,
                    sort=Sort.NEWEST,
                    count=batch_size
                )
            
            if not batch:
                print("   ⚠️ Tidak ada ulasan lagi yang bisa diambil")
                break
                
            all_reviews.extend(batch)
            print(f"   ✓ Terkumpul {len(all_reviews)}/{TARGET_REVIEWS} ulasan")
            
            # Delay untuk menghindari rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"   ⚠️ Error pada batch ini: {e}")
            print(f"   → Mengulang dalam 5 detik...")
            time.sleep(5)
            continue
    
 
    reviews_data = all_reviews[:TARGET_REVIEWS]
    print(f"\n  Berhasil mengumpulkan {len(reviews_data)} ulasan!")



    # MEMBUAT DATAFRAME
    print("\n Memproses dan membersihkan data...")
    
    df = pd.DataFrame(reviews_data)
    df_clean = pd.DataFrame({
        'review_id': df['reviewId'],
        'user_name': df['userName'],
        'rating': df['score'],
        'review_text': df['content'].apply(clean_text),
        'review_title': df['at'].apply(lambda x: str(x) if pd.notna(x) else ''),
        'review_date': pd.to_datetime(df['at']),
        'thumbs_up_count': df['thumbsUpCount'],
        'app_version': df['reviewCreatedVersion'].fillna('Unknown'),
        'review_length': df['content'].apply(lambda x: len(str(x)) if pd.notna(x) else 0),
        'word_count': df['content'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)
    })
    
    # label sentimen
    df_clean['sentiment_label'] = df_clean['rating'].apply(get_sentiment_label)
    
    # Tambahkan kolom untuk one-hot encoding (opsional untuk ANN)
    df_clean['sentiment_positive'] = (df_clean['sentiment_label'] == 'positive').astype(int)
    df_clean['sentiment_neutral'] = (df_clean['sentiment_label'] == 'neutral').astype(int)
    df_clean['sentiment_negative'] = (df_clean['sentiment_label'] == 'negative').astype(int)
    
    print("✓ Data berhasil diproses!")
    
    # STATISTIK DATA
    print("\n" + "="*80)
    print("STATISTIK DATA HASIL SCRAPING")
    print("="*80)
    
    # Statistik Rating
    print("\n DISTRIBUSI RATING:")
    rating_dist = df_clean['rating'].value_counts().sort_index()
    for rating, count in rating_dist.items():
        percentage = (count/len(df_clean))*100
        bar = "█" * int(percentage)
        print(f"   {rating} ★ : {count:4d} ulasan ({percentage:5.1f}%) {bar}")
    
    # Statistik Sentimen
    print("\n DISTRIBUSI SENTIMEN:")
    sentiment_dist = df_clean['sentiment_label'].value_counts()
    sentiment_colors = {'positive': '😊', 'neutral': '😐', 'negative': '😠'}
    for sentiment in ['positive', 'neutral', 'negative']:
        if sentiment in sentiment_dist:
            count = sentiment_dist[sentiment]
            percentage = (count/len(df_clean))*100
            bar = "█" * int(percentage)
            print(f"   {sentiment_colors[sentiment]} {sentiment.upper():8}: {count:4d} ulasan ({percentage:5.1f}%) {bar}")
    
    # Statistik Teks
    print("\n STATISTIK TEKS:")
    print(f"   • Rata-rata panjang ulasan : {df_clean['review_length'].mean():.0f} karakter")
    print(f"   • Rata-rata jumlah kata    : {df_clean['word_count'].mean():.1f} kata")
    print(f"   • Ulasan dengan teks       : {(df_clean['review_text'] != '').sum()} ulasan")
    print(f"   • Ulasan kosong            : {(df_clean['review_text'] == '').sum()} ulasan")
    print(f"   • Ulasan terpendek         : {df_clean['review_length'].min()} karakter")
    print(f"   • Ulasan terpanjang        : {df_clean['review_length'].max()} karakter")
    
    # Statistik Engagement
    print("\n STATISTIK ENGAGEMENT:")
    print(f"   • Total thumbs up          : {df_clean['thumbs_up_count'].sum():,}")
    print(f"   • Rata-rata thumbs up      : {df_clean['thumbs_up_count'].mean():.1f}")
    print(f"   • Maksimal thumbs up       : {df_clean['thumbs_up_count'].max()}")
    
    # Rentang tanggal
    print("\n RENTANG TANGGAL:")
    print(f"   • Ulasan tertua  : {df_clean['review_date'].min().strftime('%d %B %Y')}")
    print(f"   • Ulasan terbaru : {df_clean['review_date'].max().strftime('%d %B %Y')}")
    
    
    # VISUALISASI SEDERHANA
    
    print("\n" + "="*80)
    print("VISUALISASI DATA")
    print("="*80)
    
    # Setup style
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Distribusi Rating
    rating_counts = df_clean['rating'].value_counts().sort_index()
    colors_rating = ['#ff4444', '#ffaa44', '#ffff44', '#88ff88', '#44ff44']
    axes[0, 0].bar(rating_counts.index, rating_counts.values, color=colors_rating, edgecolor='black')
    axes[0, 0].set_title('Distribusi Rating Pengguna', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Rating (Bintang)', fontsize=12)
    axes[0, 0].set_ylabel('Jumlah Ulasan', fontsize=12)
    for i, (rating, count) in enumerate(rating_counts.items()):
        axes[0, 0].text(rating, count + 5, str(count), ha='center', fontsize=10, fontweight='bold')
    
    # 2. Distribusi Sentimen
    sentiment_counts = df_clean['sentiment_label'].value_counts()
    colors_sentiment = ['#44ff44', '#ffaa44', '#ff4444']
    axes[0, 1].bar(sentiment_counts.index, sentiment_counts.values, color=colors_sentiment, edgecolor='black')
    axes[0, 1].set_title('Distribusi Label Sentimen', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Sentimen', fontsize=12)
    axes[0, 1].set_ylabel('Jumlah Ulasan', fontsize=12)
    for i, (sentiment, count) in enumerate(sentiment_counts.items()):
        axes[0, 1].text(i, count + 5, str(count), ha='center', fontsize=10, fontweight='bold')
    
    # 3. Pie Chart Sentimen
    axes[1, 0].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
                   colors=colors_sentiment, startangle=90, explode=(0.05, 0.05, 0.05))
    axes[1, 0].set_title('Proporsi Sentimen', fontsize=14, fontweight='bold')
    
    # 4. Boxplot Rating vs Sentimen
    rating_by_sentiment = [df_clean[df_clean['sentiment_label'] == 'positive']['rating'],
                           df_clean[df_clean['sentiment_label'] == 'neutral']['rating'],
                           df_clean[df_clean['sentiment_label'] == 'negative']['rating']]
    bp = axes[1, 1].boxplot(rating_by_sentiment, labels=['Positive', 'Neutral', 'Negative'], 
                             patch_artist=True, showmeans=True)
    colors_box = ['#44ff44', '#ffaa44', '#ff4444']
    for patch, color in zip(bp['boxes'], colors_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    axes[1, 1].set_title('Distribusi Rating per Sentimen', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Rating', fontsize=12)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('mobile_jkn_visualisasi.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n✓ Visualisasi tersimpan sebagai 'mobile_jkn_visualisasi.png'")
    
    
    # SAMPLE ULASAN
    print("\n" + "="*80)
    print("SAMPLE ULASAN (10 Data Terbaru)")
    print("="*80)
    
    for idx, row in df_clean.head(10).iterrows():
        print(f"\n{'─'*80}")
        print(f" Rating: {row['rating']} ★ |  {row['thumbs_up_count']} likes |  {row['review_date'].strftime('%d/%m/%Y')}")
        print(f" Pengguna: {row['user_name'][:30]}")
        print(f" Sentimen: {row['sentiment_label'].upper()}")
        print(f" Ulasan: {row['review_text'][:200]}{'...' if len(row['review_text']) > 200 else ''}")
    
    
    # CONTOH ULASAN PER SENTIMEN
    
    print("\n" + "="*80)
    print("CONTOH ULASAN PER KATEGORI SENTIMEN")
    print("="*80)
    for sentiment in ['positive', 'neutral', 'negative']:
        sentiment_data = df_clean[df_clean['sentiment_label'] == sentiment]
        if len(sentiment_data) > 0:
            print(f"\n SENTIMEN {sentiment.upper()}:")
            sample_review = sentiment_data.iloc[0]
            print(f"   Rating: {sample_review['rating']} ★ | Ulasan: {sample_review['review_text'][:150]}...")
    
    # SIMPAN DATA
    
    print("\n" + "="*80)
    print(" MENYIMPAN DATA")
    print("="*80)
    
    # Simpan dalam berbagai format
    csv_file = 'mobile_jkn_reviews.csv'
    excel_file = 'mobile_jkn_reviews.xlsx'
    json_file = 'mobile_jkn_reviews.json'
    df_clean.to_csv(csv_file, index=False, encoding='utf-8-sig')
    df_clean.to_excel(excel_file, index=False, engine='openpyxl')
    df_clean.to_json(json_file, orient='records', force_ascii=False, indent=2)
    print(f"\n Data berhasil disimpan dalam 3 format:")
    print(f"   CSV   : {csv_file}")
    print(f"   Excel : {excel_file}")
    print(f"   JSON  : {json_file}")
    
    
    # DOWNLOAD FILE (Untuk Colab)
    
    from google.colab import files
    
    print("\n" + "="*80)
    print("DOWNLOAD FILE")
    print("="*80)
    
    print("\nMengunduh file ke komputer lokal...")
    
    files.download(csv_file)
    files.download(excel_file)
    
    
    # RINGKASAN FINAL
    
    print("\n" + "="*80)
    print("SCRAPING SELESAI!")
    print("="*80)
    
    print(f"""
    📊 RINGKASAN DATA:
    ─────────────────────────────────────────────────
    • Total ulasan yang diambil    : {len(df_clean)} data
    • Rentang tanggal              : {df_clean['review_date'].min().strftime('%d/%m/%Y')} - {df_clean['review_date'].max().strftime('%d/%m/%Y')}
    • Rata-rata rating             : {df_clean['rating'].mean():.2f} ★
    • Total thumbs up              : {df_clean['thumbs_up_count'].sum():,}
    
    📈 DISTRIBUSI SENTIMEN:
    • Positive  : {(df_clean['sentiment_label'] == 'positive').sum()} ulasan ({(df_clean['sentiment_label'] == 'positive').sum()/len(df_clean)*100:.1f}%)
    • Neutral   : {(df_clean['sentiment_label'] == 'neutral').sum()} ulasan ({(df_clean['sentiment_label'] == 'neutral').sum()/len(df_clean)*100:.1f}%)
    • Negative  : {(df_clean['sentiment_label'] == 'negative').sum()} ulasan ({(df_clean['sentiment_label'] == 'negative').sum()/len(df_clean)*100:.1f}%)
    
    🎯 DATA SIAP DIGUNAKAN UNTUK:
    • Preprocessing teks (case folding, tokenizing, stopword removal, stemming)
    • Feature extraction (TF-IDF / Word2Vec)
    • Implementasi Artificial Neural Network (ANN)
    • Evaluasi model (akurasi, precision, recall, F1-score)
    
    📁 FILE TERSEDIA:
    • mobile_jkn_reviews.csv  - File utama untuk analisis
    • mobile_jkn_reviews.xlsx - Backup dalam format Excel
    • mobile_jkn_visualisasi.png   - Visualisasi distribusi data
    """)
    
except Exception as e:
    print(f"\n TERJADI ERROR: {e}")
    print("\n SOLUSI:")
    print("   1. Refresh halaman Colab (Runtime → Factory reset runtime)")
    print("   2. Jalankan ulang script")
    print("   3. Pastikan koneksi internet stabil")
    print("   4. Jika error 403, tunggu 5-10 menit lalu coba lagi")
    print("   5. Gunakan VPN jika diperlukan")

print("\nSelesai!!!..")