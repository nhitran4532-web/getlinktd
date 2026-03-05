import requests
import re
import json

def get_data():
    # Nguồn tổng hợp link Gà Vàng/IPTV uy tín hơn
    url = "https://raw.githubusercontent.com/hongduy02/gavang/main/gavang.m3u"
    headers = {'User-Agent': 'Mozilla/5.0'}
    channels = []
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            content = response.text
            # Quét lấy tên trận và link m3u8
            matches = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*?\.m3u8)', content)
            
            for name, link in matches:
                channels.append({
                    "title": name.strip(), # MonPlayer cần chữ "title"
                    "url": link.strip()
                })
    except Exception as e:
        print(f"Lỗi: {e}")
    return channels

data = get_data()

# Xuất file JSON chuẩn cấu trúc MonPlayer
with open("MT.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Đã tìm thấy {len(data)} trận đấu!")
