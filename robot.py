import requests
import re
import json

def get_gavang_links():
    # Đây là nơi Robot sẽ đến để "nhặt" link
    source_url = "https://bit.ly/gavang-live" # Hoặc nguồn trực tiếp bạn có
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    channels = []
    try:
        response = requests.get(source_url, headers=headers, timeout=10)
        # Robot tìm các dòng có định dạng tên trận và link m3u8
        # Lưu ý: Đây là logic giả định, bạn có thể thay bằng link .txt hoặc .m3u gốc
        content = response.text
        
        # Tìm tất cả các link m3u8 và tên trận đấu
        matches = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*?\.m3u8)', content)
        
        for name, url in matches:
            channels.append({
                "name": f"⭐ {name.strip()}",
                "url": url.strip()
            })
    except Exception as e:
        print(f"Lỗi rồi đại ca ơi: {e}")
    
    return channels

# Chạy lệnh lấy tin
data = get_gavang_links()

# 1. Xuất file JSON cho MonPlayer
with open("MT.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 2. Xuất file M3U cho các app TV khác (phòng hờ)
with open("MT.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for item in data:
        f.write(f'#EXTINF:-1, {item["name"]}\n{item["url"]}\n')

print("Đã cập nhật xong trận đấu mới nhất!")
