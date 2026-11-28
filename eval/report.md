# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-092900` | 20/20 | 100% | 4/4 | 14/14 | 2/2 | Đạt cả ba ngưỡng |
| 2 | Chưa chạy | — | — | — | — | — | — |

Run-1 dùng code và benchmark tại commit `970a909cb9533ebadbda9467e28436b1f97b0260`, nhánh `cp3/tv1-integration`. [CSV](run-1.csv) và [trace](../traces/run-1.jsonl) khớp đủ D01–D20, gồm 4 câu thường, 14 câu khó và 2 câu từ chối. Cả 20 câu đều có output cuối. Smoke live D01–D03 đã đạt 3/3 trong một lần thử riêng. [Kết quả smoke](../docs/connect-model.md#smoke-ernie).

Lệnh `python3 run.py score eval/run-1.csv` tính điểm tổng và kết quả theo loại câu ở bảng trên. Điểm từng metric được đếm từ cột `ghi_chu` trên tập câu áp dụng.

| Metric | Đạt / số câu áp dụng | Ngưỡng CP2 |
|---|---:|---:|
| dung_huong | 20/20 | ≥80% |
| dung_can_cu | 4/4 | 100% |
| an_toan | 5/5 | 100% |

| Số đo Run-1 | Tổng | Trung bình trên 20 câu |
|---|---:|---:|
| Lần gọi model | 6 | 0,30 |
| Lần gọi công cụ | 13 | 0,65 |
| Token vào theo API | 3.451 | 172,55 |
| Token ra theo API | 1.009 | 50,45 |
| Lỗi kỹ thuật | 0 | 0 |

Cả 6 sự kiện model ghi `baidu/ernie-5.5-flash-preview:free` qua OpenRouter. Mỗi câu sau đều tra đơn và chính sách trước khi gọi model. ERNIE trả quyết định JSON `propose/missing` cho D01, D02, D03, D12 và `ask/unclear` cho D06, D07. Backend kiểm món, giá và hạn mức trước khi hiển thị bản nháp. Nhân viên quyết định việc bồi thường.

D05 chỉ gọi công cụ tra đơn một lần vì mã D999 không tồn tại. Các nhánh hỏi thông tin (D04, D13–D15), an toàn (D08, D09, D20), từ chối (D10, D11) và ngoài phạm vi (D16–D19) trả hướng dẫn trước khi tra đơn. Tổng cộng 14 câu có 0 lần gọi model và 0 token. Trace không ghi nhận model giả, lỗi gọi hoặc quyết định bị validator bác.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

Cột `error` trống ở cả 20 dòng. Hai câu D06 và D07 nhận cùng cách hỏi xác nhận một món dù nguyên nhân mơ hồ khác nhau. Cả hai câu đều yêu cầu xác nhận một món và đạt tiêu chí đã khóa. Run-1 có 0 câu trượt. [Quy tắc chấm và tập áp dụng](README.md#3-metric-và-cách-chấm).

## 3. Một lần cải tiến

Chưa thực hiện. Chưa có lượt 2 để so sánh.

## 4. Còn lại

Hai người chấm đồng thuận ở 5/5 câu đã chọn. Kết quả Run-1 phản ánh phạm vi của 20 câu và hai đơn hàng giả lập. [Điểm từng người và nhận xét](README.md#3-metric-và-cách-chấm).
