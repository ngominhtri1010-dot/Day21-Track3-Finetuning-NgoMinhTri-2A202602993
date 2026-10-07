# Hoàn thiện lab từ runtime Colab hiện tại

Máy cá nhân hiện chỉ có kết quả NB1. Không dùng số đo NB1 CPU thay cho
kết quả NB1 T4 trong báo cáo cuối. Chưa đủ dữ liệu để điền các bảng NB2–NB5.

## 1. Chạy đánh giá đầy đủ trên Colab

Giữ runtime đang chứa bốn adapter. Không chạy lại Setup, không thay model,
prompt hay tập eval. Lần đầu đã đo baseline trước train trên 8 mẫu;
lần đánh giá đầy đủ sau train cần khai báo đúng trình tự này trong report.

Upload file `scripts/finish_colab.py` từ máy bằng bảng Files của Colab vào
thư mục `scripts/` của repo đã clone (cùng thư mục với `colab_run.py`).
Tạo ô mới ngay sau ô 3 và chạy:

```python
%run scripts/finish_colab.py
```

Script sao lưu kết quả cũ vào `evaluation_backups/`, chạy NB2 + NB5 trên
toàn bộ tập eval và lưu dự đoán đầy đủ để so sánh định tính. Không train lại.
Giữ `COMPUTE_TIER=T4`; nếu dùng ô 3 về sau, để `EVAL_LIMIT=""`.
Không chạy thêm ô 3 với `EVAL_LIMIT=8` sau bước này vì sẽ ghi đè kết quả full.

Nếu script báo thiếu adapter, dừng và kiểm tra runtime/bản sao lưu;
không thể đánh giá lại bằng các file NB1 ở máy cá nhân.

## 2. Tải bằng chứng về máy

Sau khi script chạy thành công, tạo ô mới trong Colab:

```python
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from google.colab import files

archive = Path('/content/lab21_colab_evidence.zip')
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    for folder in ['results', 'adapters', 'data', 'evaluation_backups']:
        for p in Path(folder).rglob('*'):
            if p.is_file():
                z.write(p, p.as_posix())
files.download(str(archive))
```

Đặt ZIP tải về ở thư mục gốc project VS Code và báo assistant tên file.
Assistant sẽ kiểm tra, nhập kết quả, viết các phần báo cáo có căn cứ,
chọn ví dụ định tính từ dự đoán thật và chạy `make verify`.
Nếu không đủ hai ca fine-tune thua baseline, phải báo rõ, không dựng ví dụ.

## 3. Thông tin cá nhân và phản tư

Cần họ tên, MSSV, điều làm bạn ngạc nhiên, phần tốn thời gian nhất và
thử nghiệm bạn muốn làm tiếp. Assistant có thể soạn từ ý bạn cung cấp;
không tự nhận trải nghiệm thay bạn.

Gatekeeper chưa qua vì REPORT.md chưa điền là bình thường ở bước này.
Phán quyết model FAILED vẫn có thể là kết quả lab hợp lệ nếu được phân tích đúng.
NB6 và các phần thưởng là tùy chọn.
