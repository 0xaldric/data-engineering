# AH02 — Embedding Model Selection & Benchmark ⭐ (có code chạy được)

> Chọn embedding model/cấu hình bằng **SỐ** (như MTEB), không "model nào cũng được". Code: [`embedding_benchmark.py`](../../projects/06-ai-data-engineering/embedding_benchmark.py) — và nó cho một **phát hiện bất ngờ**. Liên hệ [[ab02-rag-eval-harness]], [[ai04-embedding-versioning]], [[ah06-rag-benchmarks]].

## Vì sao chọn embedding quan trọng
- Embedding là **nền** của RAG: vector tệ → mọi thứ sau tệ, không model LLM nào cứu.
- Nhiều lựa chọn: model nào (bge/e5/gte/...), kích thước (384/768/1024 chiều), đa ngữ?, max-length, **query-prefix**, normalize.
- → Phải đo trên **corpus của mình**, không tin leaderboard mù.

## ⭐ MTEB & các chiều đánh giá
**MTEB** (Massive Text Embedding Benchmark): leaderboard công khai xếp hạng embedding qua nhiều task (retrieval, classification, clustering...). Nhưng chọn model còn cân:
| Chiều | Vì sao |
|-------|--------|
| **Chất lượng** (recall/MRR/nDCG) | tìm đúng không |
| **Tốc độ** | embed nhanh? (serving cost — đo được) |
| **Kích thước chiều** | 384 vs 1024 → RAM/latency vector store ([[af04-vector-db-internals]]) |
| **Đa ngữ** | corpus tiếng Việt cần model đa ngữ ([[ac01-multilingual-rag]]) |
| **Max length** | chunk dài có bị cắt? |
| **License/self-host** | dùng được không ([[ad03-privacy-compliance]]) |

## ⭐⭐ Phát hiện BẤT NGỜ (code chạy trên capstone)
Ablation **query-prefix ON vs OFF** (bge khuyến nghị thêm prefix cho query):
```
config        recall@5    MRR
prefix ON        75%     0.490    <- theo "khuyến nghị"
prefix OFF       88%     0.604    <- TỐT HƠN!
```
→ **Prefix OFF thắng** — TRÁI với mặc định bge! Lý do:
- Doc trong index được embed **KHÔNG prefix** (build_index dùng `embed()` thẳng).
- Nội dung **tiếng Việt**, prefix là **tiếng Anh** ("Represent this sentence...") → kéo vector query lệch về "không gian prefix tiếng Anh", xa khỏi doc tiếng Việt không-prefix.
- → **Bài học vàng**: khuyến nghị mặc định của model KHÔNG luôn đúng cho **corpus của bạn**. Phải ĐO. (Phát hiện này gợi ý capstone `embed_query` nên bỏ prefix — một cải tiến thật tìm ra nhờ benchmark.)

## ⭐ Sweep k (cũng đo được)
```
k    recall@k   MRR
1      38%     0.375
3      62%     0.458
5      75%     0.490
10    100%     0.524
```
→ k lớn → recall tăng (lấy nhiều chunk dễ trúng) nhưng MRR tăng chậm (hạng không cải thiện nhiều — cần rerank [[ae07-reranking-deep]]). Tốc độ: ~4ms/câu (1 tiêu chí chọn model).

## Quy trình chọn embedding (đừng tin leaderboard mù)
```
1. Lọc ứng viên từ MTEB (theo task/đa ngữ/kích thước/license)
2. Build golden set RIÊNG trên corpus mình ([[ab02-rag-eval-harness]])
3. Benchmark từng model + cấu hình (prefix/normalize/chunk) -> recall/MRR + tốc độ
4. Chọn theo TRADE-OFF (chất lượng × tốc độ × RAM × đa ngữ), không chỉ điểm cao nhất
5. Đổi model -> re-embed toàn corpus ([[ai04-embedding-versioning]])
```

## Cạm bẫy
- **Tin leaderboard mù** → domain/ngôn ngữ của bạn khác benchmark → đo trên data thật.
- **⭐ Tin "khuyến nghị mặc định"** (prefix) → có thể HẠI corpus của bạn → ablation.
- **Query và doc embed khác cách** (1 có prefix, 1 không) → lệch không gian → nhất quán 2 phía.
- **Chỉ đo chất lượng, quên tốc độ/RAM** → model xịn nhưng chậm/nặng không serve nổi.
- **Quên đa ngữ** → model EN cho corpus Việt rớt ([[ac01-multilingual-rag]]).
- **Đổi model không re-embed** → query mới đập doc cũ → vô nghĩa.

## ✅ "Tự kiểm tra & tự mò"
- [ ] MTEB + các chiều chọn model (chất lượng/tốc độ/chiều/đa ngữ/max-len).
- [ ] ⭐ Phát hiện prefix-OFF > ON trên corpus Việt — vì sao (doc no-prefix + ngôn ngữ).
- [ ] Query/doc phải embed nhất quán (cùng prefix convention).
- [ ] Quy trình: lọc MTEB → golden riêng → benchmark → trade-off → re-embed.
- 🔭 Tự mò: cài model đa ngữ `intfloat/multilingual-e5-small` trong `rag_over_notes.py` (đã ghi sẵn comment ở MODEL_NAME), re-embed, chạy `embedding_benchmark.py` so recall với bge-small + so prefix e5 (e5 dùng "query:"/"passage:" prefix) — xem model đa ngữ + prefix đúng có vượt 88% không. Sửa `embed_query` bỏ prefix xem capstone có lên 88%.

➡️ Tiếp [[ah03-red-teaming]] — red-team hệ AI.
