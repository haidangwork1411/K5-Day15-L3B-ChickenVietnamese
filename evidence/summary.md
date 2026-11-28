# Tổng hợp Research, Evidence & Impact — TV3 / CP3

Ngày cập nhật: 28/11/2026. Baseline chính thức 58632f5f794120b4efbabaef75f480b3171edf7d;
nhánh local cp3/tv3-evidence. Chỉ sửa evidence/. Chưa stage, commit, push hay tạo PR.

## 1. Số chính và kết luận

Nguồn chính AP01 là **150 review App Store ShopeeFood VN**, mọi mức sao, từ các
trang được chọn trước; một trang rỗng, không có mẫu mới nhất liên tiếp hoàn chỉnh.
**18/150 (12.00%)** excerpt phản ánh khó/bất mãn hỗ trợ hoặc hoàn tiền;
**0/150 (0.00%)** excerpt nói trực tiếp nhận thiếu món; giao hai nhãn **0/150**.
Không suy tỷ lệ người dùng, số đơn hoặc phần trăm khách thiếu món từ các số này.

**Kết luận: cần kiểm thêm/đổi giả thuyết**, không tuyên bố pain thiếu món đã được
xác nhận. Dấu hiệu về hỗ trợ nói chung có thật trong nguồn công khai, nhưng không
đủ để nhận định nguyên nhân là khách không biết thông tin khiếu nại cần cung cấp.
0/150 không chứng minh không ai nhận thiếu món. [Hypothesis](hypothesis.md).

## 2. Nguồn, phương pháp và mức hoàn thành

| Hạng mục | Đã có | Giới hạn / chưa có |
|---|---|---|
| Đào review có cách chọn, mẫu số, số đếm và script | collection-plan, coding-protocol, CSV 150 dòng, count.py, counts.json | AI gắn nhãn excerpt; chưa có người thứ hai kiểm, gap trang 3 |
| ≥5 ví dụ có nguồn, bỏ tác giả | RV013/RV037/RV096/RV107/RV138/RV146/RV150 và các excerpt trong CSV | Tự báo cáo, chưa xác minh giao dịch hoặc vai người viết |
| Nguồn thứ hai kiểm bối cảnh | E01 báo chí; P01/E03 tài liệu chính thức đã đọc | Không độc lập xác nhận x/N, không thay thế phỏng vấn người đúng vai |
| Phỏng vấn ≥3 / khảo sát ≥20 | Không thực hiện, không bắt buộc nếu mining được chấp nhận | Không tạo file P1/P2/P3 hay response giả |
| Impact có nguồn từng thừa số | Truy vết mọi số CP2 về spec §2, có công thức/độ nhạy | N/F/C vẫn tự ước tính, không thể báo impact thực hoặc đủ trọn R2 |
| Bàn giao nguồn cho TV4 | 10 tình huống riêng trong source-cases.csv, có source/date/ref/scope/limits | Không phải 10 benchmark case đã duyệt; một số là boundary/nguồn chính sách |
| Cá nhân, làm theo cặp, review người thật | Chưa ghi nhận ngoài lời yêu cầu giao việc | Người học phải tự kiểm và nhóm thực hiện thật, AI không thay hoạt động này |

[data-mining.md](data-mining.md) có phương pháp, bảng số và ví dụ.
[sources.md](sources.md) phân biệt review/báo chí/chính sách/nguồn chưa truy cập.
[impact.md](impact.md) tách số quan sát và giả định.

## 3. Provenance cho TV4

[source-cases.csv](source-cases.csv): SC01–SC10 có Evidence ID, loại nguồn,
URL/ref, ngày, ngữ cảnh, diễn giải ẩn danh, mức xác minh và giới hạn. Bảy cơ chế
khác nhau có thể xem xét: thiếu chứng cứ, chứng cứ bị bỏ qua, chờ agent hỗ trợ,
quá hẹn phản hồi, trừ tiền nhưng không tạo đơn, sai thông tin liên hệ, yêu cầu
trả thêm ship; còn có ca không nhận đơn và bối cảnh an toàn/chính sách.
Không gọi các ca này đều là người dùng nhận thiếu món. TV4 cần duyệt, giữ ID
nguồn và chọn case phù hợp Spec; TV3 không viết input/expected hay sửa benchmark.
Không tuyên bố đã đạt ≥7/20 case nguồn thật trước khi TV4 chốt eligibility.

## 4. Những điểm phải báo leader trước khi tích hợp

- Mẫu chính chưa xác nhận trực tiếp pain hẹp; giữ lát cắt hay đổi cần leader quyết định.
- Impact 540 phút/tháng chỉ là kịch bản CP2 tự ước tính, không phải survey 100 khách.
- Baseline benchmark có 12 câu tự viết, chưa có nguồn thật được tích hợp; AI thật
  và mở rộng bộ thử là ownership TV2/TV4, không tự sửa trong nhánh TV3.
- Chưa có review theo cặp/người học kiểm độc lập. Không ghi đã diễn ra hoặc đủ mọi điểm R1/R2.
- Người học yêu cầu **không push**: tài liệu nhiệm vụ có bước commit/push/PR nhưng
  không thực hiện các bước này; để người học xem diff và tự stage/commit/push.

## 5. Kiểm tra lại

```powershell
py -3.12 evidence/count.py
py -3.12 evidence/verify.py
git diff --check
git status --short
```

Python 3.12.9 đã có; phần research và script chỉ dùng standard library nên không
cần pip install. Không cần API key/model để kiểm evidence. Không đọc/ghi .env.

## 6. AI log và quyền riêng tư

AI đọc tài liệu giao việc, guide/rubric/track và code để hiểu ngữ cảnh; thu RSS
công khai, gợi ý/rà nhãn trên 150 excerpt, viết script đếm, sổ nguồn và bảng impact.
Các dữ liệu nguồn có thật; **nhãn và phân tích có AI hỗ trợ, chưa phải người học
tự kiểm tay**. Không bịa phỏng vấn, người tham gia, giờ hẹn, số survey, hoạt động
cặp hoặc hiệu quả sản phẩm. Người học cần review diff và giải thích được kết quả.

Collector bỏ tác giả/title/raw payload, giữ tối đa một câu/25 từ gốc mỗi review;
RV113 không trích vì có thể nêu tên riêng. Không công bố dữ liệu đơn thật hoặc
email/điện thoại. Không có giấy phép mở cho cả kho; chỉ trích ngắn có nguồn để
phân tích, không tái phân phối nguyên nội dung. Chưa có người duyệt pháp lý/quyền
tái sử dụng toàn bộ; không nhận đã được cấp quyền đó.

Lỗi môi trường đã xử lý: Python Windows không có tzdata; collector dùng timezone
UTC+7 chuẩn, không tạo dependency mới. Network đọc nguồn và ghi evidence ở repo
Day15 dùng quyền giới hạn đúng thao tác; không thay đổi cấu hình hệ thống.
