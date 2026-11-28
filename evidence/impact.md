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
- [Nguồn CP4](cp4/README.md) bổ sung lời kể thiếu món và khó bồi hoàn ở bối cảnh
  Singapore, cùng báo cáo nền tảng; không cung cấp đầu vào N/F/C cho nhóm.

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
friction hỗ trợ nói chung nhưng pain thiếu món chưa được mẫu AP01 xác nhận trực tiếp.
TV1 quyết định giữ/đổi lát cắt; TV3 không tự chỉnh hướng để làm số đẹp.

Để thay đầu vào bằng số thật: xác định cohort người dùng theo tháng và log số
người gặp N; ghi số lần thực F trong cửa sổ cố định; đo active minutes C trước/sau,
tách khỏi chờ phản hồi. Mỗi người/phiếu có mã ẩn danh; không nhận là đã khảo sát.
Nhóm có thể dùng mining làm nguồn chính nên không buộc làm đủ cả ba phương pháp,
nhưng muốn kết luận mạnh cho lát cắt hẹp và R2 cần bổ sung dữ liệu phù hợp.

## 5. Kiểm tra mẫu số cơ sở cho CP4

Các số dưới đây đều là **tự ước tính**, truy về bảng CP2; không phải số người
được khảo sát hoặc thời gian tiết kiệm đã quan sát.

| Đại lượng | Công thức | Giá trị |
|---|---|---:|
| Khách nền trong kịch bản | Giả định quy mô | 100 người |
| Khách gặp khiếu nại thiếu món | N, không lấy từ 18/150 review | 20 người |
| Phiên khiếu nại mỗi tháng | 20 × 1,8 | 36 phiên |
| Tổn thất thao tác mỗi tháng | 36 × 15 | 540 phút |
| Tổn thất trên người gặp sự cố | 540 / 20 | 27 phút/người/tháng |
| Tổn thất trên khách nền | 540 / 100 | 5,4 phút/khách/tháng |

Một phiên là một sự cố khiếu nại; lượt hỏi bổ sung trong cùng phiên không tự
tạo thêm một sự cố hoặc nhân thêm 15 phút. Không coi 540 phút là lượng tiết kiệm
khả thi toàn bộ. Muốn tính lợi ích cần đo cùng công việc trước/sau, mức sử dụng
và số phút thực sự giảm. Thời gian chờ phản hồi phải được ghi riêng.

Sai món vẫn là 15 × 1,2 × 10 = 180 phút/tháng; giao trễ là 25 × 1,2 × 5 = 150
phút/tháng. Cả hai hướng đều tự ước tính và ngoài lát cắt prototype. Không cộng
người giữa các hướng vì có thể trùng, không cộng 540 + 180 + 150 thành lợi ích
trong phạm vi trợ lý thiếu một món.

## 6. Đầu vào đề xuất cho mô phỏng TV4

[cost-handoff.json](cp4/cost-handoff.json) lưu cấu hình dữ liệu để TV4 rà soát;
nhánh này không sửa `cost/personas.yaml`. Tất cả là **tự ước tính**, chưa có
log sử dụng hoặc trao đổi hai bên được xác nhận.

Mẫu số `users` là người gặp sự cố có dùng trợ lý trong tháng. Giả định tỷ lệ
sử dụng trong nhóm gặp sự cố là 100%; khi có số adoption thực phải cập nhật
người dùng trợ lý = khách gặp × adoption. Không dùng 100 khách nền làm số
người dùng trợ lý nếu chỉ có 20 khách gặp sự cố.

| Persona giả định | Share trong người dùng trợ lý | Phiên/người/tháng | Lượt hỏi/phiên |
|---|---:|---:|---:|
| Ít khiếu nại | 0,4 | 1 | 1 |
| Vừa | 0,4 | 2 | 2 |
| Nhiều | 0,2 | 3 | 3 |

Trung bình mỗi người dùng trợ lý: 0,4×1 + 0,4×2 + 0,2×3 = **1,8 phiên/tháng**;
0,4×1×1 + 0,4×2×2 + 0,2×3×3 = **3,8 lượt hỏi/tháng**. Share là tỷ trọng người,
không phải tỷ trọng phiên. Trung bình lượt hỏi/phiên theo lưu lượng là
3,8/1,8 ≈ 2,11; không dùng trung bình đơn giản của cột lượt hỏi.

| Kịch bản lưu lượng tự ước tính | Người dùng trợ lý | Phiên/tháng | Lượt hỏi/tháng |
|---|---:|---:|---:|
| Thấp | 5 | 9 | 19 |
| Cơ sở | 20 | 36 | 76 |
| Cao | 40 | 72 | 152 |

Ba mức người dùng lấy từ cột N của sensitivity cũ, giữ cùng cohort 100 khách
nền và cố định persona. Bảng lưu lượng chỉ thay N, còn sensitivity ở mục 3
thay cả N/F/C nên không đồng nhất hai bảng.

`answer()` hiện không lưu ngữ cảnh giữa lượt; mô phỏng nhiều lượt là nhiều
lần gọi độc lập, chưa chứng minh khách hoàn tất được hội thoại làm rõ. TV4 cần
giữ định nghĩa phiên, đo token/API theo từng persona và dùng tỷ lệ đạt Run-2
cùng model khi tính chi phí/task thành công. Không chuyển token thành phút
tiết kiệm; không dùng quy mô lớp Track A trong file ví dụ làm số người Track D.
