# Khai báo dùng AI

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Prototype và prompt | Trợ lý lập trình; OpenAI Chat Completions trong ứng dụng | Hỗ trợ triển khai workflow, prompt quyết định JSON, tool chỉ đọc và kiểm hạn mức | TV2 ghi nhận smoke test 3 câu trong tài liệu kết nối model. Unit test dùng phản hồi mô phỏng. | Phan Nguyễn Phan Anh · `4491b59` |
| Nghiên cứu và impact | Trợ lý AI | Hỗ trợ thu RSS App Store, lập protocol, gắn nhãn đoạn trích và viết script đếm | Có thể tính lại trên 150 trích đoạn. Chưa ghi nhận số dòng người học kiểm tay. Impact dùng giả định CP2. | Vũ Văn Chủ · `f865765` |
| Bộ câu thử | Codex ở CP2; Claude Code được ghi ở D20 | Hỗ trợ soạn câu thử và tiêu chí. D13–D19 dùng trích đoạn của bảy review, mỗi dòng giữ mã nguồn. | Đối chiếu tự động ledger, excerpt và 12 câu CP2. | Nguyễn Việt Hoàng · `f5b9bc2` (phần mở rộng) |
| Dữ liệu synthetic | Trợ lý AI | Hỗ trợ viết tay hai đơn và một chính sách, không dùng bộ sinh ngẫu nhiên | Code kiểm schema. Chưa ghi nhận số dòng kiểm tay. | Phần dữ liệu và prototype · Phan Nguyễn Phan Anh |
| Đánh giá | Trợ lý AI | Đối chiếu 5 output sơ bộ ở CP2 và đề xuất điểm cho 20 output Run-1 theo benchmark và metric đã khóa | Đội trưởng đã duyệt điểm của 20 câu. Hai người chấm cho cùng kết quả trên 5 câu đã chọn. [Điểm và nhận xét](../eval/README.md#3-metric-và-cách-chấm). | Nguyễn Việt Hoàng phụ trách lượt đánh giá |
| Tích hợp và tài liệu | Codex | Hỗ trợ tích hợp OpenRouter, kiểm thử định tuyến và xử lý JSON, kiểm tra checksum và cập nhật tài liệu kỹ thuật | Nhóm xác nhận smoke live 3/3 với JSON Schema trên `baidu/ernie-5.5-flash-preview:free` qua OpenRouter. [Số liệu từng ca](connect-model.md#smoke-ernie). | Tăng Nguyễn Hải Đăng |

Chưa thực hiện phỏng vấn hoặc khảo sát. Nguồn review, trích đoạn và kết quả quan sát được lưu trong [hồ sơ evidence](../evidence/summary.md).

Codex hỗ trợ dựng nội dung và source PDF 8 trang từ hồ sơ CP3, kiểm tra bố cục và chuẩn bị Spec CP4. Hải Đăng phụ trách xác nhận nội dung trình bày. Run-2 đã có kết quả được duyệt; chi phí đã đối chiếu simulation chính thức.

Codex hỗ trợ review bản TV2/TV3 trong snapshot cô lập, chạy kiểm thử offline, đối chiếu sáu URL nguồn bổ sung và cập nhật slide dự thảo theo SHA đã merge vào main. Rà nhãn của TV3 là AI-assisted; số kiểm tay có log vẫn là 0, tổng thực tế chưa xác định.

Codex đối chiếu 20 output Run-2 với benchmark và trace, hỗ trợ chấm điểm đã được đội trưởng duyệt và đo chỉ số nội dung hướng dẫn trên D06/D07. Phép đo UX này chưa có người dùng thực nghiệm.

Codex đối chiếu CSV/trace simulation, tái tính bảng chi phí bằng logic khung, cập nhật hồ sơ CP4 và render PDF. Người phụ trách chạy thực nghiệm và duyệt điểm Run-2 là Hải Đăng. Các phép tính chi phí dùng token ERNIE và biểu giá Gemini giả định; chất lượng Gemini chưa đo.
