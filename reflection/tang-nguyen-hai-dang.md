# Reflection — Tăng Nguyễn Hải Đăng

1. Vai trò + phần mình làm (trỏ tới file / commit):
   Tôi là đội trưởng, điều phối phân công và review, tích hợp phần của các bạn.  
   Tôi chuẩn bị Canvas, Spec và kiến trúc (`1cd01d3`, `58632f5`), hỗ trợ kiểm thử và xác minh kết quả.  
   Tôi chuẩn bị tài liệu, slide và hồ sơ checkpoint (`4623558`); sau CP4 bổ sung `demo_ui/` phục vụ demo.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   Tôi dùng Codex hỗ trợ phân tích yêu cầu, soạn tài liệu, review code, tạo test, đối chiếu artifact và dựng UI.  
   Tôi kiểm tra và sửa nội dung, duyệt diff và số liệu, chạy lệnh kiểm chứng và kiểm soát Git.  
   Phần prototype, nghiên cứu và đánh giá vẫn thuộc trách nhiệm các bạn tương ứng; tôi hỗ trợ tích hợp và xác minh.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   Khi thử D100 thiếu cơm gà qua UI sau CP4, yêu cầu cần model trả 502; CLI gọi model cũng lỗi.  
   Tôi kiểm tra endpoint của key và thấy quota miễn phí đã dùng 51/50; key chưa hết hạn tại lúc kiểm tra.  
   Tôi giữ thông báo lỗi, không chuyển ngầm sang mock; bài học là kiểm tra quota và chuẩn bị phương án dự phòng trước demo.  
   Đây là lỗi tích hợp sau CP4, không phải câu trượt của Run-1 hay Run-2; cả hai lượt đạt 20/20.
