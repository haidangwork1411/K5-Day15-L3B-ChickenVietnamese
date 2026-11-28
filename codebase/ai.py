"""Nối OpenAI — chỗ duy nhất trong bản chạy thử gọi model AI, giữ @model_call.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả quyết định mock đơn giản, model "fake", token 0 — chỉ để kiểm luồng offline.
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env theo .env.example, MODEL_PROVIDER=openai, MODEL_NAME và
API_KEY. Bản CP3 dùng Chat Completions JSON mode, lấy token trực tiếp từ usage.
Không dán API key vào file này hoặc ghi request header/body lỗi vào log.
"""
import os
import json
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        # Chỉ kiểm luồng offline, không được tính là lượt AI thật.
        try:
            data = json.loads(user)
        except json.JSONDecodeError:
            return {'text': '[mock] Chưa gọi AI thật.', 'model': 'fake', 'tokens_in': 0, 'tokens_out': 0}
        if not isinstance(data, dict) or not {'complaint', 'order', 'policy'} <= set(data):
            return {'text': '[mock] Chưa gọi AI thật.', 'model': 'fake', 'tokens_in': 0, 'tokens_out': 0}
        complaint = data['complaint'].casefold()
        items = [item for item in data['order']['items'] if item['name'].casefold() in complaint]
        decision = {'action': 'ask', 'item': None, 'amount': None, 'issue': 'unclear'}
        if len(items) == 1 and 'thiếu' in complaint:
            item = items[0]
            decision = {'action': 'propose', 'item': item['name'],
                        'amount': min(item['price'], data['policy']['max_vnd']), 'issue': 'missing'}
        return {"text": json.dumps(decision, ensure_ascii=False), "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER != 'openai':
        raise ValueError('Bản CP3 hỗ trợ MODEL_PROVIDER=openai hoặc fake.')
    if not MODEL_NAME or not API_KEY:
        raise ValueError('Thiếu MODEL_NAME hoặc API_KEY trong .env; không in key ra log.')
    body = {
        'model': MODEL_NAME,
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
        'response_format': {'type': 'json_object'},
        'max_completion_tokens': 512,
    }
    request = urllib.request.Request(
        'https://api.openai.com/v1/chat/completions',
        data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY},
        method='POST')
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        message = {401: 'API key không hợp lệ', 403: 'không có quyền truy cập model',
                   429: 'hết quota hoặc bị giới hạn lượt'}.get(error.code, 'lỗi nhà cung cấp')
        raise RuntimeError(f'OpenAI HTTP {error.code}: {message}. Kiểm tra cấu hình/tài khoản.') from None
    except (urllib.error.URLError, OSError):
        raise RuntimeError('Không kết nối được OpenAI; kiểm tra mạng.') from None
    except (ValueError, UnicodeError):
        raise RuntimeError('OpenAI trả dữ liệu không đúng JSON; chuyển nhân viên.') from None
    try:
        choice = result['choices'][0]
        finish_reason = choice['finish_reason']
        text = choice['message']['content']
        usage = result['usage']
        tokens_in, tokens_out = usage['prompt_tokens'], usage['completion_tokens']
        model = result['model']
    except (KeyError, IndexError, TypeError):
        raise RuntimeError('OpenAI trả thiếu trường bắt buộc; không được ước lượng token.') from None
    if finish_reason != 'stop':
        raise RuntimeError('OpenAI chưa trả quyết định hoàn chỉnh; không dùng output bị cắt.')
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError('OpenAI trả nội dung rỗng hoặc từ chối; chuyển nhân viên.')
    if not isinstance(model, str) or not model.strip():
        raise RuntimeError('OpenAI không trả tên model hợp lệ.')
    if any(type(value) is not int or value < 0 for value in (tokens_in, tokens_out)):
        raise ValueError('OpenAI không trả usage token hợp lệ; không được ước lượng token.')
    return {'text': text, 'model': model,
            'tokens_in': tokens_in, 'tokens_out': tokens_out}
