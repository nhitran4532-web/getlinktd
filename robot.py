import requests
import re
import json

# Đây là nơi 'robot' sẽ đến để lấy link. 
# Bạn có thể thay đổi link này sau nếu trang web đổi địa chỉ.
TARGET_URL = "https://xem1.gv05.live/" 

def hunt_m3u8():
    # Giả lập trình duyệt để không bị trang web chặn
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": TARGET_URL
    }
    try:
        print("Đang đi săn link m3u8...")
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        # Lệnh tìm link có đuôi .m3u8
        links = re.findall(r'(https?://[^\s"\'<>]*\.m3u8[^\s"\'<>]*)', response.text)
        return links[0] if links else None
    except Exception as e:
        print(f"Lỗi rồi: {e}")
        return None

# Lấy link tìm được
link_found = hunt_m3u8()

# Đóng gói vào file JSON đúng cấu trúc bạn cần
if link_found:
    data = {
        "name": "DANH SÁCH CỦA TÔI",
        "groups": [{
            "name": "🔴 TRỰC TIẾP BÓNG ĐÁ",
            "channels": [{
                "name": "Trận đấu trực tiếp",
                "sources": [{
                    "url": link_found,
                    "request_headers": [{"key": "Referer", "value": TARGET_URL}]
                }]
            }]
        }]
    }
    
    # Lưu kết quả thành file MT.json
    with open('MT.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Thành công! Đã tạo file MT.json")
else:
    print("Thất bại: Không tìm thấy link nào.")