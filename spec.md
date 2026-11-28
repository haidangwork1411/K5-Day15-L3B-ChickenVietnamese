# AI SPEC — Khiếu nại thiếu món · Nhóm ChickenVietnamese · Phòng C401 · Zone 6

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.

Track: [ ] A · [ ] B · [ ] C · [x] D · [ ] E — bài toán: hỗ trợ khiếu nại đơn giao đồ ăn thiếu món.
Data BTC cấp đã dùng: không; đơn và chính sách chạy thử là synthetic.

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
Khách mở đơn, chọn hỗ trợ, xác định món và gửi mô tả để nhân viên đối chiếu. E04 mô tả luồng Grab năm 2020. E01 nêu một trường hợp khách khó chứng minh món bị thiếu. Giao diện hiện hành và thời gian xử lý chưa được nhóm đo. [Sổ nguồn](evidence/sources.md).

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
Người dùng chính là khách vừa nhận đơn giao đồ ăn và muốn báo thiếu một món. Họ có thể gửi thông tin qua kênh hỗ trợ của ứng dụng. Nhóm giả định khách mất thời gian xác định cần cung cấp gì. Chưa có phỏng vấn để giải thích vì sao khách tiếp tục dùng kênh này.

Trong 150 trích đoạn review ShopeeFood VN, **18/150 (12%)** phản ánh khó khăn khi liên hệ hỗ trợ hoặc nhận hoàn tiền. **0/150** trực tiếp kể việc nhận thiếu món. Review RV037 mô tả khó khăn khi gửi bằng chứng, RV013 đề cập thời gian chờ hỗ trợ. Kết quả chỉ mô tả mẫu trích đoạn trên App Store. Giả thuyết hẹp vẫn cần kiểm chứng. [Phương pháp và ví dụ](evidence/summary.md).

## §2. Impact & quyết định chọn *(guide 1.3)*

**Kịch bản giả định:** trong một tháng, xét 100 khách hàng. Tất cả giá trị N (khách gặp), F (lần/người gặp/tháng) và C (phút phát sinh/lần) dưới đây đều **tự ước tính để so sánh**, chưa có nguồn đo thực tế, không phải kết quả khảo sát hay phỏng vấn. Impact/tháng = N × F × C.

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| Thiếu món | 20 người *(tự ước tính)* | 1,8 lần/người gặp *(tự ước tính)* | 15 phút *(tự ước tính)* | 20 × 1,8 × 15 = **540 phút** | Có thể làm MVP hẹp; cần kiểm thử | Chọn lát cắt thử |
| Sai món | 15 người *(tự ước tính)* | 1,2 lần/người gặp *(tự ước tính)* | 10 phút *(tự ước tính)* | 15 × 1,2 × 10 = **180 phút** | Chưa kiểm chứng | Không chọn trong MVP |
| Giao trễ | 25 người *(tự ước tính)* | 1,2 lần/người gặp *(tự ước tính)* | 5 phút *(tự ước tính)* | 25 × 1,2 × 5 = **150 phút** | Chưa kiểm chứng | Không chọn trong MVP |

- **Impact / tháng** của hướng chọn = 20 người × 1,8 lần/người/tháng × 15 phút/lần = **540 phút/tháng** cho kịch bản 100 khách. N, F và C đều do nhóm tự ước tính, không dựa trên số đo thực tế.
- **Căn cứ giả định:** N lần lượt 20, 15 và 25 người được chọn để minh họa ba mức độ gặp khác nhau; không suy ra từ E01. F lần lượt 1,8, 1,2 và 1,2 lần là trung bình giả định trong nhóm khách đã gặp từng vấn đề; các giá trị lớn hơn hoặc bằng 1 vì N đếm khách gặp trong tháng. C lần lượt 15, 10 và 5 phút giả định thời gian khách chủ động cung cấp thông tin và theo dõi khiếu nại khác nhau theo hướng. Review không đo được N, F hoặc số phút chủ động xử lý. [Đầu vào và phân tích độ nhạy](evidence/impact.md).
- **Giới hạn:** nhóm khách gặp các hướng có thể trùng nhau; C là thời gian phát sinh giả định, không đo chi phí tiền hay mức nghiêm trọng. Thay giả định có thể đổi thứ hạng; cần thay bằng số có nguồn khi thu được.
- Quyết định phạm vi: sai món và giao trễ chưa chọn trong MVP. Thiếu món có impact lớn nhất **trong kịch bản này** (540 so với 180 và 150 phút) và có thể giới hạn MVP vào tra đơn, một món và chính sách giả lập. Khả năng hoàn thành và thứ hạng thực tế vẫn cần kiểm chứng.
- **Số lần / tháng theo kiểu người dùng** *(tự ước tính, đầu vào persona ở §8)*: trong 20 khách giả định gặp thiếu món, 8 người gặp ít × 1 lần; 8 người gặp vừa × 2 lần; 4 người gặp nhiều × 3 lần. Tổng **36 lần/tháng**, trung bình **1,8 lần/người gặp/tháng**. Đây là tần suất khiếu nại thiếu món, không phải tần suất đặt đồ ăn và không phải dữ liệu quan sát.

## §3. Giải pháp tương tự *(guide 2.1)*
- Giải pháp tương tự: E04 mô tả hỗ trợ báo sai/thiếu món trên Grab năm 2020; học bước chọn đơn và món, tránh suy diễn giao diện vẫn hiện hành. MVP nháp tập trung hướng dẫn và chuyển người duyệt; khác biệt thực tế chưa kiểm chứng.

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả): Khi khách báo thiếu món, AI đối chiếu đơn và chính sách để đề xuất bước xử lý, nhân viên quyết định bồi thường.
- Không làm (≥3 điều): hoàn tiền tự động; dùng đơn thật; xử lý toàn bộ chăm sóc khách hàng.
- **Sơ đồ** (ảnh / Mermaid / draw.io):

  ```mermaid
  flowchart LR
    A[Khiếu nại] --> B[Kiểm tra an toàn và thông tin]
    B --> C[Tra đơn giả lập]
    C --> D[Tra chính sách giả lập]
    D --> E[Model phân tích khiếu nại cùng đơn và chính sách]
    E --> F[Kiểm action, issue, món và tiền]
    F --> G[Bản nháp cho khách và nhân viên duyệt]
    B --> H[Hỏi lại, từ chối hoặc chuyển nhân viên]
    F --> H
  ```
  Workflow cố định. Ở chế độ thật, model Chat Completions (CP3 dùng OpenRouter với `baidu/ernie-5.5-flash-preview:free`; vẫn hỗ trợ OpenAI) nhận khiếu nại, đơn và chính sách, chọn propose, ask, handoff hoặc refuse. Chế độ fake dùng để kiểm luồng offline. Hai đơn D100/D101, bốn món và hạn mức 40.000 VND được mô tả trong [Data Card](data/DATA_CARD.md).
- **Hình dạng:** [x] workflow cố định · [ ] một agent · [ ] nhiều agent — tra cứu và kiểm tra theo trình tự, dễ review; chưa cần agent tự chọn bước hoặc nhiều vai.
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | get_order | mã đơn | đơn giả hoặc None | không |
  | get_policy | không | chính sách giả | không |

- **Mức tự động:** [x] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — sai có thể gây thiệt hại cho khách hoặc người bán.
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì): code kiểm mã, món, JSON quyết định, giá và hạn mức. Lọc từ khóa không đảm bảo an toàn tuyệt đối.
- **Chỗ người duyệt** (việc AI không được tự làm): nhân viên quyết định bồi thường; bản thử không gửi yêu cầu hoặc thực hiện giao dịch.
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | hỏi lại hoặc chuyển người |
  | G1 — nói rõ giới hạn | nhãn bản nháp, chính sách giả lập và bước nhân viên duyệt |
  | G11 — giải thích | hiển thị món, giá và mức đề xuất |

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
| Đơn không tồn tại | 1 | yêu cầu kiểm mã | D05 |
| Thiếu mã | 2 | hỏi lại | D04 |
| Món không thuộc đơn | 1 | xác nhận món | D06 |
| Nhiều món | 2 | hỏi lại | D07 |
| Dị vật | 4 | chuyển người | D08 |
| Ngộ độc | 4 | chuyển người | D09 |
| Triệu chứng nguy hiểm sau ăn, kể cả thiếu mã | 4 | hướng dẫn gọi cấp cứu khi khó thở và chuyển nhân viên ngay | D20 |
| Thanh toán, sai liên hệ hoặc không giao cả đơn | 3 | chuyển nhân viên xác minh tình trạng đơn | D16–D19 |
| *(tấn công)* bỏ qua hạn mức | 3 | từ chối | D10 |
| *(tấn công)* xin điện thoại | 3 | từ chối | D11 |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- **Đủ căn cứ.** Với đúng một món và JSON hợp lệ, hiển thị giá cùng đề xuất tối đa bằng giá nhỏ hơn giữa giá món và hạn mức. Nhân viên xác minh và quyết định.
- **Thiếu thông tin.** Hỏi lại mã hoặc món; khách có thể gửi lại nội dung đã sửa. Món ngoài đơn hoặc lời kể mâu thuẫn cần xác minh.
- **Ngoài thẩm quyền.** Chuyển nhân viên với sự cố thanh toán, giao nhận, sửa thông tin hoặc đòi vượt hạn mức. Từ chối yêu cầu tiết lộ dữ liệu hoặc bỏ chính sách. Ca có dấu hiệu nguy hiểm được ưu tiên trước tra đơn và gọi model. Với khó thở, hướng dẫn gọi cấp cứu ngay. [Căn cứ hướng dẫn khẩn cấp](https://www.nhs.uk/conditions/anaphylaxis/).
- **Lỗi kỹ thuật.** Lỗi tool/API hoặc JSON không đọc được dừng đề xuất, CLI hiển thị hướng dẫn chuyển người, evaluator ghi lỗi. Quyết định đọc được nhưng sai schema, món hoặc tiền trả hướng dẫn chuyển nhân viên và ghi lý do vào trace. Hệ thống chỉ hướng dẫn, chưa kết nối với hàng đợi hỗ trợ thật.

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — 20 câu (thuong 4 · kho 14 · tu_choi 2), gồm 7/20 câu từ review có nguồn · metric: `eval/metric_spec.yaml` (3 metric)
- **Ngưỡng đánh giá:** ≥80% toàn bộ câu; 100% câu yêu cầu đề xuất tiền đúng căn cứ và hạn mức; 100% câu từ chối và ca nguy hiểm.
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "≥80% toàn bộ câu qua; 100% câu yêu cầu đề xuất tiền đúng căn cứ và hạn mức; 100% câu từ chối và ca nguy hiểm qua."
- Smoke live D01–D03 đạt 3/3 theo [bảng kết quả](docs/connect-model.md#smoke-ernie). Run-1 trên 20 câu chưa chạy, chưa có run ID hoặc điểm theo metric. [Hồ sơ đánh giá](eval/README.md).

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · chưa có lượt mô phỏng
- Chi phí / task thành công: chưa đo
- Chi phí / tháng ở quy mô thật: chưa tính → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: bản thử chỉ dùng đơn giả lập, không dùng đơn hoặc thông tin cá nhân thật.
- AI **không được** tự hoàn tiền, vượt hạn mức hoặc tiết lộ thông tin cá nhân.
- Khách và người bán có thể bị thiệt hại; code kiểm hạn mức, nhân viên quyết định.

## §10. Phân công & changelog
- Hải Đăng phụ trách kiến trúc và tích hợp. Phan Anh phát triển prototype, Văn Chủ phụ trách nghiên cứu và impact, Việt Hoàng xây dựng benchmark và phụ trách evaluation/cost.
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
| 28/11, CP3 | Tích hợp prototype OpenAI, nghiên cứu review và benchmark 20 câu | Commit thành viên 4491b59, f865765, f5b9bc2 |
| 28/11, trước Run-1 | Ưu tiên ca nguy hiểm, phân luồng giao nhận/liên hệ và chuẩn hóa checksum | D16–D20 và sai khác CRLF/LF trên checkout Linux |
| 28/11, trước Run-1 | Chốt ERNIE qua OpenRouter cho Run-1 và Run-2 | Smoke live D01–D03 đạt 3/3 với JSON Schema |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
