# Kết nối model cho Track D1

Bản CP3 dùng Chat Completions qua OpenRouter hoặc OpenAI bằng thư viện chuẩn Python. Lời gọi thực hiện trong `codebase/ai.py`. Công cụ tra đơn và chính sách chỉ đọc dữ liệu synthetic.

## 1. Cấu hình tại máy

Cấu hình CP3 cho Run-1 và Run-2:

```dotenv
MODEL_PROVIDER=openrouter
MODEL_NAME=baidu/ernie-5.5-flash-preview:free
API_KEY=
```

Điền key OpenRouter trong môi trường local hoặc `.env` được Git bỏ qua. Biến môi trường có sẵn được ưu tiên. Với OpenAI trực tiếp, đặt `MODEL_PROVIDER=openai`, `MODEL_NAME=gpt-4.1-mini` và dùng key OpenAI. Để thử offline, đặt `MODEL_PROVIDER=fake`.

OpenRouter nhận POST tại `https://openrouter.ai/api/v1/chat/completions`. Ngày 28/11/2026, hai bản Gemma miễn phí 31B và 26B đều chỉ liệt kê Google AI Studio. Trace cuối của cấu hình cũ ghi HTTP 429 ở ba ca, thiếu metadata để xác định nguồn giới hạn. Nhóm giữ ERNIE qua Baidu, endpoint công bố giá token bằng 0 và hỗ trợ structured outputs. [Endpoint](https://openrouter.ai/api/v1/models/baidu/ernie-5.5-flash-preview:free/endpoints).

Mỗi request chỉ định một model miễn phí, với ERNIE dùng `response_format=json_schema` (strict, đúng bốn khóa, enum riêng cho action và issue) và `require_parameters=true`. OpenRouter được phép chuyển upstream của chính model đó nếu có endpoint đủ điều kiện. Trần giá input, output và mỗi request đều bằng 0. Model suy luận dùng chung giới hạn 2.048 token cho reasoning và câu trả lời JSON.

## 2. Chạy và smoke test

Từ thư mục gốc, sau khi cấu hình key:

```bash
python3 eval/smoke_openrouter.py
```

D01 là probe đầu tiên. Nếu thành công, script kiểm tiếp D02 và D03, cách nhau 4 giây. Kiểm model, token vào/ra, món, số tiền và bước nhân viên duyệt. Khi lỗi, script dừng ngay và in chẩn đoán giới hạn đã lọc. Trường `raw` chỉ được tóm tắt theo loại lỗi. `retry_after` cho biết thời gian chờ nếu dịch vụ cung cấp; script không tự thử lại. Smoke này không ghi đè trace trước đó.

<a id="smoke-ernie"></a>

### Kết quả smoke live ERNIE · 28/11/2026

Theo kết quả nhóm ghi nhận khi chạy script, cả ba quyết định đều hợp JSON Schema, đúng món, đúng mức đề xuất và giữ quyền duyệt của nhân viên.

| Ca | Món | Đề xuất (VND) | Token vào | Token ra | Smoke |
|---|---|---:|---:|---:|---|
| D01 | cơm gà | 40.000 | 576 | 131 | PASS |
| D02 | trà | 20.000 | 575 | 166 | PASS |
| D03 | bún | 40.000 | 574 | 187 | PASS |
| **Tổng** | | | **1.725** | **484** | **3/3** |

Run-1 `run-1@20261128-092900` đã thực thi đủ 20 câu, 0 lỗi kỹ thuật. Sáu lần gọi ERNIE dùng tổng cộng 3.451 token vào và 1.009 token ra. Kết quả nghiệp vụ đã duyệt là 20/20. [Báo cáo Run-1](../eval/report.md).

- Demo: chạy `python3 run.py`, nhập `D100 thiếu cơm gà`.
- Đã lưu [CSV Run-1](../eval/run-1.csv) và [trace Run-1](../traces/run-1.jsonl). Dùng cùng provider và model ID cho Run-2.
- Smoke test lịch sử của TV2 trên OpenAI: 3 câu ngày 28/11/2026, snapshot `gpt-4.1-mini-2025-04-14`, 1.408 token vào và 70 token ra. Theo kết quả smoke D01, Liquid dùng 471/1.344 token và ERNIE dùng 476/656 token. Cả hai bị chặn; ERNIE trả cặp action/issue không hợp lệ trước khi thêm schema. Smoke mới in JSON quyết định đã lọc và lý do từ chối.

## 3. Contract và schema quyết định

- `agent.answer(text: str) -> {"output": str}`.
- `ai.call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}`,
  giữ `@model_call`; model lấy từ phản hồi API, token từ usage.
- `get_order(order_id)` và `get_policy()` giữ `@tool`, chỉ đọc
  `data/d1_orders.json`. Schema dataset được kiểm trước khi trả dữ liệu.

Model đọc nguyên khiếu nại, đơn và chính sách, trả JSON với đúng 4 khóa:

| action / issue | item / amount | Xử lý |
|---|---|---|
| propose / missing | Tên món đúng trong đơn / số nguyên bằng min(giá món, hạn mức) | Code kiểm lại rồi dựng bản nháp |
| ask / unclear | null / null | Hỏi lại một món thiếu hoặc phần mơ hồ |
| handoff / out_of_scope hoặc policy | null / null | Chuyển nhân viên |
| refuse / policy | null / null | Từ chối yêu cầu và chuyển nhân viên |

Không đưa lời tự do của model vào output. Quyết định model phải hợp schema,
đúng món và đúng tiền; action của model thực sự điều khiển nhánh trả lời.

## 4. Guardrails và lỗi

- Thiếu mã, nhiều mã, đơn không tồn tại: hỏi lại/kiểm mã, không đoán.
- Model phân biệt món thiếu với món đã nhận, phủ định, mâu thuẫn, nhiều món,
  món ngoài đơn và yêu cầu ngoài lát cắt.
- Có thông tin đã hoàn/giao bổ sung: chuyển nhân viên, tránh đề xuất lần nữa.
- Đòi tiền vượt giá món/hạn mức hoặc hoàn cả đơn: chuyển nhân viên;
  không thay bằng đề xuất bị cắt xuống hạn mức.
- Chặn một số mẫu prompt injection, yêu cầu dữ liệu cá nhân và dấu hiệu
  dị vật/ngộ độc/dị ứng; ca an toàn chuyển người ngay.
- JSON hỏng, sai schema/kiểu/món/tiền: chuyển người, ghi `guardrail` vào trace.
- Tool/API lỗi: thông báo an toàn qua exception, giữ lỗi ở evaluator/trace;
  không trả nháp thành công, không đổi sang fake hoặc token ước lượng.
  HTTP lỗi không ghi body/header/key vào log.

Các chặn theo câu chữ không bao phủ mọi cách diễn đạt. Dataset chỉ có 2 đơn,
4 món, không ảnh, số lượng món, xác thực chủ đơn hoặc lịch sử bồi thường thật.
Không tuyên bố an toàn tuyệt đối hoặc suy kết quả smoke test thành độ chính xác sản phẩm.

## 5. Tài liệu API

[OpenAI Chat Completions](https://developers.openai.com/api/reference/resources/chat),
[model GPT-4.1 mini](https://developers.openai.com/api/docs/models/gpt-4.1-mini).
