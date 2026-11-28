# Reflection — Phan Nguyễn Phan Anh

1. Vai trò + phần mình làm (trỏ tới file / commit):
   Tôi phụ trách prototype, tích hợp AI và guardrails cho luồng khiếu nại thiếu một món.  
   Ở CP3, tôi triển khai [workflow](../codebase/agent.py), [kết nối OpenAI](../codebase/ai.py), [tool chỉ đọc](../codebase/tools.py) và kiểm thử tại commit [`4491b59`](https://github.com/haidangwork1411/K5-Day15-L3B-ChickenVietnamese/commit/4491b59).  
   Bản này kiểm món, giá và hạn mức trước khi tạo đề xuất; token lấy từ API, nhân viên xác minh và quyết định bồi thường.  
   Ở CP4, tôi cải tiến câu hỏi lại cho D06/D07 và bổ sung sáu test tại commit [`e87f5fc`](https://github.com/haidangwork1411/K5-Day15-L3B-ChickenVietnamese/commit/e87f5fc); [Run-2](../eval/report.md) ghi nhận hướng dẫn nêu rõ nơi đối chiếu tên món ở 2/2 câu, so với 0/2 ở Run-1.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   Trợ lý lập trình AI hỗ trợ viết workflow, prompt trả quyết định JSON, dữ liệu synthetic và test; ứng dụng dùng OpenAI Chat Completions ở CP3, sau đó nhóm tích hợp ERNIE qua OpenRouter.  
   Phần cần kiểm và sửa là quyết định model: code kiểm schema, cặp action/issue, món thuộc đơn và số tiền; phản hồi không hợp lệ được chặn hoặc chuyển nhân viên.  
   Tôi sửa câu hỏi lại còn chung chung thành hướng dẫn mở chi tiết đơn và gửi đúng tên một món đã đặt nhưng chưa nhận; kết quả được kiểm bằng [test hồi quy](../tests/test_safety.py) và hai lượt đánh giá.  
   [Hồ sơ kết nối](../docs/connect-model.md) ghi nhận smoke OpenAI của TV2 đạt ba câu; [khai báo dùng AI](../docs/ai-usage.md) nêu phạm vi hỗ trợ. Codex hỗ trợ đối chiếu Git và soạn bản reflection này.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   Trong smoke D01, `D100 thiếu cơm gà`, ERNIE từng trả cặp action/issue không hợp lệ và bị chặn trước khi nhóm bổ sung JSON Schema, theo [hồ sơ smoke](../docs/connect-model.md#smoke-ernie).  
   Đây là lỗi ở bước thử tích hợp model; [Run-1 và Run-2 chính thức](../eval/report.md) đều đạt 20/20 câu theo tiêu chí đã khóa.  
   Tôi rút ra rằng JSON đọc được vẫn cần kiểm ý nghĩa quyết định, món và hạn mức; schema phía API và validator trong code đều cần thiết.  
   Khi đổi model, cần thử cả ca đúng và ca sai, giữ dấu vết lỗi và chỉ tạo bản nháp để nhân viên duyệt; kết quả trên 20 câu và hai đơn giả lập còn giới hạn.
