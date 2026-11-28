# Nối OpenAI — phần TV2 / Phan Anh

Bản CP3 triển khai OpenAI Chat Completions bằng thư viện chuẩn Python, không cần
SDK hoặc cài thêm package. Đơn và chính sách là synthetic; kết quả là bản nháp,
nhân viên xác minh và quyết định. Không có giao dịch thật.

## 1. Cấu hình tại máy

Nếu chưa có `.env`, chép từ `.env.example`. Nếu đã có thì sửa file đang có để
giữ cấu hình/key. Điền ba biến:

```dotenv
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4.1-mini
API_KEY=
```

Điền API_KEY trực tiếp tại máy. Không đưa key vào Git, lệnh có thể bị ghi log,
ảnh chụp, commit hoặc PR. `.env` đã có trong `.gitignore`.
Provider/model này đã được người phụ trách cho phép dùng trong phiên làm việc.
Nếu đổi model hoặc tài khoản thì xác nhận quyền truy cập/chi phí với nhóm trước.

Mặc định chưa cấu hình provider sẽ dùng `fake`, model=fake, token=0;
chỉ để kiểm luồng offline, không tính là AI thật. Bản này hỗ trợ `openai` và `fake`.

## 2. Chạy và smoke test

```powershell
python run.py
# Thử: D100 thiếu trà
python run.py eval --try
python -X utf8 -m unittest discover -s tests -v
```

Smoke test dùng **benchmark CP2 đang có**, không tạo lượt đánh giá chính thức.
`eval/run-try.csv` và `traces/run-try.jsonl` là file thử tại máy đã được Git bỏ qua;
không commit, không gọi chúng là run-1.

Đã chạy 3 câu ngày 28/11/2026: API trả
`gpt-4.1-mini-2025-04-14`, tổng **1408 token vào / 70 token ra**, không lỗi.
Token đọc trực tiếp từ `usage.prompt_tokens` và `usage.completion_tokens`,
không ước lượng. Bộ unit test có **25 test** kiểm hợp đồng/guardrail, không gọi mạng.

Lượt đánh giá đầy đủ, chấm điểm, benchmark mở rộng và mô phỏng chi phí do người
phụ trách tương ứng chạy sau khi leader tích hợp. TV2 không tạo/sửa run-1 chính thức.

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
