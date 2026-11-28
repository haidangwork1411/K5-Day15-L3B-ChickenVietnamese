# Kế hoạch thu review công khai — TV3 / CP3

- Ngày đăng ký: 28/11/2026 (Asia/Bangkok), trước khi lấy nội dung review cho đợt này.
- Baseline: 58632f5f794120b4efbabaef75f480b3171edf7d; branch local cp3/tv3-evidence.
- Phương pháp: đào review công khai, không phỏng vấn/khảo sát giả và không sử dụng data prototype làm evidence.
- Nguồn chính: App Store Việt Nam, app khách hàng ShopeeFood id1137866760. Chọn tối đa 200 review gần nhất qua customerreviews RSS, sortBy=mostRecent, page=1..4; giữ mọi mức sao, mọi vấn đề, không dừng khi đủ review tiêu cực.
- Nếu nguồn chính không truy cập được hoặc ít hơn 30 review, ghi thất bại rồi dùng App Store Việt Nam Grab id647268330, cùng quy tắc 4 trang. Không gộp hai app vào một mẫu số; công bố app thực sự dùng.
- Pilot: đọc 30 review đầu để hiểu loại nội dung; khóa định nghĩa nhãn trong data-mining.md trước khi chạy phép đếm chính thức trên toàn bộ mẫu. Pilot vẫn nằm trong mẫu, không lấy nó làm tập kiểm chứng độc lập.
- Đơn vị phân tích: một review ID công khai duy nhất; loại bản trùng ID giữa các trang, giữ bản xuất hiện đầu. N là số review có nội dung không trống và đã đọc/gắn nhãn, kể cả không liên quan hoặc tích cực. Không suy số người dùng hoặc số đơn từ N.
- Tử số dự kiến: (A) nhắc nhận thiếu món/thành phần; (B) khó khiếu nại/xác minh/nhận hoàn tiền; (C) vừa thiếu món vừa khó khiếu nại. Mỗi nhãn phải căn cứ câu chữ, không suy diễn. Sai món, giao trễ, lỗi app phải tách khỏi thiếu món.
- Phân tích là mô tả mẫu thuận tiện; không dùng x/N review để ước lượng tỷ lệ khách gặp lỗi. Review tự báo cáo, chưa xác minh giao dịch và không xác nhận tháng xảy ra nếu tác giả không nói.
- Quyền riêng tư: không lưu tác giả, tên tài khoản, địa chỉ, điện thoại, email hoặc mã đơn; không đưa nguyên response RSS vào repo. Chỉ giữ review ID nguồn, link, ngày review/ngày thu, sao, tối đa 2 câu trích ẩn danh, hash nội dung và nhãn. Nếu nội dung có PII, bỏ/che và đánh dấu.
- Quyền sử dụng: chỉ trích ngắn để phân tích có dẫn nguồn; không có giấy phép tái phân phối toàn bộ kho review, không thu vượt trang công khai, không dùng nội dung trả phí/đòi đăng nhập. Không gọi quyền công khai là giấy phép mở.
- Bàn giao: các tình huống có Evidence ID, nguồn, ngày, ngữ cảnh, mức xác minh và giới hạn ngay trong evidence/; TV4 tự viết case và expected theo spec, TV3 không sửa benchmark/metric/spec.
- Impact: số đo nào không có nguồn để trống hoặc ghi tự ước tính; không biến giả định 100 khách thành khảo sát. Không tuyên bố thời gian tiết kiệm trước thử người dùng.
- Ngưỡng hoàn thành: một nguồn có x/N, %, công thức/script kiểm lại và ít nhất 5 ví dụ; hướng tới ít nhất 7 tình huống nguồn khác bản chất để TV4 xem xét. Nếu thiếu phải báo rõ.
- Hoạt động cá nhân/làm theo cặp và duyệt người thật chưa diễn ra qua công cụ này; không ghi đã diễn ra. Không stage/commit/push; người học review diff và tự push theo yêu cầu.
