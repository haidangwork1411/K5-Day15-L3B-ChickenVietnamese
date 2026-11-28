# Tóm tắt mô phỏng simulate-1@20261128-122133

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| khieu_nai_it | 19 | 1 | 91 | 24 | 0.2 | 0.5 |
| khieu_nai_vua | 23 | 2 | 450 | 118 | 0.8 | 1.6 |
| khieu_nai_nhieu | 8 | 3 | 791 | 190 | 1.4 | 2.9 |

Tỉ lệ đạt dùng để tính: 20/20 (100%) — lượt run-2@20261128-120942

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (5 người) | Chi phí / tháng — cơ sở (20 người) | Chi phí / tháng — cao (40 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00023 | $0.00023 | $0.00013 | $0.0027 | $0.0109 | $0.0218 | $0.00055 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0013 | $0.0013 | $0.00071 | $0.0147 | $0.0589 | $0.1179 | $0.0029 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.8) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: baidu/ernie-5.5-flash-preview:free. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
