import requests
import json

def get_data_from_source():
    # Đây là link "gốc" tổng hợp từ server chứa link Gà Vàng
    source_url = "https://raw.githubusercontent.com/hongduy02/gavang/main/gavang.m3u"
    headers = {'User-Agent': 'Mozilla/5.0'}
    channels = []

    try:
        response = requests.get(source_url, headers=headers, timeout=15)
        if response.status_code == 200:
            lines = response.text.split('\n')
            current_title = None
            
            for line in lines:
                line = line.strip()
                # Lấy tên trận đấu từ dòng #EXTINF
                if line.startswith('#EXTINF:'):
                    current_title = line.split(',')[-1].strip()
                # Lấy link m3u8 ngay dòng dưới
                elif line.startswith('http') and 'm3u8' in line:
                    if current_title:
                        channels.append({
                            "title": f"⚽ {current_title}", # Đúng chuẩn MonPlayer
                            "url": line
                        })
                        current_title = None
    except Exception as e:
        print(f"Lỗi truy cập nguồn: {e}")
    return channels

# Robot xử lý và tạo file JSON
data = get_live_data_from_source()
with open("MT.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Đã cập nhật {len(data)} trận đấu từ nguồn gốc!")
