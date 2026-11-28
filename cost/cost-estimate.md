# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

**Đã hoàn thành mô phỏng chính thức** simulate-1@20261128-122133 trên SHA 669752b2000cc1bde98672c60b0c78be74050434.

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

**Model đo token:** `baidu/ernie-5.5-flash-preview:free` qua OpenRouter, cùng model với Run-1. Chi phí theo hai model Gemini sẽ là token đo trên ERNIE nhân giá Gemini. Bộ tách token khác nhau nên số thật có thể lệch.

**Tỷ lệ đạt dùng để tính:** 20/20 (100%), Run-2 `run-2@20261128-120942`, cùng model ERNIE. Đây là tỷ lệ đạt benchmark; tỷ lệ khách thật giải quyết thành công chưa được đo.

## 2. Kết quả mô phỏng

Lượt `simulate-1@20261128-122133`, SHA `669752b2000cc1bde98672c60b0c78be74050434`. 50 phiên, seed 42, 89 lượt hỏi, 0/50 phiên lỗi. Phân bố phiên ít/vừa/nhiều là 19/23/8. Tổng 18.406 token vào, 4.707 token ra, 32 model calls và 69 tool calls. Tổng latency CSV 50,535 giây, trung bình 1,0107 giây/phiên; chưa gồm khoảng nghỉ giữa lượt hỏi.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (5 người) | Chi phí / tháng — cơ sở (20 người) | Chi phí / tháng — cao (40 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00023 | $0.00023 | $0.00013 | $0.0027 | $0.0109 | $0.0218 | $0.00055 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0013 | $0.0013 | $0.00071 | $0.0147 | $0.0589 | $0.1179 | $0.0029 |

Nguồn số đo và bảng làm tròn: [CSV](simulate-1.csv), [summary](simulate-1-summary.md), [trace](../traces/simulate-1.jsonl). Trace simulation ghi sự kiện model/tool; khung không ghi final cho mỗi lượt. 89 lượt được đối chiếu từ CSV với kế hoạch seed 42, gồm cả nhánh kết thúc trước khi gọi công cụ.

Mỗi phiên có chi phí giả định = (token vào × giá vào + token ra × giá ra) / 1.000.000. Chi phí/phiên là trung bình 50 phiên. Chi phí/task = trung bình này / 1,00. Chi phí/câu hỏi đạt chia thêm 89/50 = 1,78 lượt/phiên.

Chi phí tháng dùng trung bình chi phí phiên riêng từng persona, nhân số người dùng × tỷ trọng persona × số phiên/người/tháng rồi cộng ba nhóm. Vì vậy chi phí tháng có trọng số tần suất sử dụng; không lấy trung bình toàn mẫu nhân thẳng 36 phiên cơ sở. Chi phí/người/tháng bằng chi phí tháng cơ sở / 20. Các số trong bảng giữ cách làm tròn của simulator.

Token thực đo trên ERNIE được áp hai biểu giá Gemini từ bảng BTC. Chưa đo chất lượng hai model Gemini; khác biệt tokenizer và hành vi có thể làm chi phí thật thay đổi. Các giá trị là ước tính triển khai theo biểu giá, chưa phải hóa đơn API thực trả.

## 3. So với impact

- Impact / người gặp sự cố / tháng (`spec.md` §2): 1,8 lần × 15 phút = 27 phút *(tự ước tính)*. Đây là thời gian phát sinh giả định, **chưa phải thời gian tiết kiệm được**.
- Chi phí token/người/tháng cơ sở là $0.00055 với Flash-Lite và $0.0029 với Hydrogen theo biểu giá giả định.
- **Đề xuất ITERATE.** Chi phí token ước tính thấp, nhưng 27 phút/người là tổn thất giả định, chưa đo phần tiết kiệm. Cần kiểm chứng lợi ích, tỷ lệ hoàn tất và thời gian nhân viên duyệt trước quyết định triển khai.

## 4. Giới hạn

- Chưa có log sử dụng: số người dùng, tỷ trọng persona, tần suất và số lượt hỏi đều là giả định.
- `answer()` không lưu ngữ cảnh giữa các lượt, nên mô phỏng nhiều lượt chưa chứng minh khách hoàn tất được hội thoại làm rõ.
- Chi phí token chưa gồm hosting, lưu trữ và giờ công nhân viên duyệt. Giá token bằng 0 ở gói miễn phí không có nghĩa chi phí vận hành bằng 0.
