# Data card — dataset chạy thử của TV2

## Dataset · Đơn và chính sách D1 giả lập

| Thuộc tính | Nội dung |
|---|---|
| File | `data/d1_orders.json` |
| Mục đích | Nguồn chỉ đọc cho công cụ và quyết định AI; không làm bằng chứng pain |
| Nguồn | Dữ liệu viết tay với hỗ trợ AI, giữ nguyên từ baseline CP2 |
| Quy mô | 2 đơn (D100/D101), 4 món, 1 chính sách |
| Sinh/xử lý | Không ngẫu nhiên nên seed không áp dụng; không chia train/test |
| Nhãn | `synthetic` |
| Đơn vị | Giá và hạn mức là số nguyên VND |
| Quyền riêng tư | Không đơn thật, tên khách, địa chỉ hoặc số điện thoại |
| Phiên bản | Dataset CP2, kiểm schema trong bản prototype CP3 ngày 28/11/2026 |

Schema được runtime kiểm trước khi công cụ trả dữ liệu:

- Root chỉ gồm `orders` và `policy`.
- Mỗi đơn chỉ có `id`, `items`; ID dạng D + 3 chữ số, không trùng.
- Mỗi món chỉ có `name`, `price`; tên không rỗng/trùng trong đơn, giá nguyên ≥0,
  không chấp nhận bool, chuỗi hoặc số thực thay tiền.
- Policy gồm `max_vnd` nguyên ≥0 và `description` dạng chuỗi.
- Trường ngoài schema, gồm trường thông tin cá nhân, khiến công cụ báo lỗi.
- `get_order`/`get_policy` chỉ đọc, không ghi hoặc gọi hệ thống ngoài.

Code kiểm tên món/giá/hạn mức lần nữa trước khi hiển thị đề xuất. Unit test đã
kiểm schema, dữ liệu sai kiểu, trùng ID và trường ngoài schema. Không nhận là đã
có người thứ hai kiểm tay dataset.

Giới hạn: chỉ 2 đơn nhỏ, chưa mô tả số lượng món, ảnh chứng cứ, lịch sử bồi thường,
trạng thái xử lý hoặc chủ đơn thật. Không suy phân bố thực tế hay hiệu quả ngoài
sản phẩm từ dataset này. TV2 không thay benchmark, evidence, metric hoặc chuẩn CP2.
