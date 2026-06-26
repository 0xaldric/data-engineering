# G07 — Data Structures & Algorithms cho DE

> Không phải leetcode — mà các cấu trúc/giải thuật **thực sự chạy bên dưới** Spark/DB/warehouse. Hiểu chúng = hiểu vì sao hệ thống nhanh/chậm.

## Hashing & Hash Join ⭐
- **Hash table**: ánh xạ key→value O(1) trung bình. Nền của `GROUP BY`, `DISTINCT`, hash join.
- **Hash join**: build hash table từ bảng nhỏ (theo join key) → probe bằng bảng lớn. O(n+m). Là chiến lược join phổ biến nhất khi không sort sẵn ([[32-joins-catalyst]]).
- **Hash partitioning**: `hash(key) % N` chia dữ liệu vào N partition/node → cùng key cùng nơi (shuffle, Kafka partition — [[31-partitioning-shuffle]], [[46-kafka-core]]).
- **Surrogate key bằng hash** (dbt generate_surrogate_key — [[d02-dbt-advanced]]).

## Sorting & External Sort
- **External merge sort** ⭐: sort dữ liệu **lớn hơn RAM** — chia thành chunk vừa RAM, sort từng chunk, ghi đĩa, **merge** các chunk đã sort. Đây là cách DB/Spark sort TB dữ liệu.
- **Sort-merge join**: sort 2 bảng theo key rồi merge tuyến tính — dùng khi dữ liệu lớn không broadcast được ([[32-joins-catalyst]]).
- `ORDER BY` lớn → có thể **spill** ra đĩa (external sort) — thấy trong Spark UI ([[d01-spark-internals]]).

## Merge & Two-pointer
Merge 2 luồng đã sort (merge sort, sort-merge join, LSM compaction). Two-pointer cho gaps/overlap (mutually exclusive ranges).

## ⭐ B-tree vs LSM-tree (storage engine — câu hỏi sâu hay gặp)
Hai cách DB lưu/index dữ liệu:
| | **B-tree** | **LSM-tree** |
|--|-----------|--------------|
| Cấu trúc | cây cân bằng, update tại chỗ | memtable (RAM) + SSTable (đĩa, immutable) + compaction |
| Đọc | nhanh (point lookup) | chậm hơn (đọc nhiều SSTable + bloom filter giúp) |
| Ghi | random write (chậm hơn) | **sequential write** (nhanh, append) |
| Dùng | Postgres/MySQL (OLTP read-heavy) | Cassandra/RocksDB/HBase (write-heavy), Kafka-ish |
- **LSM**: ghi vào memtable (RAM) → flush thành SSTable (immutable, sorted) → **compaction** gộp SSTable (giống compaction small files!). Ghi nhanh nhờ sequential; đọc dùng **bloom filter** ([[g08-probabilistic-ds]]) để bỏ qua SSTable không chứa key.
- → Chọn theo workload: read-heavy → B-tree; write-heavy → LSM.

## Heap cho Top-K
Tìm top-K phần tử (leaderboard, top sản phẩm) bằng **min-heap** size K: duyệt 1 lần O(n log k), không cần sort toàn bộ. SQL `ORDER BY ... LIMIT K` thường dùng heap (top-K) thay full sort ([[a05-sql-interview-2]] Pareto).

## Trie / Inverted index (search)
- **Inverted index**: word → danh sách document chứa (Elasticsearch, full-text search — [[g03-case-log-analytics]]).
- Trie cho prefix/autocomplete.

## Vì sao DE cần biết
- Hiểu **vì sao** join/sort/groupBy đắt (hash/sort/spill) → tối ưu đúng chỗ.
- Chọn storage engine (B-tree vs LSM) theo workload.
- Đọc plan/Spark UI có ý nghĩa.
- Trả lời phỏng vấn "vì sao X chậm".

## ⚠️ Cạm bẫy
- Nghĩ index luôn nhanh (LSM đọc cần nhiều SSTable; B-tree ghi chậm).
- Sort/distinct/count(distinct) trên dữ liệu lớn → spill/shuffle đắt (cân nhắc approx — [[g08-probabilistic-ds]]).
- Hash collision / skew (một key quá nhiều → hash partition lệch).

## ✅ "Tự mò"
🔭 Giải thích bằng lời: vì sao Cassandra ghi nhanh (LSM sequential) nhưng đọc cần bloom filter? Vì sao `ORDER BY ... LIMIT 10` rẻ hơn sort toàn bộ (heap top-K)?

➡️ Tiếp: [[g08-probabilistic-ds]].
