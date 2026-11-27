"""Công cụ chỉ đọc dataset synthetic D1; không tác động hệ thống bên ngoài."""
import json
from pathlib import Path
import re

from tracing import tool


DATA = Path(__file__).resolve().parent.parent / "data" / "d1_orders.json"


def _read_dataset():
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or set(data) != {"orders", "policy"}:
        raise ValueError("Dataset synthetic không đúng schema.")
    orders, policy = data["orders"], data["policy"]
    if not isinstance(orders, list) or not isinstance(policy, dict):
        raise ValueError("Orders/policy không đúng kiểu.")
    if (set(policy) != {"max_vnd", "description"}
            or type(policy["max_vnd"]) is not int or policy["max_vnd"] < 0
            or not isinstance(policy["description"], str)):
        raise ValueError("Chính sách synthetic không hợp lệ.")
    ids = set()
    for order in orders:
        if not isinstance(order, dict) or set(order) != {"id", "items"}:
            raise ValueError("Đơn synthetic không đúng schema.")
        order_id, items = order["id"], order["items"]
        if (not isinstance(order_id, str) or not re.fullmatch(r"D\d{3}", order_id)
                or order_id in ids):
            raise ValueError("Mã đơn synthetic không hợp lệ hoặc trùng.")
        ids.add(order_id)
        if not isinstance(items, list) or not items:
            raise ValueError("Danh sách món không hợp lệ.")
        names = set()
        for item in items:
            if not isinstance(item, dict) or set(item) != {"name", "price"}:
                raise ValueError("Món synthetic không đúng schema.")
            name, price = item["name"], item["price"]
            if (not isinstance(name, str) or not name.strip() or name in names
                    or type(price) is not int or price < 0):
                raise ValueError("Tên hoặc giá món synthetic không hợp lệ.")
            names.add(name)
    return data


@tool
def get_order(order_id):
    """get_order · input mã đơn · output đơn synthetic/None · không tác động ra ngoài."""
    data = _read_dataset()
    return next((order for order in data["orders"] if order["id"] == order_id), None)


@tool
def get_policy():
    """get_policy · không input · output chính sách synthetic · không tác động ra ngoài."""
    return _read_dataset()["policy"]
