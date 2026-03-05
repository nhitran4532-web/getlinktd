import requests
import json

def get_live_links():
    # Sử dụng API nguồn tổng hợp đã giải mã sẵn cho IPTV
    # Đây là nguồn cực mạnh, chuyên cào link Gà Vàng, Socolive...
    url = "https://raw.githubusercontent.com/hongduy02/gavang/main/gavang.m3u"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    channels = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        lines = response.text.split('\n')
        
        current_name = None
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                # Tách lấy tên trận đấu sau dấu phẩy
                current_name = line.split(',')[-1]
            elif line.startswith('http') and ('.m3u8' in line or 'm3u8' in line):
                if current_name:
                    channels.append({
                        "title": f"⚽ {current_name}", # MonPlayer cần "title"
                        "url": line
                    })
                    current_name = None
    except Exception as e:
        print(f"Lỗi cào dữ liệu: {e}")
    
    return channels

# Thực thi
data = get_live_links()

# Xuất file JSON chuẩn cho MonPlayer
with open("MT.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Thành công! Robot đã tóm được {len(data)} trận đấu đang live.")
