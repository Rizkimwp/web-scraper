import pandas as pd
import time
from playwright.sync_api import sync_playwright

hashtag = "BubarkanDpr"
start_date = "2025-08-10"
end_date = "2025-08-25"
output_file = f"{hashtag}_{start_date}_to_{end_date}.csv"

url = f"https://x.com/search?q=%23{hashtag}%20since%3A{start_date}%20until%3A{end_date}&src=typed_query&f=live"

def scrape_tweets_live():
    tweets = []
    seen_ids = set()  # untuk mencegah duplikat
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="/home/rizkimwp/.config/google-chrome",
            executable_path="/opt/google/chrome/google-chrome",
            headless=False,
            args=["--profile-directory=Default"]
        )

        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("article[data-testid='tweet']", timeout=15000)

        same_count_times = 0
        prev_count = 0

        while True:
            articles = page.query_selector_all("article[data-testid='tweet']")
            new_tweets = 0

            for art in articles:
                tweet_id = art.get_attribute("data-tweet-id") or art.inner_text()[:20]  # fallback unik
                if tweet_id in seen_ids:
                    continue
                seen_ids.add(tweet_id)
                new_tweets += 1

                try:
                    text_el = art.query_selector("div[lang]")
                    text = text_el.inner_text() if text_el else ""

                    user_el = art.query_selector("div[dir='ltr'] > span")
                    user = user_el.inner_text() if user_el else ""

                    time_el = art.query_selector("time")
                    timestamp = time_el.get_attribute("datetime") if time_el else ""

                    photo_el = art.query_selector("img[src*='twimg']")
                    photo = photo_el.get_attribute("src") if photo_el else ""

                    tweets.append({
                        "user": user,
                        "time": timestamp,
                        "text": text,
                        "photo": photo
                    })
                except:
                    continue

            # Simpan CSV setiap scroll
            if new_tweets > 0:
                pd.DataFrame(tweets).to_csv(output_file, index=False, encoding="utf-8")

            print(f"Scroll: {len(tweets)} total tweets saved")

            # Stop condition
            if new_tweets == 0:
                same_count_times += 1
            else:
                same_count_times = 0

            if same_count_times >= 3:
                break

            page.mouse.wheel(0, 1000)
            time.sleep(2)

        context.close()
    return tweets

tweets = scrape_tweets_live()
print(f"Selesai! Tersimpan {len(tweets)} tweet di {output_file}")
