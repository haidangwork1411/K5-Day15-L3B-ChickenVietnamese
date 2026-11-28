# Impact — căn cứ và phần chưa đo

Ownership TV3: file này để TV1 tham khảo và tích hợp spec §2; không tự sửa Spec,
Canvas, cost/personas, metric hoặc dataset prototype. Không thay chuẩn đạt CP2.

## 1. Dữ liệu thật hiện có

- Mẫu AP01: 18/150 excerpt có khó/bất mãn về hỗ trợ/hoàn tiền; không đo số khách
  nhận thiếu món. Không lấy 12% × 100 khách để ước lượng người gặp thiếu món.
- RV013 chỉ ra thời gian chờ hỗ trợ; RV107 và RV146 có thời gian tự báo cáo nhưng
  đó là elapsed waiting, không phải số phút thao tác khiếu nại. Không đổi 48h/hai
  tháng thành C phút lao động hoặc tự nhận sản phẩm tiết kiệm toàn bộ thời gian đó.
- E01/P01/E03 xác nhận bối cảnh tranh chấp/chứng cứ, không có mẫu số người,
  tần suất/tháng hoặc phút tiết kiệm. Chưa có A/B hoặc người thử để đo cải thiện.

## 2. Nguồn từng thừa số của bảng CP2

Quy mô 100 khách trong spec §2 là kịch bản giả định, **không phải 100 người khảo sát**.
Giữ các số baseline để truy vết, không biến chúng thành đo thực tế.

| Hướng | N người gặp/tháng | F lần/người gặp/tháng | C phút phát sinh/lần | N×F×C phút/tháng | Căn cứ từng số |
|---|---|---|---|---|---|
| Thiếu món | 20 | 1.8 | 15 | 540 | Tất cả là tự ước tính của spec §2 ở baseline 58632f5; chưa có đo kiểm |
| Sai món | 15 | 1.2 | 10 | 180 | Tất cả tự ước tính, cùng nguồn spec §2 CP2 |
| Giao trễ | 25 | 1.2 | 5 | 150 | Tất cả tự ước tính, cùng nguồn spec §2 CP2 |

Nguồn nội bộ xác minh được: `git show 58632f5:spec.md`, không phải nguồn bên ngoài
chứng minh đầu vào đúng. JSON công thức ở impact-inputs.json; số người giữa các
hướng có thể trùng nhau, không cộng thành tổng số người độc lập. F áp dụng người
đã gặp vấn đề, không phải tần suất đặt món của mọi khách.

## 3. Độ nhạy minh họa cho hướng thiếu món

| Kịch bản tự ước tính | N | F | C | Phút/tháng |
|---|---|---|---|---|
| Thấp | 5 | 1 | 5 | 25 |
| Cơ sở CP2 | 20 | 1.8 | 15 | 540 |
| Cao | 40 | 3 | 30 | 3600 |

Đây là sensitivity, không phải khoảng tin cậy. Không có lý do thực nghiệm để
coi 540 là dự báo tốt nhất hay để khẳng định thiếu món đáng làm hơn giao trễ.
Nhìn riêng bảng giả định không đủ chứng minh ưu tiên sản phẩm.

## 4. Kết luận cho quyết định

**Iterate / cần kiểm thêm**, chưa chứng minh impact thực hoặc ROI. Có dấu hiệu
friction hỗ trợ nói chung nhưng pain thiếu món chưa được mẫu xác nhận trực tiếp.
TV1 quyết định giữ/đổi lát cắt; TV3 không tự chỉnh hướng để làm số đẹp.

Để thay đầu vào bằng số thật: xác định cohort người dùng theo tháng và log số
người gặp N; ghi số lần thực F trong cửa sổ cố định; đo active minutes C trước/sau,
tách khỏi chờ phản hồi. Mỗi người/phiếu có mã ẩn danh; không nhận là đã khảo sát.
Nhóm có thể dùng mining làm nguồn chính nên không buộc làm đủ cả ba phương pháp,
nhưng muốn kết luận mạnh cho lát cắt hẹp và R2 cần bổ sung dữ liệu phù hợp.
