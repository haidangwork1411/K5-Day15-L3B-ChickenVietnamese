"""Chat Completions (OpenAI/OpenRouter) — chỗ duy nhất trong bản chạy thử gọi model AI, giữ @model_call.

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

Nối model thật: điền .env theo .env.example, MODEL_PROVIDER=openrouter hoặc openai, MODEL_NAME và
API_KEY. Bản CP3 dùng Chat Completions JSON mode, lấy token trực tiếp từ usage.
Không dán API key vào file này hoặc ghi request header/body lỗi vào log.
"""
from email.utils import parsedate_to_datetime
import os
import re
import json
import urllib.error
import urllib.request

from decision_contract import DECISION_SCHEMA
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


def _router_error_details(error, retry_after=None):
    """Keep routing identifiers and a category, never provider text or request data."""
    if not isinstance(error, dict):
        error = {}
    metadata = error.get('metadata')
    if not isinstance(metadata, dict):
        metadata = {}
    details = []
    for field in ('limit_source', 'provider_name'):
        value = metadata.get(field)
        if (isinstance(value, str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9 _.-]{0,49}', value)
                and not value.lower().startswith(('sk-', 'bearer ', 'ghp_'))
                and not (API_KEY and API_KEY in value)):
            details.append(f'{field}={value}')
    raw = metadata.get('raw')
    # Raw payloads can echo private prompts or headers. Emit only known categories.
    for label, source in [('raw', raw), ('message', error.get('message'))]:
        if source is None:
            continue
        normalized = str(source).lower().replace('_', ' ').replace('-', ' ')
        for category, markers in (
            ('rate_limited_upstream', ('rate limited upstream', 'upstream rate limit')),
            ('rate_limited', ('rate limit', 'resource exhausted', 'too many requests')),
            ('quota', ('quota',)), ('capacity', ('capacity', 'overload')),
            ('routing', ('no endpoint', 'no provider')),
            ('unsupported_parameter', ('unsupported parameter', 'unsupported response')),
        ):
            if any(marker in normalized for marker in markers):
                details.append(f'{label}={category}')
                break
        else:
            if label == 'raw':
                details.append('raw=unclassified')
    delay = retry_after or metadata.get('retry_after') or error.get('retry_after')
    if delay is not None:
        delay = str(delay)
        if re.fullmatch(r'[0-9]{1,9}(?:[.][0-9]{1,3})?', delay):
            details.append(f'retry_after={delay}s')
        else:
            try:
                retry_at = parsedate_to_datetime(delay)
            except (TypeError, ValueError, OverflowError):
                pass
            else:
                details.append(f'retry_after={retry_at.isoformat()}')
    return ' '.join(details)


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
    if MODEL_PROVIDER == 'openrouter':
        provider, endpoint = 'OpenRouter', 'https://openrouter.ai/api/v1/chat/completions'
    elif MODEL_PROVIDER == 'openai':
        provider, endpoint = 'OpenAI', 'https://api.openai.com/v1/chat/completions'
    else:
        raise ValueError('Bản CP3 hỗ trợ MODEL_PROVIDER=openrouter, openai hoặc fake.')
    if not MODEL_NAME or not API_KEY:
        raise ValueError('Thiếu MODEL_NAME hoặc API_KEY trong .env; không in key ra log.')
    body = {
        'model': MODEL_NAME,
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
        'response_format': {'type': 'json_object'},
    }
    if MODEL_PROVIDER == 'openrouter':
        if not MODEL_NAME.endswith(':free'):
            raise ValueError('CP3 yêu cầu một model ID OpenRouter có hậu tố :free.')
        if MODEL_NAME == 'baidu/ernie-5.5-flash-preview:free':
            body['response_format'] = {
                'type': 'json_schema',
                'json_schema': {'name': 'complaint_decision', 'strict': True, 'schema': DECISION_SCHEMA},
            }
        body['max_tokens'] = 2048  # Includes reasoning tokens before the JSON answer.
        body['provider'] = {'require_parameters': True, 'allow_fallbacks': True,
                            'max_price': {'prompt': 0, 'completion': 0, 'request': 0}}
    else:
        body['max_completion_tokens'] = 512
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY},
        method='POST')
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        if MODEL_PROVIDER == 'openrouter':
            try:
                payload = json.loads(error.read(65536))
            except (ValueError, OSError):
                payload = {}
            metadata_error = payload.get('error') if isinstance(payload, dict) else None
            delay = error.headers.get('Retry-After') if error.headers else None
            details = _router_error_details(metadata_error, delay)
            raise RuntimeError(f'OpenRouter HTTP {error.code} {details}'.rstrip()) from None
        message = {401: 'API key không hợp lệ', 403: 'không có quyền truy cập model',
                   429: 'hết quota hoặc bị giới hạn lượt'}.get(error.code, 'lỗi nhà cung cấp')
        raise RuntimeError(f'{provider} HTTP {error.code}: {message}. Kiểm tra cấu hình/tài khoản.') from None
    except (urllib.error.URLError, OSError):
        raise RuntimeError(f'Không kết nối được {provider}; kiểm tra mạng hoặc timeout.') from None
    except (ValueError, UnicodeError):
        raise RuntimeError(f'{provider} trả dữ liệu không đúng JSON; chuyển nhân viên.') from None
    # OpenRouter can report an upstream error inside an HTTP 200 response.
    if isinstance(result, dict) and result.get('error') is not None:
        error = result['error']
        code = error.get('code') if isinstance(error, dict) else None
        label = f' ({code})' if type(code) is int else ''
        details = _router_error_details(error) if MODEL_PROVIDER == 'openrouter' else ''
        raise RuntimeError(f'{provider} báo lỗi{label} {details}'.rstrip())
    try:
        choice = result['choices'][0]
        finish_reason = choice['finish_reason']
        text = choice['message']['content']
        usage = result['usage']
        tokens_in, tokens_out = usage['prompt_tokens'], usage['completion_tokens']
        model = result['model']
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f'{provider} trả thiếu trường bắt buộc; không được ước lượng token.') from None
    if finish_reason != 'stop':
        raise RuntimeError(f'{provider} chưa trả quyết định hoàn chỉnh; không dùng output bị cắt.')
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError(f'{provider} trả nội dung rỗng hoặc từ chối; chuyển nhân viên.')
    if not isinstance(model, str) or not model.strip():
        raise RuntimeError(f'{provider} không trả tên model hợp lệ.')
    if any(type(value) is not int or value < 0 for value in (tokens_in, tokens_out)):
        raise ValueError(f'{provider} không trả usage token hợp lệ; không được ước lượng token.')
    return {'text': text, 'model': model,
            'tokens_in': tokens_in, 'tokens_out': tokens_out}
