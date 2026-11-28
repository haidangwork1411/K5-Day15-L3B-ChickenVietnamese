# Demo localhost

Từ root repo, dùng Python 3.10+ và thư viện chuẩn:

    python3 demo_ui/server.py

Mở http://127.0.0.1:8000. Server dùng biến môi trường hiện có hoặc .env ở root. Để demo live:

    export MODEL_PROVIDER=openrouter
    export MODEL_NAME=baidu/ernie-5.5-flash-preview:free
    python3 demo_ui/server.py

API_KEY phải có trong terminal hoặc .env cục bộ. Key chỉ được đọc phía Python. Nhập một ca D100 thiếu cơm gà để tự kiểm live; thao tác này dùng quota. Dừng server cũ bằng Ctrl+C trước khi thay cấu hình.

Thử offline bằng MODEL_PROVIDER=fake python3 demo_ui/server.py. Header và từng phản hồi ghi Mock Mode. Live yêu cầu đúng model ERNIE đã chốt. Lỗi API được báo lỗi, người dùng quyết định gửi lại.

## Sử dụng

- Chọn tình huống gợi ý để điền nội dung, bấm gửi hoặc Enter. Shift+Enter xuống dòng.
- Hội thoại mới, mở lại hoặc xóa lịch sử ở sidebar. Lịch sử lưu trên trình duyệt, refresh vẫn còn nếu localStorage được cho phép.
- Chỉ nhập dữ liệu demo giả lập. Nội dung hội thoại lưu nguyên văn trong trình duyệt; người vận hành chịu trách nhiệm tránh dữ liệu cá nhân thật và có thể xóa từng hội thoại.
- Panel chỉ hiện trường có căn cứ từ quyết định backend được chấp nhận và tracing. Ca kết thúc sớm có thể chỉ có số call/token.
- Mỗi yêu cầu gọi agent.answer(text) độc lập. Lịch sử hiển thị không được gửi làm memory cho model.
- Server chỉ bind 127.0.0.1:8000. Một yêu cầu được xử lý tại một thời điểm vì tracing dùng trạng thái chung.
- CLI python3 run.py và video CP3 trong README root là phương án dự phòng.

Chưa xác thực chủ đơn hoặc kết nối hàng đợi nhân viên, không thực hiện giao dịch. Live adapter đã nối cùng prototype, cần người vận hành kiểm một ca bằng key và quota của mình.

## Trạng thái sau CP4

Ngày 28/11, kiểm thử offline dùng Mock Mode; nhánh không cần model cũng đã phản hồi qua UI. Lần thử live D100 cần model trả 502; kiểm tra key endpoint cho thấy quota miễn phí đã hết (51/50). Chưa có kết quả live end-to-end thành công qua UI. Lỗi được hiển thị và không tự chuyển sang mock.
