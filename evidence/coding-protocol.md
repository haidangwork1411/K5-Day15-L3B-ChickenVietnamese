# Khóa cách gắn nhãn trước phép đếm chính thức

Ngày 28/11/2026, đợt TV3 exploratory. Kế hoạch chọn nguồn và mẫu đã lưu trong
collection-plan.md trước khi lấy nội dung. Đã đọc pilot 30, sau đó rà các đoạn
trích thu được; việc tinh chỉnh định nghĩa dưới đây là exploratory, không phải
đăng ký trước giả thuyết độc lập. Không đổi chuẩn đạt prototype/spec/metric CP2.

## Mẫu số

N = số review ID riêng biệt, có nội dung, thu từ đúng 4 trang đã định của app
ShopeeFood VN; mọi mức sao được giữ. Trang trả rỗng không được bù bằng trang
thuận lợi khác. Dữ liệu là lời người viết tự báo cáo, không phải đơn/khách đã xác minh.

## Hai nhãn kết luận (đọc đoạn trích ngắn đã ẩn danh)

- missing_food=1: đoạn trích nói một sự kiện thực tế nhận đơn thiếu món/thành phần
  được đặt. Không tính giao chậm, không giao toàn đơn, sai món, thiếu trách nhiệm,
  hoặc câu hỏi giả định. 0 = không quan sát thấy trong trích đoạn; không có nghĩa
  chắc chắn người đó chưa từng gặp thiếu món hoặc toàn bộ review không nói tới.
- complaint_difficulty=1: đoạn trích thể hiện khó khăn/bất mãn rõ ràng với hỗ trợ,
  phản hồi, xử lý tranh chấp hoặc nhận hoàn tiền; không chỉ suy từ số sao. Không
  tính lời chê chung chung không nêu cơ chế, giao chậm đơn thuần hoặc khen hỗ trợ.
  Đây là phản ánh của reviewer, không phải phán quyết ứng dụng đã sai.
- Intersection = cả hai nhãn bằng 1 trên cùng một dòng. Không cộng hai tỷ lệ để
  suy ra giao nhau. Các nhãn không loại trừ nhau.

Các cột *_candidate là kết quả dò từ khóa toàn nội dung trong bộ thu, chỉ dùng
gợi ý rà soát, không thay nhãn cuối. Nhãn cuối do AI hỗ trợ rà excerpt; chưa có
người học hoặc người thứ hai kiểm độc lập. coding_note phải nói cơ sở/giới hạn.

## Công thức và giới hạn

x=sum(int(row[label]) for row in rows); percent=100*x/N. Đếm trên snapshot CSV
đã lưu, không lấy mẫu số tổng rating App Store. Kiểm ID duy nhất, tất cả nhãn đã
điền 0/1, nguồn/ngày/sao hợp lệ, trích không quá 25 từ gốc/review, không tên tác giả.
Đoạn trích giới hạn một câu/25 từ có thể bỏ mất ngữ cảnh: kết quả là lower-bound
của dấu hiệu nhìn thấy trong đoạn trích, không phải ước lượng prevalence thực.

Không đặt ngưỡng pain sau khi nhìn kết quả để tuyên bố giả thuyết được xác nhận.
Nếu nhãn thiếu món không có quan sát, kết luận hẹp là chưa đủ evidence; dùng
nguồn báo chí/chính sách riêng để giải thích bối cảnh, không cộng vào N review.

Không suy tần suất/tháng, số khách hoặc số phút từ review tự chọn. Giữ nguyên
những đầu vào impact của CP2 dưới nhãn tự ước tính, trình bày độ nhạy và phần chưa đo.
