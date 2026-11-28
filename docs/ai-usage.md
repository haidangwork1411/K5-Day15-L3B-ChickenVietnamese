# Khai báo dùng AI

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Prototype và prompt | Trợ lý lập trình; OpenAI Chat Completions trong ứng dụng | Hỗ trợ triển khai workflow, prompt quyết định JSON, tool chỉ đọc và kiểm hạn mức | TV2 ghi nhận smoke test 3 câu trong tài liệu kết nối model. Unit test dùng phản hồi mô phỏng. | Phan Nguyễn Phan Anh · `4491b59` |
| Nghiên cứu và impact | Trợ lý AI | Hỗ trợ thu RSS App Store, lập protocol, gắn nhãn đoạn trích và viết script đếm | Có thể tính lại trên 150 trích đoạn. Chưa ghi nhận số dòng người học kiểm tay. Impact dùng giả định CP2. | Vũ Văn Chủ · `f865765` |
| Bộ câu thử | Codex ở CP2; Claude Code được ghi ở D20 | Hỗ trợ soạn câu thử và tiêu chí. D13–D19 dùng trích đoạn của bảy review, mỗi dòng giữ mã nguồn. | Đối chiếu tự động ledger, excerpt và 12 câu CP2. Chưa có kết quả chấm giữa hai người. | Nguyễn Việt Hoàng · `f5b9bc2` (phần mở rộng) |
| Dữ liệu synthetic | Trợ lý AI | Hỗ trợ viết tay hai đơn và một chính sách, không dùng bộ sinh ngẫu nhiên | Code kiểm schema. Chưa ghi nhận số dòng kiểm tay. | Phần dữ liệu và prototype · Phan Nguyễn Phan Anh |
| Đánh giá | AI hỗ trợ đối chiếu sơ bộ ở CP2 | Đối chiếu năm câu trả lời với expected và tiêu chí đạt | Run-1 và chấm độc lập theo metric chưa thực hiện. | Nguyễn Việt Hoàng phụ trách lượt đánh giá |
| Tích hợp và tài liệu | Codex | Kiểm ba commit gốc, bổ sung provider OpenRouter và test phản hồi mô phỏng, sửa định tuyến an toàn và lỗi JSON, chuẩn hóa checksum, chạy kiểm thử offline, đồng bộ Spec, Canvas, hướng dẫn và kịch bản demo | Nhóm xác nhận smoke live 3/3 với JSON Schema trên `baidu/ernie-5.5-flash-preview:free` qua OpenRouter. Run-1 chưa chạy. [Số liệu từng ca](connect-model.md#smoke-ernie). | Tăng Nguyễn Hải Đăng |

Chưa thực hiện phỏng vấn hoặc khảo sát. Nguồn review, trích đoạn và kết quả quan sát được lưu trong [hồ sơ evidence](../evidence/summary.md).
