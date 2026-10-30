
!pip install google-play-scraper pandas -q

import pandas as pd
import time
import re
from google_play_scraper import app, reviews, Sort

print("="*60)
print("SCRAPING ULASAN MOBILE JKN")
print("="*60)

# Konfigurasi
PACKAGE_NAME = 'app.bpjs.mobile'
TARGET_REVIEWS = 1500

print(f"\nPackage: {PACKAGE_NAME}")
print(f"Target: {TARGET_REVIEWS} ulasan\n")

def clean_text(text):
    if pd.isna(text) or text is None:
        return ''
    text = str(text)
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

print("Mengambil data ulasan...")
all_reviews = []
continuation_token = None

while len(all_reviews) < TARGET_REVIEWS:
    remaining = TARGET_REVIEWS - len(all_reviews)
    batch_size = min(500, remaining)
    
    print(f"  → Mengambil {len(all_reviews)+1}-{len(all_reviews)+batch_size}...")
    
    if continuation_token:
        batch, continuation_token = reviews(
            PACKAGE_NAME,
            continuation_token=continuation_token,
            lang='id',
            country='id',
            sort=Sort.NEWEST,
            count=batch_size
        )
    else:
        batch, continuation_token = reviews(
            PACKAGE_NAME,
            lang='id',
            country='id',
            sort=Sort.NEWEST,
            count=batch_size
        )
    
    if not batch:
        break
        
    all_reviews.extend(batch)
    time.sleep(1)

reviews_data = all_reviews[:TARGET_REVIEWS]
print(f"\n✓ Berhasil mengambil {len(reviews_data)} ulasan")

df = pd.DataFrame(reviews_data)
df_clean = pd.DataFrame({
    'review_id': df['reviewId'],
    'user_name': df['userName'],
    'rating': df['score'],
    'review_text': df['content'].apply(clean_text),
    'review_date': pd.to_datetime(df['at']),
    'thumbs_up_count': df['thumbsUpCount'],
    'app_version': df['reviewCreatedVersion'].fillna('Unknown')
})


output_file = 'reviews.csv'
df_clean.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✓ Data tersimpan: {output_file}")

from google.colab import files
files.download(output_file)

print("\n✓ Selesai! File sudah terdownload")
print(f"  Total data: {len(df_clean)} ulasan")
print(f"  Kolom: review_id, user_name, rating, review_text, review_date, thumbs_up_count, app_version")