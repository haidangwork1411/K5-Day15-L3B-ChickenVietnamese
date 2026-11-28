# Nguồn và provenance — TV3

Ngày kiểm: 28/11/2026. URL công khai không đồng nghĩa giấy phép mở. Chỉ trích
ngắn, ghi nguồn; không tái phân phối nguyên bài/RSS hay tên tài khoản. Các excerpt
review tối đa một câu/25 từ; sổ nguồn này không phải chính sách prototype.

| Evidence ID | Loại / nguồn | Mức xác minh và được dùng làm gì | Giới hạn |
|---|---|---|---|
| AP01 / RV001–RV150 | [App Store ShopeeFood VN](https://apps.apple.com/vn/app/shopeefood-food-delivery/id1137866760?platform=iphone&see-all=reviews); URL từng trang tại public-reviews/collection.json | Feed được tải trực tiếp; ID/ngày/hash từng review trong CSV. Dùng mô tả mẫu và tình huống nguồn | Tự báo cáo, đoạn trích, chưa xác minh giao dịch/vai, gap trang 3; không dùng làm prevalence |
| E01 | [CafeF 05/03/2026](https://cafef.vn/tu-nay-dat-mon-tren-app-nho-lam-viec-nay-de-duoc-den-tien-khi-do-an-bi-do-hoac-thieu-mon-188260305185811121.chn) | Đã đọc. Bài mô tả một khách thiếu món khó khiếu nại và gợi ý giữ chứng cứ | Báo chí thứ cấp, không có mẫu số; lời tác giả không phải phỏng vấn của nhóm |
| E02 | [Trợ giúp Shopee](https://help.shopee.vn/portal/4/article/79520) | Công cụ không truy cập được ngày kiểm; không dùng nội dung | Không suy chính sách từ tiêu đề/URL |
| E03 | [Grab merchant terms VN](https://www.grab.com/vn/terms-policies/merchant-terms-and-conditions/) §8.12; trang ghi cập nhật 01/07/2026 | Đã đọc: Grab xem xét/xác minh yêu cầu hoàn; phạm vi có thiếu món và vấn đề an toàn | Điều khoản cho thương nhân, không phải bằng chứng người dùng gặp pain; không hứa mức hoàn/hạn mức cho prototype |
| E04 | [24h 18/06/2020](https://www.24h.com.vn/cong-nghe-thong-tin/cach-lay-lai-tien-khi-shipper-giao-thieu-do-an-dat-qua-grabfood-c55a1158472.html) | CP2 từng ghi nguồn lịch sử; lần này timeout, không tái xác minh nội dung | Không dùng làm quy trình UI hiện hành hoặc quote mới |
| P01 | [ShopeeFood Merchant](https://resource.foody.vn/web/merchant-private-policy.html) §5.3 | Đã đọc: cần chứng cứ hai bên; phần này có thiếu/sai món và an toàn thực phẩm | Điều khoản thương nhân; trang không có ngày cập nhật rõ. Mốc 48h là gửi chứng cứ của người bán, không phải lời hứa hoàn tiền cho khách trong 48h |

Không dùng các trang tổng hợp phân tích review làm nguồn số đếm; không dùng
Google snippet như đã đọc toàn bài. Không lấy chính sách có thật để sửa hạn mức
giả lập của spec. Nguyên văn E01 không chép lại; chỉ diễn giải ngắn và dẫn nguồn.

## Bàn giao cho TV4 ngay trong ledger

[source-cases.csv](source-cases.csv) chứa nguồn, ngày, ngữ cảnh, diễn giải ẩn danh,
mức xác minh và giới hạn cho từng tình huống. Đây là đầu vào để TV4 chọn case,
không phải benchmark, input giả hay expected. Phải giữ ID nguồn trong case viết lại.
Không chuyển tên/số đơn/thông tin riêng tư từ review vào prototype.

Các case review không tự chứng minh nhận thiếu món; cột scope phân biệt ca trong
lát cắt, ca cần xác minh và ca ngoài phạm vi dùng thử boundary/escalation. Các ca
chính sách là tình huống được văn bản mô tả, không phải sự kiện người dùng đã quan sát.
TV4 phải xác nhận tính đủ khác bản chất và source eligibility trước khi chốt ít
nhất 7/20 case thật; không chia một chuyện thành nhiều case để đủ tỷ lệ.

## Nguồn bổ sung CP4

[Ledger CP4](cp4/supplemental-sources.json) lưu riêng sáu nguồn đã đọc ngày
28/11/2026, vị trí đoạn trích, ngày xuất bản khi hiển thị và hash excerpt.
[Phương pháp và bảng nguồn](cp4/README.md) phân biệt hai báo cáo nền tảng
CP4P01–CP4P02 với bốn bài gốc CP4R01–CP4R04 ở bối cảnh Singapore.
Chỉ bài gốc nằm trong mẫu số bốn; không cộng vào AP01 hoặc ledger benchmark.
Các trang không truy cập được được ghi riêng, không suy nội dung từ snippet.

Nguồn mới hỗ trợ nhận định có phản ánh trực tiếp thiếu món và khó bồi hoàn;
không chứng minh tỷ lệ tại Việt Nam, nguyên nhân khách thiếu thông tin hoặc
hiệu quả của trợ lý. Những số quy mô và persona trong [bàn giao TV4](cp4/cost-handoff.json)
là tự ước tính, không trích ra từ báo cáo nền tảng hoặc lịch sử người đăng.
