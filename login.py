from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://x.com/login")

    # 🔹 Login manual di sini
    input("Login dulu di browser, lalu tekan ENTER di terminal...")

    # simpan cookie & local storage
    context.storage_state(path="auth.json")
    browser.close()
