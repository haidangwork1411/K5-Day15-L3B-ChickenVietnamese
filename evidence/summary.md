# Tổng hợp Research, Evidence & Impact — TV3 / CP3

Ngày thu mẫu: 28/11/2026. Bộ evidence do Vũ Văn Chủ phụ trách, tích hợp từ commit `f865765`.

## 1. Số chính và kết luận

Nguồn chính AP01 là **150 review App Store ShopeeFood VN**, mọi mức sao, từ các
trang được chọn trước; một trang rỗng, không có mẫu mới nhất liên tiếp hoàn chỉnh.
**18/150 (12.00%)** excerpt phản ánh khó/bất mãn hỗ trợ hoặc hoàn tiền;
**0/150 (0.00%)** excerpt nói trực tiếp nhận thiếu món; giao hai nhãn **0/150**.
Không suy tỷ lệ người dùng, số đơn hoặc phần trăm khách thiếu món từ các số này.

**Kết luận: cần kiểm thêm/đổi giả thuyết**, không tuyên bố pain thiếu món đã được
xác nhận. Dấu hiệu về hỗ trợ nói chung có thật trong nguồn công khai, nhưng không
đủ để nhận định nguyên nhân là khách không biết thông tin khiếu nại cần cung cấp.
0/150 không chứng minh không ai nhận thiếu món. [Hypothesis](hypothesis.md).

## 2. Nguồn, phương pháp và mức hoàn thành

| Hạng mục | Đã có | Giới hạn / chưa có |
|---|---|---|
| Đào review có cách chọn, mẫu số, số đếm và script | collection-plan, coding-protocol, CSV 150 dòng, count.py, counts.json | AI gắn nhãn excerpt; chưa có người thứ hai kiểm, gap trang 3 |
| ≥5 ví dụ có nguồn, bỏ tác giả | RV013/RV037/RV096/RV107/RV138/RV146/RV150 và các excerpt trong CSV | Tự báo cáo, chưa xác minh giao dịch hoặc vai người viết |
| Nguồn thứ hai kiểm bối cảnh | E01 báo chí; P01/E03 tài liệu chính thức đã đọc | Không độc lập xác nhận x/N, không thay thế phỏng vấn người đúng vai |
| Phỏng vấn ≥3 / khảo sát ≥20 | Không thực hiện, không bắt buộc nếu mining được chấp nhận | Không tạo file P1/P2/P3 hay response giả |
| Impact có nguồn từng thừa số | Truy vết mọi số CP2 về spec §2, có công thức/độ nhạy | N/F/C vẫn tự ước tính, không thể báo impact thực hoặc đủ trọn R2 |
| Bàn giao nguồn cho TV4 | 10 tình huống riêng trong source-cases.csv, có source/date/ref/scope/limits | Không phải 10 benchmark case đã duyệt; một số là boundary/nguồn chính sách |
| Cá nhân, làm theo cặp, review người thật | Chưa có ghi nhận thực hiện | Chưa có biên bản xác nhận |

[data-mining.md](data-mining.md) có phương pháp, bảng số và ví dụ.
[sources.md](sources.md) phân biệt review/báo chí/chính sách/nguồn chưa truy cập.
[impact.md](impact.md) tách số quan sát và giả định.

## 3. Provenance cho TV4

[source-cases.csv](source-cases.csv): SC01–SC10 có Evidence ID, loại nguồn,
URL/ref, ngày, ngữ cảnh, diễn giải ẩn danh, mức xác minh và giới hạn. Bảy cơ chế
khác nhau có thể xem xét: thiếu chứng cứ, chứng cứ bị bỏ qua, chờ agent hỗ trợ,
quá hẹn phản hồi, trừ tiền nhưng không tạo đơn, sai thông tin liên hệ, yêu cầu
trả thêm ship; còn có ca không nhận đơn và bối cảnh an toàn/chính sách.
Benchmark dùng bảy review riêng biệt SC02–SC08 cho D13–D19. Các ca này mô tả ranh giới hỗ trợ, thanh toán và giao nhận.

## 4. Giới hạn khi sử dụng

Mẫu chưa xác nhận trực tiếp pain thiếu món. Kịch bản 540 phút/tháng trong Spec dùng các hệ số tự ước tính. Chưa có kiểm nhãn độc lập hoặc đo hiệu quả với người dùng.

## 5. Kiểm tra lại

Từ thư mục gốc, chạy `python3 evidence/count.py` để đếm và `python3 evidence/verify.py` để đối chiếu với metadata, nguồn từng tình huống và phép tính impact. Verifier tính SHA-256 trên byte CSV sau khi thay CRLF bằng LF; giữ nguyên BOM, nội dung, thứ tự dòng và khoảng trắng. Việc đổi một giá trị vẫn làm sai checksum. Có thể kiểm phạm vi đóng góp gốc riêng bằng `git diff --name-status 58632f5 f865765`. Các bản ghi `verification.json` và `project-check.txt` lưu kết quả lịch sử trên nhánh nghiên cứu.

## 6. AI log và quyền riêng tư

AI hỗ trợ gắn nhãn trên trích đoạn; chưa có số dòng được người học xác nhận kiểm tay. [Khai báo sử dụng AI](../docs/ai-usage.md).

Collector bỏ tác giả/title/raw payload, giữ tối đa một câu/25 từ gốc mỗi review;
RV113 không trích vì có thể nêu tên riêng. Không công bố dữ liệu đơn thật hoặc
email/điện thoại. Không có giấy phép mở cho cả kho; chỉ trích ngắn có nguồn để
phân tích, không tái phân phối nguyên nội dung. Chưa có người duyệt pháp lý/quyền
tái sử dụng toàn bộ; không nhận đã được cấp quyền đó.
