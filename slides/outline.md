# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | ☐ |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | ☐ |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | ☐ |
| 4 | Demo live | 1 trường hợp thường + 1 trường hợp khó (lấy từ bộ câu thử); mạng hỏng → video dự phòng | `eval/benchmark.csv` | ☐ |
| 5 | **Đánh giá thế nào** | Dataset · bộ câu thử · metric · lượt 1 → lượt 2 so với chuẩn "đạt" (kèm run ID) · lỗi chính | `eval/README.md`, `eval/report.md` | ☐ |
| 6 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | ☐ |
| 7 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6 | — | ☐ |
| 8 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | ☐ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| 1–2 | Vũ Văn Chủ |
| 3–4 | Phan Nguyễn Phan Anh |
| 5–6 | Nguyễn Việt Hoàng |
| 7–8 | Tăng Nguyễn Hải Đăng |


## Hồ sơ trình bày CP4

PDF gồm đủ 8 trang theo rubric, số liệu từ hai lượt đánh giá và simulation chính thức. Source `slides/build_pdf.py` cần Python, ReportLab và font DejaVu Sans. Chạy `python3 slides/build_pdf.py` để tái tạo.

## Kịch bản demo

Phan Anh mở CLI đã cấu hình OpenRouter và ERNIE. Nhập `D100 thiếu cơm gà`, chỉ giá 50.000, trần 40.000 VND, bước nhân viên duyệt, model và token. Tiếp theo nhập `D100 thiếu pizza`, giải thích câu hỏi xác nhận món và việc chưa có căn cứ đề xuất tiền. Quan sát output thật trên bản tích hợp, ghi nhận nếu có lỗi. Mỗi ca dành khoảng 30–45 giây. Video CP3 trong README dự phòng ca thường; nhóm cần tự diễn tập ca khó.

## Checklist trước khi nộp

- [ ] Xác nhận phòng và zone được BTC phân, link form CP4; L3B có C401/E403.
- [ ] Thử README trên máy demo, cấu hình API key cục bộ ngoài khung hình; người phụ trách tự gọi thử một câu trong vòng 1 giờ trước demo.
- [ ] Chốt SHA demo, model, Run-2 và cost; kiểm PDF 8 trang, font tiếng Việt, nguồn và số liệu.
- [ ] Mở video bằng cửa sổ ẩn danh, chuẩn bị bản MP4 đã có trên máy demo.
- [ ] Cả bốn thành viên tập phần nói và câu hỏi giám khảo.
- [ ] Rà soát nhóm 15 phút, ghi nhận đúng hoạt động đã diễn ra.
- [ ] Điền form trước 14:30 với phòng, repo, 7 hạng mục, hai run ID và x/N, chi phí/task cơ sở kèm model, PDF, video, phần thiếu.

## Số liệu đã chốt

- Run-1 `run-1@20261128-092900`, Run-2 `run-2@20261128-120942`: cùng đạt 20/20; ba metric 20/20, 4/4, 5/5.
- Run-2 SHA `7b639e0`; hai câu cải thiện UX 0/2 → 2/2, 18 output giữ nguyên. Token ra tăng 198, tổng latency tăng 2,003 giây; nguyên nhân usage tăng chưa xác định.
- Simulation `simulate-1@20261128-122133`, SHA `669752b`: 50 phiên, 89 lượt hỏi, seed 42, 0 lỗi. 18.406 token vào, 4.707 token ra; 32/69 model/tool calls.
- Cost/task $0.00023 / $0.0013 theo hai tầng giá; cơ sở $0.0109 / $0.0589 mỗi tháng. Công thức và nguồn ở `cost/cost-estimate.md`.
- Giới hạn R5: Run-1 có 0 câu trượt, thiếu ba lỗi theo rubric. Chưa có bằng chứng hoạt động nghiên cứu cá nhân/cặp, kiểm tay nhãn và bonus người dùng thử đầy đủ.
- Đề xuất ITERATE. Các ô checklist ở trên cần người phụ trách trực tiếp xác nhận sau khi thực hiện.
