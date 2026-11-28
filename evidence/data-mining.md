# Đào review công khai — TV3 / CP3

Ngày thu: 28/11/2026; timestamp thực tế và hash trang nằm trong
[collection.json](public-reviews/collection.json). Không dùng dữ liệu prototype.

## 1. Chọn mẫu và cách đếm

Đã ghi [collection-plan.md](collection-plan.md) trước lần thu, rồi lưu
[coding-protocol.md](coding-protocol.md) trước phép đếm cuối. Đây là phân tích
exploratory có AI hỗ trợ; chưa có ngưỡng kiểm chứng giả thuyết được chốt ở CP2.
Không trình bày nó như một thử nghiệm xác nhận được đăng ký trước đầy đủ.

Nguồn: App Store Việt Nam ShopeeFood id1137866760; bốn trang customerreviews RSS
sortby=mostrecent, mọi mức sao. Trang 1/2/4 trả 50 review mỗi trang, trang 3 trả
0. Không thay trang rỗng bằng nguồn thuận lợi khác. Do khoảng trống trang 3,
**không gọi đây là 150 review mới nhất liên tiếp**. Các trang có thể đổi khi Apple cập nhật.

N=150 review có nội dung và source ID duy nhất; không có trùng hoặc rỗng
bị loại trong các trang trả dữ liệu. Khoảng ngày review theo snapshot: 2026-10-28–2026-11-26.
Giữ cả lời khen và nội dung không liên quan. Phân bố sao: {'1': 96, '2': 3, '3': 4, '4': 1, '5': 46}.
N không phải số khách, số đơn, số người Việt hay mẫu người dùng đại diện.

Mỗi dòng [reviews.csv](public-reviews/reviews.csv) lưu link trang, ID review,
ngày/sao, hash nội dung, tối đa một câu/25 từ gốc và hai nhãn cuối. Tác giả không
được lưu. Chỉ đọc đoạn trích để gắn nhãn cuối; các cột *_candidate từ regex toàn
bài chỉ gợi ý, không được tự coi là kết luận. Nhãn 0 là không có dấu hiệu trong
excerpt, không khẳng định toàn review hoặc trải nghiệm không có vấn đề đó.

Đã đọc pilot RV001–RV030 để thấy các loại nội dung: khen, ghép đơn/giao trễ,
lỗi app/thanh toán, phản ánh hỗ trợ/hoàn tiền. Sau đó AI rà 150 đoạn trích; chưa
có thành viên nhóm hoặc người thứ hai kiểm độc lập. Đây là giới hạn thực sự.

## 2. Kết quả chạy script trên snapshot

| Nhãn, theo định nghĩa đã lưu | x / N | % |
|---|---|---|
| Nói trực tiếp sự kiện nhận thiếu món (missing_food) | 0/150 | 0.00% |
| Phản ánh khó/bất mãn khi hỗ trợ hoặc hoàn tiền (complaint_difficulty) | 18/150 | 12.00% |
| Cùng dòng có cả hai nhãn | 0/150 | 0.00% |

Số 12% chỉ mô tả excerpt của mẫu lấy được, **không phải tỷ lệ khách hàng gặp
pain, lỗi của nền tảng hoặc tỷ lệ khiếu nại thiếu món**. 0/150 không chứng minh
thiếu món không xảy ra. Các review là tự báo cáo và chưa xác minh giao dịch.

## 3. Kiểm lại được

Từ root repo, không cần thêm package:

```powershell
py -3.12 evidence/count.py
```

Công thức: x = tổng nhãn 1; phần trăm = 100*x/N. Script kiểm ID, nhãn 0/1,
ngày, sao, nguồn, số từ trích và mẫu liên hệ phổ biến, rồi in JSON. So sánh với
[counts.json](public-reviews/counts.json). Script kiểm lại số đã mã hóa, không
chứng minh nhãn đúng hoặc tính đại diện. RV031 được để 0 dù regex đánh dấu,
RV003 là giả định nên không tính thiếu món; RV113 ẩn trích đoạn nghi tên riêng.

Muốn thu một đợt khác: `py -3.12 evidence/collect_reviews.py --output evidence/new-sample`.
Collector từ chối ghi đè snapshot; mẫu live mới có thể khác. Không gộp mẫu mới
vào mẫu cũ, không overwrite kết quả rồi gọi là cùng một lần nghiên cứu.

## 4. Ít nhất năm ví dụ có nguồn

Nguyên văn ngắn chỉ nằm tại cột excerpt trong CSV; không chép lại để tránh trích
quá dài. Mỗi ID bên dưới tra được source ID, link trang, ngày và hash:

| ID | Dấu hiệu quan sát từ trích đoạn | Giới hạn |
|---|---|---|
| RV013 | Chờ nói chuyện với hỗ trợ gây tốn thời gian | Không đo phút thao tác thực |
| RV037 | Phản ánh bằng chứng đã gửi không được xem | Lời một phía, chưa kiểm hệ thống |
| RV096 | Hỗ trợ lâu, vấn đề chưa giải quyết | Không nêu thiếu món |
| RV107 | Phản ánh quá mốc chờ 48h chưa được phản hồi | Thời gian tự báo cáo, không phải SLA đã xác nhận |
| RV138 | Bị trừ tiền nhưng đơn không thành công, chưa nhận hoàn | Không phải nhận thiếu một món |
| RV146 | Tự báo chờ hơn hai tháng chưa hoàn tiền | Không chuyển thành phút lao động hay bình quân |
| RV150 | Khó sửa thông tin sau khi đặt và không được hỗ trợ | Ngoài lát cắt thiếu món; không trích số liên hệ thật |

## 5. Kết luận và giới hạn

Có dấu hiệu friction hỗ trợ/hoàn tiền nói chung. **Chưa xác nhận trực tiếp giả
thuyết hẹp về người nhận thiếu món trong mẫu này**; cần thêm người đúng vai hoặc
một mẫu phù hợp khác, hoặc leader quyết định đổi trọng tâm. Không đổi Spec hay
ngưỡng prototype bằng kết quả mining này. E01 và tài liệu chính sách chỉ kiểm
bối cảnh, không đo prevalence hoặc chứng minh app hiện tại đúng/sai.

Review ngắn, tự chọn, iOS VN, có gap trang và cắt nội dung; người đăng không
được xác minh vai ngoài nhóm hoặc thời điểm sự cố. Ngày đăng không mặc định là
ngày sự cố. Chưa có phỏng vấn/khảo sát/pair-review thật. Không tuyên bố đã làm.
