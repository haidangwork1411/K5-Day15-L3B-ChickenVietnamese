"""Live D01–D03 check: stop at the first failure, keep numbered runs untouched."""
from functools import partial
import json
import re
import sys
import time

from run_eval import CODEBASE, call_case, load_items

sys.path.insert(0, CODEBASE)
import ai
import tracing
from agent import answer
from decision_contract import DECISION_SCHEMA


def print_decision(decision, order):
    """Show the original field types and safe values, including misplaced enum tokens."""
    if not isinstance(decision, dict):
        print(f"decision_json: [root={type(decision).__name__}]", flush=True)
        return
    props = DECISION_SCHEMA["properties"]
    words = set(props["action"]["enum"]) | set(props["issue"]["enum"]) | {
        "refund", "compensate", "compensation", "missing_item", "missing_food",
        "missing_one_item", "missing_dish", "propose_refund", "request_info", "escalate",
    }
    items = {item["name"] for item in order["items"]}
    safe = {}
    for key in props.keys() & decision.keys():
        value = decision[key]
        if value is None or type(value) is bool:
            safe[key] = value
        elif key in ("action", "issue") and isinstance(value, str) and len(value) <= 60 and all(
                part in words for part in value.strip().lower().split("/")):
            safe[key] = value
        elif key == "item" and isinstance(value, str) and value in items:
            safe[key] = value
        elif key == "amount" and type(value) in (int, float) and abs(value) <= 1_000_000:
            safe[key] = value
        elif key == "amount" and isinstance(value, str) and re.fullmatch(r"[0-9]{1,6}", value):
            safe[key] = value
        else:
            safe[key] = f"[redacted {type(value).__name__}]"
    print("decision_json:", json.dumps(safe, ensure_ascii=False, sort_keys=True),
          f"(extra_fields={len(decision.keys() - props.keys())})", flush=True)


def main():
    if ai.MODEL_PROVIDER != 'openrouter' or not ai.API_KEY or not ai.MODEL_NAME.endswith(':free'):
        sys.exit('Cần MODEL_PROVIDER=openrouter, MODEL_NAME có hậu tố :free và API_KEY local.')
    cases = {row['id']: row for row in load_items()}
    # These smoke cases exercise both the item-price limit and the policy limit.
    checks = [('D01', 'cơm gà', 40000), ('D02', 'trà', 20000), ('D03', 'bún', 40000)]
    for index, (case_id, item, amount) in enumerate(checks):
        if index:
            time.sleep(4)
        row, events = call_case(partial(answer, on_decision=print_decision), tracing, case_id, cases[case_id]['input'])
        print(f"{case_id}: model={row['model'] or '—'} token={row['tokens_in']}/{row['tokens_out']}",
              flush=True)
        for event in events:
            if event['kind'] == 'note' and event['text'].startswith('guardrail:'):
                print(f"{case_id}: {event['text']}", flush=True)
        if row['error']:
            for event in events:
                if event['kind'] == 'model' and event.get('error'):
                    print(event['error'], flush=True)
            sys.exit(row['error'])
        output = row['output']
        print(output, flush=True)
        if (row['model'].removesuffix(':free') != ai.MODEL_NAME.removesuffix(':free')
                or min(row['tokens_in'], row['tokens_out']) <= 0
                or f'món {item},' not in output or f'đề xuất tối đa {amount} VND' not in output
                or 'Nhân viên xác minh và quyết định' not in output):
            sys.exit(f'{case_id}: cần kiểm lại model, usage hoặc đề xuất trước khi chạy tiếp.')
    print('Smoke 3/3 đạt. Chưa chạy Run-1.')


if __name__ == '__main__':
    main()
