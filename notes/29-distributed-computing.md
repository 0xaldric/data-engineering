# 29 — Distributed Computing & MapReduce

> Phase 4 mở màn. Mục tiêu: hiểu **vì sao** và **cách** xử lý dữ liệu vượt khả năng một máy.

## Vì sao cần xử lý phân tán?
Khi dữ liệu/tải vượt một máy: RAM không đủ, CPU một máy quá chậm, đĩa một máy quá nhỏ. Hai hướng mở rộng:
- **Scale-up (dọc):** mua máy mạnh hơn. Đơn giản nhưng có **trần** (giá tăng phi tuyến, vẫn 1 điểm hỏng).
- **Scale-out (ngang):** thêm nhiều máy thường (commodity). Rẻ, gần như **vô hạn**, chịu lỗi tốt — nền tảng của big data (Hadoop, Spark). Đánh đổi: **phức tạp** (điều phối, mạng, lỗi cục bộ).

## MapReduce — paradigm nền tảng
Mô hình của Google (2004), gốc của Hadoop. Chia xử lý thành 3 pha chạy **song song trên nhiều node**:
```
Input → [MAP] → (key, value) → [SHUFFLE] gom theo key → [REDUCE] → Output
```
- **Map**: mỗi node xử lý một phần dữ liệu (partition), phát ra cặp `(key, value)`. *Song song hoàn toàn, không cần nói chuyện với node khác.*
- **Shuffle**: gom tất cả value cùng key về cùng một reducer. *Tốn network — đây là pha đắt nhất.*
- **Reduce**: với mỗi key, gộp các value (sum/count/...). *Song song theo key.*

Ví dụ doanh thu theo category (pseudo):
```
MAP:     mỗi dòng đơn  -> (category, line_total)
SHUFFLE: gom mọi line_total theo category
REDUCE:  (category, sum(line_total))
```
Word-count là "hello world" của MapReduce: map `(word, 1)` → reduce `sum`.

## Khái niệm cốt lõi
- **Data partitioning**: chia dữ liệu thành nhiều mảnh để xử lý song song. Chọn **khoá phân vùng** tốt để tải đều (tránh skew).
- **Data locality**: đưa **tính toán tới chỗ dữ liệu** (chạy map trên node đang giữ block) thay vì kéo dữ liệu qua mạng — giảm I/O mạng.
- **Fault tolerance**: node hỏng giữa chừng → re-chạy task đó trên node khác (nhờ dữ liệu được nhân bản + task idempotent).
- **Shuffle là kẻ thù số 1 của hiệu năng**: mọi tối ưu big data xoay quanh việc **giảm shuffle** (xem [[31-partitioning-shuffle]]).

## HDFS & Object Storage
Dữ liệu lớn lưu ở đâu?
- **HDFS** (Hadoop Distributed File System): chia file thành **block** (vd 128MB), **nhân bản 3 lần** trên nhiều node → chịu lỗi + cho data locality. Kiểu cũ, chạy on-prem.
- **Object storage** (S3, GCS, Azure Blob): chuẩn **hiện đại**. Tách hẳn **storage khỏi compute** → co giãn độc lập, rẻ, bền (11 số 9 độ bền). Hầu hết lakehouse/cloud dùng cái này. Đánh đổi: không có data locality thật (đọc qua mạng), nên cần file format tốt ([[09-file-formats]]) + table format ([[34-delta-lake]]).

## CAP Theorem (nhắc lại, xem [[20-nosql]])
Hệ phân tán khi có phân vùng mạng (P) chỉ đạt 2/3: **C**onsistency, **A**vailability, **P**artition tolerance. Vì mạng luôn có thể đứt → chọn **CP** (nhất quán, có thể từ chối) hoặc **AP** (luôn phục vụ, chấp nhận tạm cũ).

## ⚠️ Cạm bẫy
- **Data skew**: một key chiếm phần lớn dữ liệu → một reducer làm mãi, các reducer khác chờ. (Cách xử lý ở [[31-partitioning-shuffle]].)
- **Small files**: hàng triệu file nhỏ → overhead metadata khổng lồ ([[33-spark-tuning]]).
- Nghĩ "song song là luôn nhanh" — sai nếu shuffle/skew/IO mạng lấn át.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Phân biệt scale-up vs scale-out, ưu/nhược.
- [ ] Vẽ 3 pha MapReduce cho bài "doanh thu theo category".
- [ ] Giải thích vì sao shuffle đắt và data locality giúp gì.
- [ ] HDFS vs object storage (tách compute/storage).
- 🔭 *Tự mò:* viết word-count bằng MapReduce thuần Python (chia list thành N partition, map, gom dict theo key, reduce); rồi nghĩ xem Spark làm gì khác.

➡️ Tiếp: [[30-spark-model]] — Spark hiện đại hoá MapReduce thế nào.
