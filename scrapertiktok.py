from playwright.sync_api import sync_playwright
import pandas as pd

hashtag = "bubarkandpr"
url = f"https://www.tiktok.com/tag/{hashtag}"
videos = []

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="/home/rizkimwp/.config/google-chrome",
        executable_path="/opt/google/chrome/google-chrome",
        headless=False,
        args=["--profile-directory=Default"]
    )
    page = context.new_page()
    page.goto(url, timeout=60000)

    # scroll untuk load lebih banyak video
    for _ in range(30):
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(2000)

    # ambil video item (khusus dari halaman hashtag)
    items = page.query_selector_all("div[id^='column-item-video-container-']")

    for item in items:
        try:
            # caption
            caption_el = item.query_selector("div[data-e2e='video-desc']")
            caption = caption_el.inner_text() if caption_el else ""

            # username
            user_el = item.query_selector("a[data-e2e='video-author-uniqueid']")
            username = user_el.inner_text() if user_el else ""

            # link video
            link_el = item.query_selector("a[href*='/video/']")
            link = link_el.get_attribute("href") if link_el else ""

            if link:
                videos.append({
                    "caption": caption,
                    "username": username,
                    "video_link": link
                })
        except Exception as e:
            print("skip:", e)

    context.close()

# simpan hasil
df = pd.DataFrame(videos)
df.to_csv(f"tiktok_{hashtag}.csv", index=False, encoding="utf-8")
print(f"Selesai! Tersimpan {len(videos)} video dari #{hashtag}")
