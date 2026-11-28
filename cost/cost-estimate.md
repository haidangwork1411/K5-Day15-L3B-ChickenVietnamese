# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

**Trạng thái:** đã có cấu hình đầu vào. **Chưa chạy mô phỏng**, nên chưa có số đo token và chi phí.

## 1. Đầu vào

**Persona** (`cost/personas.yaml`), tất cả *(tự ước tính)*:

| Persona | Tỷ trọng người dùng | Phiên / người / tháng | Lượt hỏi / phiên |
|---|---:|---:|---:|
| khieu_nai_it | 40% | 1 | 1 |
| khieu_nai_vua | 40% | 2 | 2 |
| khieu_nai_nhieu | 20% | 3 | 3 |

Trung bình mỗi người dùng trợ lý: 1,8 phiên và 3,8 lượt hỏi mỗi tháng. Số phiên theo [spec.md §2](../spec.md); số lượt hỏi theo [đề xuất của TV3](../evidence/cp4/cost-handoff.json).

**Ba kịch bản** *(tự ước tính)*. Số người là khách gặp sự cố có dùng trợ lý trong tháng, trong cohort giả định 100 khách nền. Giả định 100% khách gặp sự cố dùng trợ lý; khi có số adoption thật phải tính lại.

| Kịch bản | Người dùng trợ lý | Phiên / tháng | Lượt hỏi / tháng |
|---|---:|---:|---:|
| Thấp | 5 | 9 | 19 |
| Cơ sở | 20 | 36 | 76 |
| Cao | 40 | 72 | 152 |

Ba kịch bản chỉ đổi số người dùng và giữ nguyên persona. Bảng độ nhạy impact trong [evidence/impact.md](../evidence/impact.md) đổi cả số người, tần suất và số phút, nên không so trực tiếp hai bảng.

**Giá hai mức model**, USD / 1 triệu token, giá chuẩn gói trả phí, chưa thuế. Nguồn: [bảng giá BTC](../further-reading/model-prices.md), BTC tra [trang giá chính thức](https://ai.google.dev/gemini-api/docs/pricing) ngày 25/11/2026.

| Mức | Model | Giá vào | Giá ra |
|---|---|---:|---:|
| Rẻ | gemini-3.1-flash-lite | 0,25 | 1,50 |
| Mạnh | gemini-4-hydrogen | 1,50 | 7,50 |

**Cấu hình mô phỏng:** 50 phiên · seed 42 · đầu vào lấy từ câu `thuong` và `kho` trong `eval/benchmark.csv`. Với bộ câu hiện tại, cấu hình này sinh 89 lượt hỏi.

**Model đo token:** dự kiến `baidu/ernie-5.5-flash-preview:free` qua OpenRouter, cùng model với Run-1. Chi phí theo hai model Gemini sẽ là token đo trên ERNIE nhân giá Gemini. Bộ tách token khác nhau nên số thật có thể lệch.

**Tỷ lệ đạt dùng để tính:** chưa chốt. Run-2 chưa chạy. Run-1 đạt 20/20 nhưng chạy trên code trước thay đổi câu hỏi làm rõ của TV2.

## 2. Kết quả mô phỏng

Lượt mô phỏng: chưa chạy.

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gemini-3.1-flash-lite | chưa đo | chưa đo | chưa tính | chưa tính | chưa tính | chưa tính |
| gemini-4-hydrogen | chưa đo | chưa đo | chưa tính | chưa tính | chưa tính | chưa tính |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người gặp sự cố / tháng (`spec.md` §2): 1,8 lần × 15 phút = 27 phút *(tự ước tính)*. Đây là thời gian phát sinh giả định, **chưa phải thời gian tiết kiệm được**.
- Chi phí / người / tháng: chưa tính.
- **Kết luận đáng làm không:** chưa kết luận.

## 4. Giới hạn

- Chưa có log sử dụng: số người dùng, tỷ trọng persona, tần suất và số lượt hỏi đều là giả định.
- `answer()` không lưu ngữ cảnh giữa các lượt, nên mô phỏng nhiều lượt chưa chứng minh khách hoàn tất được hội thoại làm rõ.
- Chi phí token chưa gồm hosting, lưu trữ và giờ công nhân viên duyệt. Giá token bằng 0 ở gói miễn phí không có nghĩa chi phí vận hành bằng 0.
