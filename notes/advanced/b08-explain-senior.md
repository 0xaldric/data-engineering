# B08 — "Explain like a senior": 10 khái niệm hay bị đào sâu

> Phỏng vấn senior thường đào "vì sao" tới tận gốc. Đây là cách trả lời **sâu** 10 khái niệm cốt lõi — không chỉ định nghĩa mà cả nguyên nhân & đánh đổi.

### 1. Idempotency
*Định nghĩa nông:* chạy lại ra cùng kết quả. *Sâu:* trong hệ phân tán, **mọi thứ sẽ chạy lại** (retry do lỗi tạm thời, backfill, scheduler restart, at-least-once delivery). Không idempotent → nhân đôi/sai âm thầm. Đạt bằng: thao tác **theo khoá xác định** (partition overwrite theo logical_date, upsert/MERGE theo unique_key), không append mù, atomic publish. Đây là **điều kiện nền** cho retry & exactly-once. ([[40-pipeline-patterns]])

### 2. Exactly-once
*Sâu:* "exactly-once processing" thường = **at-least-once delivery + idempotent state/sink**. Kafka EOS dùng idempotent producer + transactions cho luồng Kafka→Kafka; nhưng sink ngoài (DB/lake) vẫn cần idempotency phía sink. "Exactly-once" tuyệt đối end-to-end rất khó; thực tế = at-least-once + dedup theo key. ([[47-kafka-consumers]])

### 3. Shuffle
*Sâu:* shuffle = phân phối lại dữ liệu giữa node để gom theo key (groupBy/join/distinct). Đắt vì **3 chi phí**: network I/O, disk I/O (ghi shuffle files), serialization. Tạo ranh giới stage. 90% tối ưu Spark = giảm shuffle (lọc/bỏ cột sớm, broadcast, tránh wide không cần). ([[31-partitioning-shuffle]])

### 4. SCD Type 2
*Sâu:* giữ lịch sử dimension để **báo cáo quá khứ đúng**. Cùng natural key → nhiều phiên bản, mỗi cái 1 **surrogate key** + effective_from/to + is_current. Fact trỏ surrogate key → mỗi giao dịch gắn đúng phiên bản tại thời điểm đó (vd doanh thu "theo quốc gia khách lúc mua"). Không có SCD2 → gán hết về giá trị hiện tại = sai lịch sử. ([[18-scd]])

### 5. Partitioning
*Sâu:* đơn vị **song song** (Spark: 1 partition=1 task) và **cắt dữ liệu quét** (lake: partition pruning). Quá ít → không tận dụng core / partition to → spill. Quá nhiều → overhead + small files. Chọn cột partition theo **cột hay lọc**, lực lượng vừa phải. Khác index OLTP — đây là đòn bẩy OLAP. ([[31-partitioning-shuffle]], [[14-indexing]])

### 6. CAP Theorem
*Sâu:* hệ phân tán khi **có** partition mạng (P — luôn có thể xảy ra) chỉ đạt 2/3. Nên thực chất chọn **CP** (ưu tiên nhất quán, có thể từ chối phục vụ) vs **AP** (luôn phục vụ, chấp nhận dữ liệu tạm cũ). Liên hệ ACID (CP-ish) vs BASE (AP-ish). Không phải "chọn 2 bất kỳ" mà là đánh đổi C vs A khi P xảy ra. ([[20-nosql]])

### 7. ELT vs ETL
*Sâu:* ELT thắng vì warehouse cloud **tách compute/storage**, mạnh & rẻ → nạp thô rồi transform bằng SQL (dbt) ngay trong warehouse. Lợi: giữ raw (replay), transform versioned/tested, dùng sức mạnh warehouse. ETL vẫn hợp khi cần xử lý nặng/đặc thù trước khi nạp hoặc warehouse yếu. ([[21-warehouse-dbt]])

### 8. Data Lineage
*Sâu:* bản đồ dòng chảy dữ liệu (table & column level). Giá trị: **impact analysis** (đổi cột nguồn → biết chính xác cái gì hỏng), **root cause** (dashboard sai → lần ngược), **triage incident** (nguồn lỗi → ai ảnh hưởng), audit PII (GDPR). Khi scale (nghìn bảng) không có lineage = mù. ([[63-lineage-catalog]])

### 9. Backfill
*Sâu:* chạy lại pipeline cho khoảng quá khứ (thêm cột mới, sửa bug, nguồn bổ sung dữ liệu cũ). An toàn **chỉ khi idempotent** — mỗi run xử lý đúng partition của logical_date của nó, ghi đè không nhân đôi. Đây là lý do Airflow nghĩ theo data_interval, không `now()`. ([[39-airflow-scheduling]])

### 10. Watermark
*Sâu:* trong streaming, event time ≠ processing time (data tới trễ). Watermark = "ta chờ data trễ tối đa T"; sau đó **đóng cửa sổ** + chốt kết quả + bỏ data trễ hơn + **dọn state cũ** (tránh phình RAM vô hạn). Đánh đổi: T lớn = chính xác hơn nhưng trễ kết quả + tốn RAM; T nhỏ = nhanh nhưng bỏ sót data trễ. ([[49-stream-processing]])

## Mẹo trả lời "sâu"
Mỗi khái niệm theo cấu trúc: **định nghĩa → vì sao tồn tại (vấn đề nó giải) → cách hoạt động → đánh đổi → ví dụ thực tế**. Người phỏng vấn senior tìm "hiểu trade-off", không phải thuộc lòng.

## ✅ "Tự mò"
🔭 Tự giải thích 10 cái trên thành tiếng (như đang dạy người khác) ≤ 2 phút mỗi cái, có nêu trade-off + 1 ví dụ.

➡️ Tiếp: [[00-moduleB-summary]].
