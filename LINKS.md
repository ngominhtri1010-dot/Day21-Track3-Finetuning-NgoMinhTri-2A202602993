# Lab 21 — Nộp qua GitHub

- Học viên: Ngô Minh Trí — 2A202620993
- Repo: https://github.com/ngominhtri1010-dot/Day21-Track3-Finetuning-Lab
- Báo cáo: [submission/REPORT.md](submission/REPORT.md)
- Phản tư: [submission/REFLECTION.md](submission/REFLECTION.md)
- Kết quả thực nghiệm: [results/](results/)
- Baseline trước train (8 mẫu): [submission/evidence/baselines_before_training.json](submission/evidence/baselines_before_training.json)

Repo chứa nội dung **Option C (code-only)** trong rubric: báo cáo, toàn bộ kết quả
JSON/CSV, code và requirements để tái lập. Không nhận điểm thưởng Hugging Face Hub;
chưa upload adapter lên Hub và chưa áp dụng Option B.

Adapter đã train được giữ trong ZIP bằng chứng và trên máy cá nhân, không đưa
trọng số lớn vào Git. Nếu nơi nhận yêu cầu Option B hoặc adapter, cần cung cấp
adapter riêng (Hub hoặc ZIP Option A), không chỉ link repo code-only.

Kiểm tra tại thư mục repo sau khi cài môi trường CPU:

```bash
make setup-cpu
make verify
```

Phán quyết model FAILED do regression giảm; đây là kết quả được phân tích trong
báo cáo. Baseline full đo sau train và thiếu hai ca FT thua trên target được
khai báo rõ. Chạy `make nb1` sẽ ghi đè kết quả NB1 đã nộp bằng kết quả máy hiện tại;
hãy giữ bản đã commit khi chỉ muốn kiểm tra bài.
