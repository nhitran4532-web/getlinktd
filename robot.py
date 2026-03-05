import requests
import re
import json

def get_data():
    # Nguồn này thường chứa danh sách m3u8 trực tiếp của Gà Vàng
    url = "https://raw.githubusercontent.com/hongduy02/gavang/main/gavang.m3u"
    headers = {'User-Agent': 'Mozilla/5.0'}
    channels = []
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        content = response.text
        # Tìm tên trận và link m3u8
        matches = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*?\.m3u8)', content)
        
        for name, link in matches:
            channels.append({
                "title": name.strip(), # MonPlayer cần "title" thay vì "name"
                "url": link.strip()
            })
    except:
        pass
    return channels

data = get_data()

# Xuất file JSON đúng cấu trúc MonPlayer (Dạng danh sách đối tượng)
with open("MT.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Tạo thêm file M3U cho chắc chắn
with open("MT.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for item in data:
        f.write(f'#EXTINF:-1, {item["title"]}\n{item["url"]}\n')
