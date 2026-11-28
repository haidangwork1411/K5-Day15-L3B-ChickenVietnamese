# Bằng chứng bổ sung và impact CP4

Ngày truy cập nguồn: 28/11/2026. Phần TV3 bổ sung sáu nguồn công khai, rà soát
nhãn và chuẩn bị đầu vào quy mô cho TV4. Nguồn bổ sung cho thấy có phản ánh trực
tiếp về thiếu món và khó xử lý bồi hoàn trong bối cảnh Singapore, cùng xác nhận
về nhóm sai/thiếu món từ nền tảng. Chưa đủ căn cứ đo tần suất tại Việt Nam hoặc
kết luận nguyên nhân là khách không biết cung cấp đúng tên món.

## Snapshot CP3

Giữ nguyên 150 review AP01, nhãn, quy tắc đếm và ledger nguồn CP3:
18/150 đoạn phản ánh khó hỗ trợ/hoàn tiền, 0/150 trực tiếp nêu thiếu món và
0/150 có cả hai nhãn. **12% không phải tỷ lệ thiếu món.**
[Manifest SHA-256](cp3-snapshot.json) khóa mười file tại baseline `c9246a2`.
Chuẩn hóa CRLF thành LF trước khi băm, giữ BOM, khoảng trắng và thứ tự dòng.
Không cộng các nguồn CP4 vào mẫu số 150.

## Phương pháp và nguồn bổ sung

Đợt này dùng tìm kiếm có chủ đích để tìm tình huống thiếu món, không phải mẫu
ngẫu nhiên hay một đợt đo prevalence. [Ledger](supplemental-sources.json) lưu
query, quy tắc tuyển, URL, vị trí đoạn trích, ngày truy cập, ngày xuất bản khi
trang hiển thị, nguyên văn ngắn và hash của đoạn trích. Một bài gốc là một đơn
vị; không lấy bình luận hoặc tách nhiều sự cố trong một bài thành nhiều mẫu.
Giữ cả ca đã được giao bổ sung. Không dùng trang không mở được làm bằng chứng.

| ID | Nguồn đã đọc | Điều quan sát được | Phạm vi sử dụng |
|---|---|---|---|
| CP4P01 | [Grab ngày 14/08/2026](https://www.grab.com/inside-grab/stories/how-we-taught-llms-to-solve-the-missing-muffins-mystery/) | Doanh nghiệp báo nhóm thiếu/sai món thường dẫn đến yêu cầu hỗ trợ, có thiếu thành phần và số lượng | Xác nhận bối cảnh khu vực; không suy tỷ lệ Việt Nam hoặc hiệu quả prototype |
| CP4P02 | [Đào tạo ShopeeFood](https://merchant.shopeefood.vn/edu/article/chien-luoc-van-hanh-nhom-mon-an-hieu-qua-tu-goc-nhin-danh-gia-cua-khach-hang) | Nêu sai/thiếu món trong nhóm khách muốn quán cải thiện | Bối cảnh Việt Nam; số 31.2% gộp hai loại, thiếu N và kỳ đo trong văn bản nên không đưa vào impact |
| CP4R01 | [Bài gốc về voucher](https://www.reddit.com/r/singapore/comments/1e4euuk/grab_greed_is_taking_it_too_far/) | Tự báo thiếu một món và bất mãn với voucher bồi hoàn | Cơ chế khó khăn về phương án bồi hoàn, không phải chính sách được xác nhận |
| CP4R02 | [Bài gốc hỏi cách liên hệ hỗ trợ](https://www.reddit.com/r/askSingapore/comments/1js3e9a/how_to_contact_grabfood_support/) | Tự báo thiếu phần món trong combo, không hài lòng voucher và khó tìm liên hệ | Không biết giá riêng phần combo; không suy khách cung cấp thiếu thông tin |
| CP4R03 | [Bài gốc đã được giao bổ sung](https://www.reddit.com/r/askSingapore/comments/1r8rozd/grab_delivery_guy_missed_out_several_items_i/) | Thiếu nhiều món rồi được giao bổ sung và đã nhận hoàn | Ca ranh giới cần xác minh trạng thái, tránh bồi thường lặp |
| CP4R04 | [Bài gốc về từ chối hoàn](https://www.reddit.com/r/singapore/comments/1b6avab/increase_in_grabfood_service_failures_but/) | Tự báo sự cố ngày 16/02/2024 đặt hai cốc nhưng nhận một; bài còn kể các sự cố sai món riêng | Không gộp sai món vào thiếu món; ngày sự cố là lời tự báo cáo |

Mẫu bổ sung có **4 bài gốc**, trong đó 4/4 nói trực tiếp thiếu món và 3/4 phản
ánh khó khăn hỗ trợ/bồi hoàn; hai bài của nền tảng không nằm trong mẫu số này.
Đây là kết quả tuyển bài theo vấn đề đã tìm, không chứng minh độ phổ biến.
Các bài Reddit đều ở diễn đàn Singapore; vai người viết, nơi cư trú và giao
dịch chưa được xác minh. Không gán ngày tuyệt đối từ nhãn tương đối của trang.
Chỉ lưu trích ngắn, bỏ tác giả/tài khoản, không lưu raw payload hay hồ sơ đơn.

## Rà soát nhãn

[Audit nhãn](label-audit.json) ghi rõ người rà là AI: đã xem 150 dòng,
đánh giá được 149 đoạn trích; RV113 bị ẩn nên không đủ nội dung đánh giá.
Ba dòng chờ con người phân xử là RV011, RV119 và RV149. Hai dòng đầu có lời chê
hỗ trợ chung cần đối chiếu quy tắc yêu cầu cơ chế; dòng cuối có từ chối hoàn
nhưng là deal không phải món ăn. Các đề xuất trong audit không thay nhãn gốc.

Số dòng kiểm tay có log xác nhận là **0**; tổng số thực tế chưa xác định.
Không gọi lượt AI rà là kiểm tay, kiểm độc lập hoặc độ chính xác nhãn.

## Bàn giao quy mô cho TV4

[cost-handoff.json](cost-handoff.json) là đầu vào đề xuất, chưa áp dụng vào
`cost/personas.yaml`. Tất cả số quy mô/persona là **tự ước tính**. Với 100 khách
nền, giả định mọi khách gặp sự cố đều dùng trợ lý; ba kịch bản có 5/20/40 người
dùng trợ lý, cùng tần suất trung bình 1,8 phiên/người/tháng. Lưu lượng tương
ứng 9/36/72 phiên và 19/76/152 lượt hỏi mỗi tháng.

Trong cơ sở: 20 người × 1,8 phiên × 15 phút = 540 phút tổn thất giả định;
27 phút/người gặp sự cố và 5,4 phút/khách nền. Chưa có phép đo tiết kiệm.
[Impact](../impact.md) giải thích công thức, các mẫu số và sensitivity riêng.
TV4 cần rà lại giả định, cấu hình persona và mô phỏng bằng token từ API;
không dùng quy mô Track A đang có trong file ví dụ cho sản phẩm Track D.

## Kiểm tra và việc cần người thực hiện

Chạy từ root repo:

```powershell
python3 evidence/verify.py
python3 -m unittest discover -s evidence -p "test_*.py" -v
git diff --check
```

Verifier kiểm nội dung cục bộ, hash, số đếm, mẫu số và phép tính; không xác nhận
giao dịch, tính đúng của lời kể hoặc danh tính người kiểm tay.
[Sổ hoạt động](research-activity.md) phân biệt thay đổi có trong Git với nghiên
cứu cá nhân, làm theo cặp, review nhóm và bonus cần ghi nhận từ người thật.
TV1 cần tích hợp phần thích hợp vào Spec/slide; TV4 phụ trách cost và đánh giá.
Nhánh này chỉ cập nhật `evidence/`.
