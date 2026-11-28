# Canvas — ChickenVietnamese · Track D

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".
> Track F: chép thêm thẻ đề của nhóm (khung trong file track F) xuống dưới bảng này.

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến |  Track D — E-commerce, hướng D1: Hỗ trợ xử lý khiếu nại đơn giao đồ ăn bị thiếu món. |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") |  Khách hàng đặt đồ ăn qua ứng dụng và nhận đơn hàng không đầy đủ số món đã đặt. |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả |  Nhóm đặt giả thuyết rằng khách hàng nhận đơn giao đồ ăn bị thiếu món gặp khó khăn và mất thời gian khi xác định thông tin cần cung cấp và phương án khiếu nại phù hợp. |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | 18/150 trích đoạn review phản ánh khó khăn hỗ trợ/hoàn tiền. RV013 viết “tốn hết cả thgian”. 0/150 trực tiếp nêu việc nhận thiếu món. E01 là nguồn báo chí thứ cấp. [Nguồn và giới hạn mẫu](evidence/summary.md). |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Khi khách báo thiếu một món, hệ thống tra đơn và chính sách giả lập, dùng `baidu/ernie-5.5-flash-preview:free` qua OpenRouter để đề xuất bước tiếp theo để nhân viên duyệt. |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì |  AI hỗ trợ phân tích và đề xuất phương án; nhân viên có thẩm quyền quyết định việc hoàn tiền hoặc bồi thường nhằm hạn chế xử lý sai chính sách, vượt hạn mức hoặc thực hiện giao dịch không phù hợp. Không tự động thực hiện giao dịch hoàn tiền thật. |
| 7 | Phân công có tên |  Tăng Nguyễn Hải Đăng — CP1, CP2, Canvas, Spec, kiến trúc và tích hợp; Phan Nguyễn Phan Anh — prototype, AI integration và guardrails; Vũ Văn Chủ — research, evidence và impact; Nguyễn Việt Hoàng — benchmark, evaluation và cost simulation. |
| — | *(CP2)* Đã đổi gì so với CP1 | Đã bổ sung nguồn báo chí thứ cấp E01, workflow mock và benchmark; chưa có số đếm và trích dẫn trực tiếp. |

Trong kịch bản tự ước tính trên 100 khách, thiếu món có impact 540 phút/tháng, sai món 180 và giao trễ 150. Nhóm chọn thiếu món vì có thể đối chiếu một món, giá và hạn mức ngay trong bản thử. [Giả định và công thức](evidence/impact.md).
