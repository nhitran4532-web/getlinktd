import requests
import json
import re

def get_all_m3u8():
    # Đây là "nguồn tổng" đã được giải mã sẵn link m3u8 của các trang bóng đá
    source_url = "https://raw.githubusercontent.com/hongduy02/gavang/main/gavang.m3u"
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []

    try:
        response = requests.get(source_url, headers=headers, timeout=15)
        if response.status_code == 200:
            # Dùng Regex để quét sạch các cặp Tên trận và Link m3u8
            pattern = r'#EXTINF:.*?,(.*?)\n(http.*?\.m3u8)'
            matches = re.findall(pattern, response.text)
            
            for name, url in matches:
                results.append({
                    "title": name.strip(), # MonPlayer cần title
                    "url": url.strip()
                })
    except Exception as e:
        print(f"Lỗi: {e}")
    return results

# Chạy Robot
data = get_all_m3u8()

# Xuất file MT.json
with open("MT.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Đã hốt được {len(data)} trận đấu m3u8!")
