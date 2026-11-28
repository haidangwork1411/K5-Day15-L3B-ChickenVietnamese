"use strict";
const $ = id => document.getElementById(id);
const KEY = "chickenvietnamese-demo-history-v1";
let conversations = [], activeId = null, busy = false, ready = false;
try {
  const saved = JSON.parse(localStorage.getItem(KEY) || "[]");
  if (Array.isArray(saved)) conversations = saved.filter(c =>
    typeof c.id === "string" && typeof c.title === "string" && Array.isArray(c.messages)
    && c.messages.every(m => typeof m.text === "string" && ["user", "system", "error"].includes(m.role))
  );
} catch { $("feedback").textContent = "Không đọc được lịch sử đã lưu."; }
activeId = conversations[0]?.id || null;
function current() { return conversations.find(c => c.id === activeId); }
function persist() {
  try { localStorage.setItem(KEY, JSON.stringify(conversations)); }
  catch { $("feedback").textContent = "Trình duyệt không lưu được lịch sử. Nội dung hiện tại vẫn hiển thị."; }
}
function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}
function newConversation() {
  if (busy) return;
  const c = {id: crypto.randomUUID(), title: "Hội thoại mới", time: new Date().toISOString(), messages: []};
  conversations.unshift(c); activeId = c.id;
  persist(); render(); $("input").focus();
}
function renderPanel(data) {
  $("fields").replaceChildren();
  $("detail-empty").hidden = Boolean(data);
  if (!data) return;
  const actions = {propose: "Đề xuất phương án", ask: "Yêu cầu xác nhận", refuse: "Từ chối yêu cầu", handoff: "Hướng tới nhân viên"};
  const fields = [
    ["Chế độ phản hồi", data.mode === "mock" ? "Mock Mode" : "Live"],
    ["Mã đơn hàng", data.order_id], ["Món cần xác minh", data.item],
    ["Hướng xử lý", actions[data.action]], ["Mức đề xuất", Number.isInteger(data.amount) ? new Intl.NumberFormat("vi-VN").format(data.amount) + " VND" : null],
    ["Phê duyệt", data.approval], ["Model thực gọi", data.model || "Không gọi model trong yêu cầu này"],
    ["Token vào / ra", data.tokens_in + " / " + data.tokens_out],
    ["Model / tool calls", data.model_calls + " / " + data.tool_calls]
  ];
  for (const [label, value] of fields) {
    if (value != null) $("fields").append(node("dt", label), node("dd", String(value)));
  }
}
function render() {
  $("history").replaceChildren();
  for (const c of conversations) {
    const row = node("div", undefined, "history-row" + (c.id === activeId ? " active" : ""));
    const open = node("button", undefined, "history-open");
    open.append(node("span", c.title), node("small", new Date(c.time).toLocaleDateString("vi-VN")));
    open.disabled = busy;
    open.onclick = () => {activeId = c.id; $("feedback").textContent = ""; render();};
    const del = node("button", "×", "delete");
    del.setAttribute("aria-label", "Xóa " + c.title); del.disabled = busy;
    del.onclick = () => {
      if (!confirm("Xóa hội thoại này khỏi trình duyệt?")) return;
      conversations = conversations.filter(item => item.id !== c.id);
      if (activeId === c.id) activeId = conversations[0]?.id || null;
      persist(); render();
    };
    row.append(open, del); $("history").append(row);
  }
  const messages = current()?.messages || [];
  $("messages").replaceChildren();
  $("empty").hidden = messages.length > 0;
  for (const m of messages) {
    const article = node("article", undefined, "message " + m.role);
    const label = m.role === "user" ? "Khách hàng" : m.role === "error" ? "Yêu cầu chưa hoàn tất" : "Hỗ trợ đơn hàng" + (m.data?.mode === "mock" ? " · Mock Mode" : "");
    article.append(node("p", label, "label"), node("div", m.text, "bubble"));
    article.append(node("time", new Date(m.time).toLocaleTimeString("vi-VN", {hour: "2-digit", minute: "2-digit"})));
    $("messages").append(article);
  }
  const last = messages[messages.length - 1];
  renderPanel(last?.role === "system" ? last.data : null);
  $("messages").scrollTop = $("messages").scrollHeight;
  $("new").disabled = busy;
  $("send").disabled = busy || !ready;
  $("send").textContent = busy ? "Đang xử lý…" : "Gửi yêu cầu ↗";
  $("input").disabled = busy;
  for (const button of document.querySelectorAll("[data-sample]")) button.disabled = busy;
}
$("new").onclick = newConversation;
for (const button of document.querySelectorAll("[data-sample]")) {
  button.onclick = () => {$("input").value = button.dataset.sample; $("input").focus();};
}
$("input").addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault(); $("form").requestSubmit();
  }
});
$("form").onsubmit = async event => {
  event.preventDefault();
  const text = $("input").value.trim();
  if (!text || busy || !ready) return;
  if (!current()) newConversation();
  const c = current();
  if (!c.messages.length) c.title = text.slice(0,45);
  c.messages.push({role: "user", text, time: new Date().toISOString()});
  busy = true; $("input").value = "";
  $("feedback").textContent = "Đang đối chiếu thông tin…";
  persist(); render();
  try {
    const response = await fetch("/api/answer", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({text})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Không xử lý được yêu cầu.");
    c.messages.push({role: "system", text: data.output, data, time: new Date().toISOString()});
    $("feedback").textContent = "";
  } catch (error) {
    c.messages.push({role: "error", text: error.message === "Failed to fetch" ? "Mất kết nối tới localhost. Kiểm tra server trước khi gửi lại." : error.message, time: new Date().toISOString()});
    $("feedback").textContent = "Có thể thử lại sau khi kiểm tra server.";
  } finally {
    busy = false; persist(); render(); $("input").focus();
  }
};
render();
fetch("/api/status").then(r => {if (!r.ok) throw new Error(); return r.json();}).then(data => {
  ready = data.ready;
  $("status").textContent = !ready ? "Chưa sẵn sàng · kiểm tra cấu hình" : data.mode === "mock" ? "● Mock Mode" : "● Live · OpenRouter ERNIE";
  render();
}).catch(() => {$("status").textContent = "Mất kết nối server"; ready = false; render();});
