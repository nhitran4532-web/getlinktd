import asyncio
import json
from playwright.async_api import async_playwright

async def intercept_m3u8():
    async with async_playwright() as p:
        # Dùng trình duyệt thật để tránh bị check bot
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        found_links = []

        # HÀM CHẶN DÒNG DỮ LIỆU
        async def handle_request(request):
            url = request.url
            # Lọc lấy link m3u8, bỏ qua mấy cái link quảng cáo hay rác
            if ".m3u8" in url and "google" not in url and "doubleclick" not in url:
                if url not in [item['url'] for item in found_links]:
                    found_links.append({
                        "name": f"Trận {len(found_links) + 1}",
                        "url": url,
                        "headers": {
                            "Referer": "https://gavang...tv/", # Thay bằng domain thật của nó
                            "User-Agent": "Mozilla/5.0..."
                        }
                    })
                    print(f"Đã hốt được: {url}")

        # Bắt đầu nghe lén Network
        page.on("request", handle_request)

        try:
            # 1. Đi thẳng vào trang chủ
            print("Đang đột nhập Gà Vàng...")
            await page.goto("https://gavang...tv/", wait_until="networkidle", timeout=60000)
            
            # 2. Cuộn trang để nó load hết các trận
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(10) # Đợi 10s cho các request ngầm chạy hết

            # 3. Lưu thành file JSON cho MoPlayer
            output = {
                "name": "Gavang Auto Live",
                "urls": found_links
            }
            
            with open("playlist.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            
            print(f"Xong! Hốt được tổng cộng {len(found_links)} link.")

        except Exception as e:
            print(f"Lỗi: {e}")
        finally:
            await browser.close()

asyncio.run(intercept_m3u8())
