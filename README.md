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

**Chạy OpenRouter với model miễn phí cố định cho Run-1 và Run-2.** Trong Bash, các lệnh dưới đây giữ key ngoài lịch sử lệnh. Nếu đã cấu hình đủ ba biến trong `.env` cục bộ, có thể chạy thẳng lệnh Python. Biến môi trường hiện có được ưu tiên hơn `.env`.

```bash
export MODEL_PROVIDER=openrouter MODEL_NAME=baidu/ernie-5.5-flash-preview:free
read -rsp 'OpenRouter API key: ' API_KEY && printf '\n'
export API_KEY
python3 run.py
```

Trên Windows, dùng `.env.example` làm mẫu cho `.env` và chạy `py run.py`. [Cấu hình OpenRouter, OpenAI và lịch sử smoke test](docs/connect-model.md).

## Lệnh

| Lệnh | Kết quả cần xem |
|---|---|
| `MODEL_PROVIDER=fake python3 -m unittest discover -s tests` | Kiểm thử offline cho quyết định, provider, tool và guardrail |
| `python3 evidence/verify.py` | Kiểm checksum snapshot, số đếm, provenance và phép tính impact |
| `python3 run.py check` | Kiểm benchmark, metric và format thành viên |
| `python3 eval/smoke_openrouter.py` | Kiểm D01–D03 với model miễn phí đã chọn, token từ API và đề xuất thực tế. Dừng ở lỗi đầu tiên. |
| `python3 run.py eval` | Chạy 20 câu bằng phiên bản đã duyệt, lưu CSV và trace được đánh số |
| `python3 run.py score eval/run-1.csv` | Sau khi chấm, in x/N tổng và theo loại câu. Ba metric được đếm theo tập áp dụng riêng trong hồ sơ đánh giá. |

## Bản chạy thử — viết ở đâu

`codebase/agent.py` định tuyến tình huống và kiểm quyết định. `codebase/tools.py` đọc đơn và chính sách. `codebase/ai.py` gọi Chat Completions qua OpenRouter hoặc OpenAI, hoặc chạy fake, tùy cấu hình. Chi tiết tại [Spec §4](spec.md).

## Phần nào thật, phần nào giả

| Thành phần | Trạng thái |
|---|---|
| Quyết định trung tâm | ERNIE qua OpenRouter đã đạt 3/3 câu smoke D01–D03 với JSON Schema, đúng món, số tiền và bước nhân viên duyệt. [Smoke từng câu](docs/connect-model.md#smoke-ernie). Run-1 `run-1@20261128-092900` đã thực thi 20/20 câu, 0 lỗi kỹ thuật. [CSV, trace và số liệu](eval/report.md). |
| Dataset và giao dịch | Hai đơn, bốn món, một chính sách synthetic. Bản thử chỉ tạo đề xuất hoặc hướng dẫn liên hệ nhân viên. |
| Evidence | 150 trích đoạn review công khai. 18 đoạn phản ánh khó khăn hỗ trợ/hoàn tiền, 0 đoạn đề cập trực tiếp việc giao thiếu món. |
| Benchmark | 20 câu, trong đó 7 câu truy được tới review gốc. Run-1 đạt 20/20 câu. Hai người chấm đồng thuận ở 5/5 câu đã chọn. [Kết quả chấm](eval/README.md#3-metric-và-cách-chấm). |

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
| Chi phí | [Thư mục cost](cost/), đã có mô phỏng 50 phiên |
| Slide và video | [Xem video demo AI thật](https://drive.google.com/file/d/1y7jnc8wYgmPQqtxI2iZpvszd4KbUMLkN/view?usp=sharing) (MP4, 29,89 giây). Nhóm đã kiểm tra quyền xem bằng cửa sổ ẩn danh. [Slide CP4](demo-slides.pdf). |

Trong video, khách báo `D100 thiếu cơm gà`. Bản thử hiển thị giá món 50.000 VND, đề xuất tối đa 40.000 VND và nêu rõ nhân viên xác minh, quyết định. CLI hiển thị model ERNIE và số token thực tế.

**Giới hạn hồ sơ CP3.** Impact dựa trên giả định cho 100 khách. Hồ sơ chưa ghi nhận câu hỏi nghiên cứu riêng của từng thành viên, hoạt động theo cặp qua các chặng, buổi rà soát nhóm 15 phút hoặc số dòng review đã được kiểm nhãn thủ công. [Nguồn và phạm vi kiểm chứng](evidence/summary.md).

**Hồ sơ CP4.** [PDF 8 trang](demo-slides.pdf), [kịch bản demo và phân vai](slides/outline.md), [báo cáo đánh giá](eval/report.md) và [chi phí](cost/cost-estimate.md).

Run-1 và Run-2 đều đạt 20/20. Hướng dẫn D06/D07 đạt đủ hai tiêu chí UX 0/2 → 2/2; 18 output giữ nguyên. Simulation 50 phiên, seed 42, 89 lượt hỏi, 0 lỗi. Chi phí/task giả định $0.00023 hoặc $0.0013 theo hai tầng giá Gemini áp trên token ERNIE. Đề xuất ITERATE vì lợi ích với người dùng và chi phí vận hành đầy đủ chưa đo.

**Bổ sung sau CP4.** Nhóm đã demo trực tiếp. [UI localhost](demo_ui/README.md) dùng cùng prototype và có Mock Mode để thử offline; live D100 bị chặn bởi quota OpenRouter, chưa có kết quả end-to-end thành công qua UI. Lịch sử trình duyệt chỉ để hiển thị, không phải memory. Baseline CP4 giữ nguyên.
