"""Build with Python + reportlab; inspect with PyMuPDF. Output: ../demo-slides.pdf."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
FONT = Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("Sans", str(FONT / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Bold", str(FONT / "DejaVuSans-Bold.ttf")))
SLIDES = [
("Người dùng & pain", "18/150 review phản ánh khó khăn hỗ trợ", [
("Người dùng", "Khách vừa nhận đơn giao đồ ăn, muốn báo thiếu một món và biết bước xử lý tiếp theo."),
("Bằng chứng", "12% mẫu review phản ánh khó khăn hỗ trợ hoặc hoàn tiền. RV013 viết “tốn hết cả thgian”."),
("Giới hạn", "CP3: 0/150 trực tiếp nêu thiếu món. CP4 bổ sung 4 bài tự báo thiếu món, 3 bài khó bồi hoàn; tuyển có chủ đích ở Singapore, chưa đo tỷ lệ Việt Nam.")],
"evidence/summary.md; TV3 bce01cf: evidence/cp4/README.md", False),
("Vì sao chọn thiếu món", "540 phút/tháng trong kịch bản tự ước tính", [
("So sánh trên 100 khách", "Thiếu món: 20 × 1,8 × 15 = 540 phút. Sai món: 15 × 1,2 × 10 = 180 phút. Giao trễ: 25 × 1,2 × 5 = 150 phút."),
("Lý do chọn", "Một món, một giá và một hạn mức tạo phạm vi có thể kiểm tra được trong hackathon."),
("Giả định", "N, F, C đều tự ước tính. 540 phút là tổn thất giả định; mức tiết kiệm thực tế chưa được đo.")],
"spec.md §2; evidence/impact.md", False),
("Giải pháp", "AI đề xuất • nhân viên quyết định", [
("Workflow cố định", "Khiếu nại → kiểm rủi ro → tra đơn & chính sách → ERNIE quyết định JSON → kiểm món & hạn mức → bản nháp cho nhân viên."),
("Dữ liệu và quyền hạn", "2 đơn, 4 món và chính sách giả lập. Hai công cụ chỉ đọc. Đề xuất tối đa bằng giá món hoặc 40.000 VND, lấy mức thấp hơn."),
("Rào chắn", "Thiếu căn cứ thì hỏi lại; ca nguy hiểm hoặc ngoài phạm vi hướng tới nhân viên. Mọi giao dịch cần nhân viên xác minh.")],
"spec.md §4–§6; data/DATA_CARD.md; codebase/agent.py", False),
("Demo live", "Một ca thường và một ca khó", [
("Ca thường · D01", "Nhập D100 thiếu cơm gà. Quan sát giá 50.000 VND, đề xuất tối đa 40.000 VND, quyền quyết định của nhân viên và token thực tế."),
("Ca khó · D06", "Nhập D100 thiếu pizza. Quan sát yêu cầu xác nhận món thuộc đơn và việc chưa đề xuất tiền. Hệ thống hướng dẫn mở chi tiết đơn, gửi đúng tên một món đã đặt nhưng chưa nhận."),
("Video dự phòng", "Video CP3 dài 29,89 giây thể hiện ca D01. Link trong README đã được nhóm mở thử bằng cửa sổ ẩn danh.")],
"eval/benchmark.csv D01/D06; TV2 e87f5fc codebase/agent.py", False),
("Đánh giá thế nào", "Run-1 đạt 20/20 • Run-2 đạt 20/20", [
("Dataset & metric", "20 câu: 4 thường, 14 khó, 2 từ chối; 7/20 từ review. Ngưỡng: đúng hướng ≥80%, đúng căn cứ 100%, an toàn 100%."),
("Run-1 · run-1@20261128-092900", "Đúng hướng 20/20; đúng căn cứ 4/4; an toàn 5/5. Hai người chấm khớp 5/5. Lỗi kỹ thuật 0; câu trượt 0."),
("Trước / sau", "Run-2 run-2@20261128-120942: đạt 20/20 đã duyệt. D06/D07 đủ nơi đối chiếu + thông tin cần gửi: 0/2 → 2/2. 18 output giữ nguyên. Token ra +198; latency +2,003 giây. Chưa đo hiệu quả người dùng.")],
"eval/README.md §2–§5; eval/report.md; eval/metric_spec.yaml", True),
("Chi phí khi dùng thật", "50 phiên • 89 lượt hỏi • 0 lỗi", [
("Đo ERNIE, áp giá Gemini", "18.406 token vào, 4.707 token ra. Biểu giá BTC ngày 25/11/2026; chưa đo chất lượng Gemini. Tỷ lệ dùng tính task: Run-2 20/20."),
("USD theo hai tầng giá", "Flash-Lite: $0.00023/task; tháng thấp/cơ sở/cao $0.0027 / $0.0109 / $0.0218. Hydrogen: $0.0013/task; $0.0147 / $0.0589 / $0.1179."),
("So với impact", "Cơ sở: $0.00055 / $0.0029 mỗi người/tháng. Tổn thất 27 phút/người/tháng tự ước tính; phần tiết kiệm và chi phí nhân viên chưa đo.")],
"cost/simulate-1-summary.md; cost/cost-estimate.md; spec.md §2", False),
("Kết luận", "Đề xuất ITERATE trước khi triển khai", [
("Có cơ sở tiếp tục", "Hai lượt cùng 20/20. Hai câu hướng dẫn rõ hơn 0/2 → 2/2. Chi phí token cơ sở giả định $0.0109 / $0.0589 mỗi tháng."),
("Giới hạn cần giải quyết", "0/150 review CP3 trực tiếp nêu thiếu món; nguồn bổ sung tuyển có chủ đích. Prototype dùng 2 đơn giả lập, chưa đo thành công với khách thật."),
("Việc tiếp theo", "Kiểm chứng pain, đo mức tiết kiệm và thời gian nhân viên duyệt. Chỉ quyết định triển khai khi có lợi ích thực và chi phí vận hành đầy đủ.")],
"evidence/summary.md; eval/report.md; cost/cost-estimate.md", False),
("Nếu có thêm một tuần", "Ba việc xuất phát từ giới hạn hiện tại", [
("Kiểm chứng pain", "Tìm khách từng thiếu món, hỏi sự việc gần nhất và đo thời gian xử lý. Mẫu hiện tại có 0/150 trích đoạn trực tiếp nêu thiếu món."),
("Đánh giá khả năng khái quát", "Kiểm thêm cách diễn đạt ngoài bộ 20 câu; ghi lỗi thật và độ hữu ích khi hỏi lại, dựa trên D06/D07."),
("Kiểm quy trình vận hành", "Đo thời gian nhân viên duyệt và chi phí vận hành. Kiểm trải nghiệm với người ngoài nhóm trước khi mở rộng.")],
"evidence/summary.md §4; eval/report.md §2, §4; spec.md §6", False),
]
pdf = canvas.Canvas(str(ROOT / "demo-slides.pdf"), pagesize=(960, 540))
pdf.setTitle("ChickenVietnamese — CP4")
pdf.setAuthor("ChickenVietnamese")
def paragraph(text, x, top, width, size, font, color):
    style = ParagraphStyle("text", fontName=font, fontSize=size, leading=size*1.4, textColor=HexColor(color))
    para = Paragraph(escape(text), style)
    _, height = para.wrap(width, 500)
    assert top + height <= 492, (text, top, height)
    para.drawOn(pdf, x, 540-top-height)
    return height
for index, (title, headline, blocks, source, draft) in enumerate(SLIDES, 1):
    pdf.setFillColor(HexColor("#F4F3EE")); pdf.rect(0, 0, 960, 540, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#143E38")); pdf.rect(0, 532, 960, 8, fill=1, stroke=0)
    paragraph("CHICKENVIETNAMESE  /  L3B · D1", 42, 25, 620, 11, "Bold", "#143E38")
    paragraph("CP4 · 28/11/2026", 655, 25, 270, 10, "Bold", "#966022")
    paragraph(title, 42, 64, 875, 30, "Bold", "#142E2A")
    paragraph(headline, 42, 113, 875, 21, "Sans", "#235D51")
    top = 171
    for label, body in blocks:
        paragraph(label, 42, top, 205, 15, "Bold", "#143E38")
        height = paragraph(body, 265, top, 650, 16, "Sans", "#263A36")
        top += max(70, height+22)
    pdf.setStrokeColor(HexColor("#C5D0C8")); pdf.line(42, 49, 918, 49)
    pdf.setFont("Sans", 9);pdf.setFillColor(HexColor("#4C6159"))
    assert pdfmetrics.stringWidth(source, "Sans", 9)<830
    pdf.drawString(42, 31, source)
    pdf.drawRightString(918, 31, f"{index}/8")
    pdf.showPage()
pdf.save()
