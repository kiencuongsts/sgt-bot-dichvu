# SGT Service Lab

Microsite thử nghiệm công cụ **Tư vấn chọn dịch vụ tự động** của Saigontourist. Dữ liệu lấy từ SGT Channel API (production: `https://platform.saigontourist.net/channel/v1`).

## Tính năng

- **Tư vấn (hội thoại):** hệ thống hỏi–đáp để thu thập nhu cầu: điểm đến, loại dịch vụ, số khách, tuổi trẻ em, ngày sử dụng, quốc tịch, số ngày, ngân sách, sở thích. Chỉ hỏi những câu có ảnh hưởng tới kết quả, dựa trên dữ liệu thật. Sau đó chấm điểm, kiểm tra ngày đặt được và tính giá theo `ticket_types[].prices[]`. Có tuỳ chọn dùng Claude để hiểu câu tự do khi mở trên claude.ai (capability `sample`); không có thì dùng bộ luật tiếng Việt.
- **Danh mục:** lọc và xem chi tiết 140 dịch vụ, kèm bảng giá và cách bộ tư vấn hiểu từng dòng giá.
- **Dữ liệu & kiểm thử:** thống kê, kiểm tra chất lượng dữ liệu, ma trận kịch bản kiểm thử.

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `index.html` | Microsite đã build, một file duy nhất, mở trực tiếp bằng trình duyệt |
| `services_kb.json` | Dữ liệu dịch vụ dạng văn bản thuần, dùng để nạp vào công cụ AI |
| `src/template.html` | Mã nguồn giao diện và bộ tư vấn (HTML/CSS/JS) |
| `tools/fetch.py` | Tải `/services/filters`, `/services` và `/services/{id}` từ API |
| `tools/thumbs.py` | Tải và nén ảnh đại diện thành data URI |
| `tools/build.py` | Ghép template, dữ liệu và ảnh thành `index.html` và `services_kb.json` |
| `data/` | Dữ liệu thô đã tải (`services.json`) và ảnh thu nhỏ (`thumbs.json`) |

## Cập nhật dữ liệu

Tạo file `.env` ở thư mục gốc (đã nằm trong `.gitignore`, **không commit**):

```
SGT_API_BASE=https://platform.saigontourist.net/channel/v1
SGT_CLIENT_ID=...
SGT_CLIENT_SECRET=...
SGT_WEBHOOK_SECRET=...
```

Rồi chạy:

```bash
python3 tools/fetch.py
python3 tools/thumbs.py
python3 tools/build.py
```

Có thể đặt các biến trên bằng `export` thay cho file `.env`. Đổi `SGT_API_BASE` sang `https://sandbox.saigontourist.me/channel/v1` để dùng sandbox.

Cần Python 3 và Pillow (`pip install pillow`) cho bước tạo ảnh thu nhỏ.
