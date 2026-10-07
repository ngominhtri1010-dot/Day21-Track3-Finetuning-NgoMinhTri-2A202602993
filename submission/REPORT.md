# Lab 21 — Evaluation Report

**Họ tên:** Ngô Minh Trí · **MSSV:** 2A202620993 · **Ngày:** 2026-10-07

## 1. Bài toán và cấu hình

Tôi dùng corpus mặc định gồm 250 ticket CSKH tiếng Việt, với đầu ra JSON bốn trường
intent, urgency, product và sentiment. Đây là tác vụ hẹp, dễ kiểm tra từng trường,
phù hợp để so sánh prompt engineering với fine-tuning trong phạm vi lab.
Model là `unsloth/Qwen3.5-4B`, tier T4, GPU Tesla T4 (ảnh runtime báo 14,6 GB),
precision fp16. Chọn cấu hình mặc định giúp chạy trên GPU Colab và giữ phép đối chứng
nhất quán, thay vì đồng thời thay model và hyperparameter.

Train/val là 225/25 mẫu, seed 42. Batch thiết bị 1, gradient accumulation 16,
batch hiệu dụng 16; 2 epochs và ngân sách 30 optimizer steps cho cả bốn run.
Tập đánh giá đầy đủ gồm 50 target và 15 regression.

`results/token_stats.json` ghi mean 93,1, p95 98, max 101 token và đề xuất
`max_length=256`. Lần chạy giữ `max_length=1024` của tier T4 để tái lập cấu hình
mặc định; đó là giới hạn trên lớn hơn nhu cầu đo được, không phải độ dài đã tối ưu.
Các mẫu đo được đều ngắn hơn giới hạn nên không cần cắt tại 1024.

## 2. Bằng chứng template và loss mask

`results/template_check.json` ghi `ok=true`, giữ cả thẻ mở và nội dung `<think>`.
Điều này chứng minh template giữ trace trong ví dụ kiểm tra; không chứng minh
model sau train duy trì năng lực reasoning trên mọi đầu vào.

Mask `assistant-only`: 39/94 token được giám sát, `supervised_fraction=0.4149`.
`answer_is_supervised=true`, `question_is_masked=true`. Phần tính loss giải mã:

```text
</think>

{"intent": "doi_tra", "urgency": "trung_binh", "product": "balo laptop", "sentiment": "trung_tinh"}<|im_end|>
```

Thẻ đóng `</think>` cũng nằm trong phần giám sát ở ví dụ này. Câu hỏi và system
prompt nằm trong phần mask. Đây là số đo T4 trong ZIP; kết quả CPU trước đó được
lưu riêng trên máy và không dùng thay cho số đo T4.

## 3. Trình tự baseline và kết quả

Baseline ban đầu được đo **trước train trên 8 mẫu mỗi tập**: (a) target 0,0000,
regression 0,7500; (b) target 0,6875, regression 0,7500. Bản gốc giữ ở
`submission/evidence/baselines_before_training.json`.
Sau train, chạy lại NB2 và NB5 trên toàn bộ tập đánh giá với các adapter đã lưu.
Do đó không tuyên bố baseline đầy đủ được đo trước train. Trình tự này có giới hạn
so với yêu cầu rubric về baseline trước train và được khai báo ở
`results/evaluation_provenance.json`. Không thay prompt hay corpus để làm FT thắng.
SHA prompt tối ưu ở hai bản đều là `719e74d3b6232053`; gatekeeper kiểm tra với mã gốc.

| Run | target | regression | format | latency ms |
|---|---:|---:|---:|---:|
| (a) base + naive prompt | 0.0000 | 0.7911 | 0.0000 | 3194.1 |
| (b) base + optimized prompt | 0.7650 | 0.7911 | 1.0000 | 1019.8 |
| (c) LoRA fine-tune | 0.9700 | 0.6111 | 1.0000 | 1354.4 |

(b) mạnh hơn (a) về target và format, không cải thiện regression. Target là độ đúng
trung bình của bốn trường JSON, không phải tỷ lệ toàn bộ ticket đúng hoàn toàn.
Regression là keyword recall trên các câu hỏi phổ thông. Latency phụ thuộc runtime,
không nên diễn giải như benchmark cố định cho triển khai.

## 4. Đối chứng cấu hình

| Run | Vị trí | r | Tham số trainable | LR | Final loss | Target | Train s | Peak VRAM GB |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| correct | text-linear | 16 | 32,464,896 | 0.0001 | 0.6273 | 0.970 | 390.2 | 8.78 |
| attn_only | attn-only | 283 | 32,456,704 | 0.0001 | 0.5386 | 0.970 | 257.1 | 8.79 |
| wrong_lr | text-linear | 16 | 32,464,896 | 1e-05 | 1.5702 | 0.000 | 383.9 | 8.78 |
| qlora | text-linear | 16 | 32,464,896 | 0.0001 | 0.7058 | 0.940 | 451.7 | 3.86 |

### 4.1. Vị trí và rank

`attn_only` có 32.456.704 tham số so với 32.464.896 của `correct`, lệch khoảng
0,0252%; rank 283 bù cho ít vị trí gắn hơn. Cả hai đạt target 0,970, trong khi
attn_only có final loss thấp hơn (0,5386 so với 0,6273). Vì vậy thứ tự theo loss
không tạo ra thứ tự theo target: loss thấp hơn chưa chứng minh năng lực tác vụ tốt
hơn. Trong một lần chạy trên corpus này, attention-only với ngân sách khớp đã hòa;
không đủ bằng chứng nói text-linear luôn tốt hơn hoặc rank lớn luôn thắng.

### 4.2. Learning rate

`wrong_lr` giảm LR từ 1e-4 xuống 1e-5, giữ vị trí, rank, số tham số và 30 steps.
Final loss tăng lên 1,5702, target và format đều bằng 0. Điều này phù hợp với việc
LR nhỏ chưa học được định dạng trong ngân sách hiện tại, nhưng không chứng minh
LR ấy sẽ thất bại nếu tăng số steps. ZIP chỉ chứa final loss, không có toàn bộ
đường loss; không thể mô tả hình dạng hay tốc độ hội tụ từng step như đã đo được.
Nhìn một con số loss mà bỏ qua LR và khả năng sinh JSON có thể dẫn đến kết luận
sai rằng kiến trúc adapter không phù hợp.

### 4.3. QLoRA

QLoRA giảm peak VRAM từ 8,78 xuống 3,86 GB: tiết kiệm 4,92 GB, khoảng 56,0%.
Đổi lại target giảm 0,030, thời gian train tăng từ 390,2 lên 451,7 giây
(khoảng 15,8%) và latency tăng từ 1354,4 lên 1753,3 ms (khoảng 29,4%).
Format vẫn đạt 1,000. NB5 đánh giá adapter QLoRA với base 4-bit tương ứng.
Số đo này ủng hộ ưu tiên fp16 khi đủ VRAM ở cấu hình đang xét, nhưng chưa đủ để
khái quát rằng QLoRA luôn không nên dùng: tiết kiệm bộ nhớ là lợi ích rõ ràng,
và đây chỉ là một lần chạy trên một tác vụ nhỏ.

## 5. Phán quyết và diễn giải

**Cổng hồi quy: FAILED.** Target delta +0,205; regression delta −0,180;
`valid_trace_rate=0,0000`. Ngưỡng regression cho phép giảm tối đa 0,020.

Fine-tune học tốt tác vụ phân loại ticket: target tăng từ 0,765 lên 0,970,
format giữ ở 1,000 dù chỉ dùng prompt ngắn. Tuy nhiên, lợi ích chuyên môn hóa
đi kèm giảm khả năng trả lời nhóm câu hỏi phổ thông từ 0,7911 xuống 0,6111.
Mức giảm 0,180 vượt ngưỡng 0,020 nên chưa đủ điều kiện triển khai theo cổng của lab.
Không nới ngưỡng hay sửa eval để đổi FAILED thành PASSED. Quên thảm họa là một
khả năng cần kiểm tra, chứ số đo keyword recall đơn lẻ chưa xác định đầy đủ nguyên
nhân. Bước thử tiếp hợp lý là trộn 1–5% dữ liệu replay phổ thông và đo lại với
cùng ngân sách, đồng thời xem câu trả lời regression cụ thể để phân biệt sai nội
dung với thay đổi cách diễn đạt. Valid trace rate bằng 0 cũng không tự chứng minh
reasoning collapse vì dữ liệu train mặc định là JSON triage, không phải corpus
reasoning trace. Kết luận hiện tại là giữ baseline prompt cho nhu cầu tổng quát,
và chưa deploy adapter này khi yêu cầu giữ năng lực phổ thông.

## 6. Định tính và giới hạn yêu cầu ca thua

So toàn bộ 50 ticket bằng cùng hàm `triage_field_accuracy`: FT thắng (b) ở 33 mẫu,
hòa 17 mẫu, thua 0 mẫu. Vì vậy chưa đáp ứng yêu cầu rubric ≥2 ca FT thua baseline
trên target. Các ca sai dưới đây là **hòa cùng sai**, không gọi là FT thua baseline.
Không dựng ca thua hay thay tập eval sau khi xem kết quả.
Bảng dùng chỉ số i bắt đầu từ 0 trong dữ liệu và ghi trường quyết định để dễ đọc;
dự đoán và nhãn đầy đủ nằm trong hai file `*_predictions_full.json`.

| i | Ticket rút gọn | Trường và nhãn đúng | (b) | FT | Nhận xét |
|---|---|---|---|---|---|
| 0 | Chuột không dây; Cho tôi trả lại; Gấp | intent=doi_tra | hoan_tien | doi_tra | FT thắng, sửa intent |
| 1 | Ốp lưng; Hoàn tiền; Sớm nhé | urgency=trung_binh | cao | trung_binh | FT thắng, sửa urgency |
| 4 | Đèn bàn LED; Vỡ khi nhận; Shop xem giúp | sentiment=trung_tinh | tieu_cuc | trung_tinh | FT thắng, sửa sentiment |
| 3 | Bình giữ nhiệt; Chưa thấy tiền; Khi nào tiện | urgency=thap | trung_binh | trung_binh | Hòa cùng sai, mỗi bên 0,75 |
| 12 | Áo khoác gió; Bị lỗi; Khi nào tiện | urgency=thap | trung_binh | trung_binh | Hòa cùng sai, mỗi bên 0,75 |

Hai ca lỗi này cùng bỏ sót ý mức khẩn cấp thấp trong “Khi nào tiện”. Đó là vùng
cần xem lại dữ liệu và khả năng phân biệt urgency, dù FT vượt baseline về điểm tổng.
Cổng regression cho thấy một loại thất bại khác ở mức tập dữ liệu; không suy ra
hai ca thua target từ điểm regression tổng hợp.

## 7. Kết luận và điều cần kiểm chứng

Tôi chưa nên deploy bản fine-tune này cho hệ thống vừa phân loại ticket vừa trả lời
câu hỏi phổ thông. Mức tăng target là đáng kể, nhưng cổng hồi quy đã phát hiện một
đánh đổi mà chỉ nhìn loss huấn luyện hoặc điểm ticket sẽ bỏ qua. Prompt tối ưu cũng
là đối thủ mạnh: nó đạt định dạng JSON đầy đủ mà không cần huấn luyện, và giữ điểm
regression tốt hơn adapter. Do đó quyết định triển khai phải xuất phát từ yêu cầu
nghiệp vụ và năng lực cần bảo toàn, không chỉ từ việc đã train thành công.

Phép đối chứng cho thấy learning rate là đòn bẩy rõ nhất trong ngân sách hiện tại:
giảm một bậc làm model mất khả năng sinh đúng định dạng trên tập target. Vị trí gắn
adapter chưa tạo chênh lệch target khi ngân sách tham số được khớp, mặc dù loss khác
nhau. QLoRA đổi bộ nhớ lấy thời gian và một phần điểm tác vụ; việc chọn nó cần xét
ràng buộc VRAM thực tế. Loss mask đúng là điều kiện nền tảng để các phép so sánh
có ý nghĩa, nhưng lab này chưa làm đối chứng mask để lượng hóa riêng tác động của
nó. Corpus nhỏ và sinh theo mẫu cũng hạn chế khả năng suy rộng sang ticket thật.

Ba điều rút ra từ số đo:
1. Loss 0,5386 thấp hơn 0,6273 nhưng hai adapter vẫn hòa target 0,970.
2. Target tăng 0,205 không đủ bù cho regression giảm 0,180 theo cổng đã đặt.
3. Full eval và baseline trước train là hai yêu cầu khác nhau; phải lưu và khai báo
   đúng trình tự thay vì thay file rồi coi như baseline đầy đủ đã có từ đầu.

Nếu có thêm hai giờ, hướng thử đề xuất là replay phổ thông với tỷ lệ nhỏ, giữ
nguyên eval/prompt, đóng băng baseline đầy đủ trước lần train mới, và đo lại cả
bốn nhóm. Trong quá trình làm, ô 3 chạy lâu và ban đầu tôi chưa hiểu vì sao.
Tôi đã hỏi về vai trò của Colab, GPU, API key và sự khác nhau giữa viết code với
chạy thực nghiệm. Phần phản tư cụ thể được ghi trong `submission/REFLECTION.md`.

## Phụ lục và bằng chứng

Chưa làm NB6 hoặc các bonus B1–B5. AI assistant hỗ trợ kiểm tra môi trường,
chuẩn bị script đánh giá đầy đủ, nhập dữ liệu, tính bảng so sánh và soạn báo cáo.
Số liệu lấy từ artifacts thật; người nộp cần đọc, hiểu và xác nhận phần diễn giải.
Baseline trước train chỉ có 8 mẫu và thiếu hai ca thua target là giới hạn còn lại.
