# Trạng thái bài nộp

Đã nhập kết quả T4, soạn REPORT.md và kiểm tra: 26 PASS, 1 WARN, 0 FAIL.
WARN là model FAILED cổng hồi quy, không phải lỗi chạy pipeline.

Giới hạn rubric còn lại:
- Baseline trước train chỉ đo 8 mẫu; full baseline đo sau train, đã khai báo.
- 50 target có 33 thắng, 17 hòa, 0 thua. Không có 2 ca FT thua baseline
  để đáp ứng mục 3.4; báo cáo đưa ca hòa cùng sai và không gọi chúng là thua.

REPORT.md và cả năm câu REFLECTION.md đã hoàn thiện từ số liệu và cuộc trao đổi.
Người nộp cần đọc để xác nhận phần diễn giải phù hợp với cách hiểu của mình.

Không cần thêm Colab để dùng các kết quả hiện có. Nếu yêu cầu tuân thủ đầy đủ
baseline trước train trên full eval, cần một lần train mới sau khi đóng băng full
baseline, rồi đo lại NB5; không sửa mốc hay dữ liệu để che trình tự cũ.
Không chạy thêm GPU chỉ để tìm ca thua hoặc ép phán quyết PASSED.

Nộp qua repo theo nội dung Option C: xem LINKS.md. Results JSON/CSV được đưa
vào Git; trọng số, ZIP và bản sao lưu cục bộ được bỏ qua.
Baseline trước train được lưu ở submission/evidence/baselines_before_training.json.

ZIP dự phòng: dist/lab21_2A202620993.zip. Đọc REPORT trước khi nộp.
Nếu sửa report/reflection sau khi đóng gói, cần tạo lại ZIP để có bản mới.
