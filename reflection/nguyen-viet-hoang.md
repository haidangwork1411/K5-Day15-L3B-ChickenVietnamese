# Reflection — Nguyễn Việt Hoàng

1. Vai trò + phần mình làm (trỏ tới file / commit):
   Tôi là TV4, phụ trách benchmark, evaluation và mô phỏng chi phí.
   Ở CP3, tôi mở rộng `eval/benchmark.csv` từ 12 lên 20 câu (thêm 7 câu từ trích đoạn review công khai và 1 câu an toàn tự viết), ghi nguồn, giới hạn và cách chấm trong `eval/README.md` (`f5b9bc2`).
   Ở CP4, tôi làm cấu hình 3 persona, 50 phiên, giá 2 mức model và 3 kịch bản người dùng trong `cost/personas.yaml`, `cost/cost-estimate.md` (`08cff09`). Số người dùng và tần suất là tự ước tính.
   Run-2, simulation chính thức và phần kết quả chi phí bổ sung sau đó không nằm trong hai commit này.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   Công cụ: Claude Code.
   Việc được hỗ trợ: soạn D13–D20 (kèm expected, tiêu chí đạt) và soạn cấu hình chi phí.
   Ngoài ra: kiểm tra offline và thao tác Git; commit, push được thực hiện khi tôi đồng ý.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   Run-1 và Run-2 đều đạt 20/20. Ví dụ này lấy từ bản trước Run-1, chạy offline, không phải lượt chính thức.
   D16 là review “đã trừ tiền nhưng đơn lại ko thành công và cũng chả hoàn tiền”. Prototype `4491b59` trả lời bằng cách hỏi mã đơn và món thiếu, nên trượt tiêu chí: ca này ngoài phạm vi, cần chuyển nhân viên (D18, D19 cũng vậy).
   Ở bản `970a909` dùng cho Run-1, D16 đã chuyển nhân viên. Cả hai bản đều trả lời D16 bằng luật trong code, không gọi model.
   Tôi rút ra: phải thử cả ca ngoài phạm vi bằng lời người dùng thật, giữ nguyên expected khi output chưa đạt; 20/20 trên bộ câu đã biết chưa chứng minh hệ thống xử lý đúng câu mới.
