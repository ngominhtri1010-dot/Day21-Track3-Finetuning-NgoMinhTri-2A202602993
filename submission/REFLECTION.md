# Reflection — Lab 21

*Ngắn gọn, thành thật. Phần này chấm theo độ cụ thể, không theo độ dài.*

**1. Điều gì làm bạn ngạc nhiên nhất?**

Điểm đáng chú ý nhất trong kết quả là fine-tune đạt target 0,970 nhưng vẫn
FAILED cổng hồi quy: regression giảm từ 0,7911 xuống 0,6111. Một model làm
tốt hơn trên ticket chưa chắc phù hợp với hệ thống còn phải trả lời câu hỏi
phổ thông. Vì vậy tôi cần đọc cả phán quyết và các nhóm điểm, thay vì chỉ
xem train xong hay chưa.

**2. Bạn mất nhiều thời gian nhất ở đâu? Nó có phải chỗ bạn dự đoán không?**

Ô 3 trên Colab (Core pipeline NB1 → NB5) chạy khá lâu. Khi chạy, tôi chưa
hiểu vì sao ô này mất nhiều thời gian. Tôi cần phân biệt thời gian đo baseline,
huấn luyện bốn cấu hình và sinh câu trả lời để đánh giá, thay vì coi ô 3 là
một bước huấn luyện duy nhất.

**3. Trước lab này bạn tin điều gì về fine-tuning mà giờ bạn không còn tin?**

Ban đầu tôi chưa phân biệt rõ vai trò của Colab và VS Code: tôi hỏi liệu
Colab chỉ dùng để test và có thể làm toàn bộ bằng vibe coding hay không.
Qua luồng chạy này, tôi phân biệt được viết/sửa code với chạy thực nghiệm:
VS Code hỗ trợ phần code và NB1 trên máy, còn GPU T4 thực hiện huấn luyện
và đánh giá. Lab cũng chạy model trực tiếp, không cần API key để gọi một
dịch vụ model. Viết được pipeline chưa thay thế được việc chạy pipeline
và kiểm tra các số liệu sinh ra.

**4. Bạn dùng AI assistant vào việc gì trong lab? Chỗ nào nó sai?**

AI assistant giúp kiểm tra setup, giải thích cách dùng Colab, viết script đánh giá
đầy đủ và soạn báo cáo từ kết quả. Hướng dẫn ban đầu chạy lại NB2 + NB5 chưa nêu
rõ giới hạn: baseline full được đo sau train, còn baseline trước train chỉ có 8 mẫu.
Điểm này đã được bổ sung trong báo cáo và lưu bằng chứng gốc.

**5. Nếu ngày mai phải fine-tune cho một khách hàng thật, bước đầu tiên bạn làm là gì?**

Tôi sẽ làm rõ đầu ra khách hàng cần và những năng lực model phải giữ lại,
rồi chuẩn bị tập đánh giá riêng cho cả hai yêu cầu đó. Trước khi train,
tôi sẽ đo baseline prompt đủ mạnh trên toàn bộ tập và lưu phiên bản
prompt, dữ liệu cùng kết quả. Sau đó mới quyết định fine-tune có cần thiết
hay không, kiểm tra loss mask và chọn cấu hình theo GPU. Kết quả lab này
cho thấy bỏ qua nhóm regression có thể khiến tôi chọn một adapter đạt
điểm ticket cao nhưng không đáp ứng yêu cầu tổng thể.
