# Web Scraping Tools

Repository ini berisi skrip Python untuk mengambil data video dari halaman hashtag TikTok / Twitter menggunakan **Playwright**. Data yang diambil meliputi caption, username, dan link video, kemudian disimpan dalam format CSV.

---

## Fitur

* Scraping video dari hashtag TikTok tertentu.
* Menyimpan hasil scraping ke CSV.
* Scroll otomatis untuk memuat lebih banyak video.
* Mendukung Chrome profile untuk login otomatis jika dibutuhkan.

---

## Prasyarat

* Python 3.8+
* Google Chrome terinstall.
* Library Python:

```bash
pip install pandas playwright
```

* Install browser Playwright:

```bash
playwright install
```

---

## Cara Penggunaan

1. **Clone repositori**:

```bash
git clone https://github.com/Rizkimwp/web-scraper.git
cd tiktok-scraper
```

2. **Sesuaikan hashtag dan path Chrome** di `scraper**.py`:

```python
hashtag = "bubarkandpr"

context = p.chromium.launch_persistent_context(
    user_data_dir="/home/rizkimwp/.config/google-chrome",  # path profil Chrome
    executable_path="/opt/google/chrome/google-chrome",    # path executable Chrome
    headless=False,
    args=["--profile-directory=Default"]
)
```

3. **Jalankan skrip**:

```bash
python scrapertiktok.py
python scrapertweet.py
```

4. **Hasil scraping** akan tersimpan di file CSV:

```
tiktok_bubarkandpr.csv
```

---

## Struktur CSV

| caption      | username        | video\_link |
| ------------ | --------------- | ----------- |
| teks caption | username TikTok | link video  |

---

## Catatan

* Gunakan scraping dengan etika: patuhi **robots.txt** dan jangan overload server TikTok.
* Bisa dikembangkan untuk:

  * Menambah jumlah scroll atau video yang diambil.
  * Menyimpan info tambahan seperti likes, komentar, dan views.
* Pastikan akun TikTok-mu bisa diakses lewat Chrome profile jika halaman memerlukan login.
