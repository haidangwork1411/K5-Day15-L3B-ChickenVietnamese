# ChickenVietnamese — Food Order Complaint Assistant

**L3B · Track D1 · CP3.** Khi khách báo thiếu một món, bản thử tra đơn và chính sách, sau đó đề xuất bước xử lý cho nhân viên duyệt. Đơn, giá và hạn mức đều giả lập. Xem [thành viên](TEAMS.md), [Canvas](canvas.md) và [thiết kế](spec.md).

## Nhóm làm gì, khung làm gì

Nhóm xây dựng workflow, công cụ tra cứu, guardrails, bằng chứng và benchmark. Khung BTC chạy ứng dụng, ghi trace, đo token, xuất lượt đánh giá và tính điểm từ cột `pass`.

## Chạy trong 3 phút

Từ thư mục có `run.py`, dùng Python 3.10+ và thư viện chuẩn. Thử offline trên Linux/macOS:

```bash
MODEL_PROVIDER=fake python3 run.py
```

Nhập `D100 thiếu cơm gà`. Giá món trong đơn là 50.000 VND, hạn mức là 40.000 VND. Output hợp lệ thể hiện đề xuất và người quyết định. CLI hiển thị model và token ngay dưới câu trả lời.

**Chạy OpenAI sau khi được phép sử dụng tài khoản và chi phí.** Trong Bash, các lệnh dưới đây giữ key ngoài lịch sử lệnh. Nếu đã cấu hình đủ ba biến trong `.env` cục bộ, có thể chạy thẳng lệnh Python. Biến môi trường hiện có được ưu tiên hơn `.env`.

```bash
export MODEL_PROVIDER=openai MODEL_NAME=gpt-4.1-mini
read -rsp 'OpenAI API key: ' API_KEY && printf '\n'
export API_KEY
python3 run.py
```

Trên Windows, dùng `.env.example` làm mẫu cho `.env` và chạy `py run.py`. [Cấu hình provider và smoke test của TV2](docs/connect-model.md).

## Lệnh

| Lệnh | Kết quả cần xem |
|---|---|
| `MODEL_PROVIDER=fake python3 -m unittest discover -s tests` | Kiểm thử offline cho quyết định, provider, tool và guardrail |
| `python3 evidence/verify.py` | Kiểm checksum snapshot, số đếm, provenance và phép tính impact |
| `python3 run.py check` | Kiểm benchmark, metric và format thành viên |
| `python3 run.py eval --try 3` | Với cấu hình thật, kiểm 3 ca đầu có model, token từ API và không có lỗi |
| `python3 run.py eval` | Chạy 20 câu bằng phiên bản đã duyệt, lưu CSV và trace được đánh số |
| `python3 run.py score eval/run-1.csv` | Sau khi chấm, in x/N tổng và theo loại câu. Ba metric được đếm theo tập áp dụng riêng trong hồ sơ đánh giá. |

## Bản chạy thử — viết ở đâu

`codebase/agent.py` định tuyến tình huống và kiểm quyết định. `codebase/tools.py` đọc đơn và chính sách. `codebase/ai.py` gọi OpenAI Chat Completions hoặc chạy fake, tùy cấu hình. Chi tiết tại [Spec §4](spec.md).

## Phần nào thật, phần nào giả

| Thành phần | Trạng thái |
|---|---|
| Quyết định trung tâm | Đã tích hợp OpenAI. TV2 ghi nhận smoke test trên phiên bản thành viên. Bản tích hợp đã kiểm offline, chưa có Run-1. |
| Dataset và giao dịch | Hai đơn, bốn món, một chính sách synthetic. Bản thử chỉ tạo đề xuất hoặc hướng dẫn liên hệ nhân viên. |
| Evidence | 150 trích đoạn review công khai. 18 đoạn phản ánh khó khăn hỗ trợ/hoàn tiền, 0 đoạn trực tiếp ghi nhận nhận thiếu món. |
| Benchmark | 20 câu, trong đó 7 câu truy được tới review gốc. Chưa có điểm chính thức hoặc kết quả chấm độc lập. |

## Dùng AI vào việc gì

Nhóm dùng AI để hỗ trợ lập trình, gắn nhãn review, soạn câu thử và kiểm tra tích hợp. Công cụ, phần việc của từng thành viên và giới hạn kiểm chứng được ghi trong [khai báo sử dụng AI](docs/ai-usage.md).

## File mẫu — điền ở bước nào

Bằng chứng và giới hạn chọn mẫu nằm trong [tổng hợp nghiên cứu](evidence/summary.md). [Data Card](data/DATA_CARD.md) mô tả dữ liệu chạy thử. [Hồ sơ đánh giá](eval/README.md) liên kết phương pháp chấm với [benchmark](eval/benchmark.csv) và [metric đã khóa](eval/metric_spec.yaml).

## Bảy hạng mục bắt buộc — nằm ở file nào

| Hạng mục | Hồ sơ |
|---|---|
| Bằng chứng pain | [Nghiên cứu](evidence/summary.md) |
| Impact | [Spec §2](spec.md), [nguồn giả định](evidence/impact.md) |
| Thiết kế | [Spec §4](spec.md) |
| Bản chạy thử | [Workflow](codebase/agent.py), lệnh demo ở trên |
| Bộ câu thử và metric | [Hồ sơ đánh giá](eval/README.md) |
| Chi phí | [Thư mục cost](cost/), thuộc CP4 |
| Slide và video | Video CP3 chưa quay. Slide demo thuộc CP4. |

**Video CP3 (30 giây).** 0–5 giây mở CLI ở chế độ OpenAI, 5–15 giây nhập `D100 thiếu cơm gà`, 15–25 giây cho thấy output thực tế, 25–30 giây chỉ vào model, token và bước nhân viên duyệt. Giữ key và nội dung `.env` ngoài khung hình.

**Nộp CP3.** Đội trưởng dùng mã ở dòng 1 của TEAMS, điền link repo/commit, Spec §0–§7, evidence, benchmark, video, run ID, x/N đã chấm và phần còn thiếu. Đặt video YouTube *Không công khai* hoặc Drive *Bất kỳ ai có đường liên kết* với quyền xem. Mở repo, các link bài và phát thử video trong cửa sổ ẩn danh trước khi nộp. [Các trường theo đề BTC](README-de-goc.md#checkpoint).
