# AJ04 — Next-gen Vector Search: Matryoshka & Binary Quant ⭐ (có code chạy được)

> Nén vector để vừa RAM ở scale tỉ-vector, giữ recall: **Matryoshka** (cắt chiều) + **binary quantization** (1 bit/chiều). Code đo trade-off thật: [`vector_compression.py`](../../projects/06-ai-data-engineering/vector_compression.py). Sâu hơn [[af04-vector-db-internals]], [[ab07-vector-search-opt]].

## Vấn đề: RAM ở scale
- 1 tỉ vector × 384 chiều × 4 byte = **1.5 TB RAM** → không khả thi ([[aa10-llmops]]).
- Cần **nén** vector mà giữ recall đủ → 2 kỹ thuật hiện đại.

## ⭐ Matryoshka Embedding (cắt chiều)
```
ý tưởng: train embedding sao cho PREFIX vector cũng dùng được
   vector 768 chiều -> dùng 768 (đầy đủ) HOẶC 256 HOẶC 64 (cắt) tuỳ ngân sách
   -> 1 model, nhiều "kích thước" — như búp bê Matryoshka lồng nhau
```
- Cho phép **chọn chiều lúc chạy**: tìm thô bằng 64 chiều (rẻ) → rerank bằng full (chính xác).
- ⚠️ Chỉ hoạt động tốt nếu model **được train kiểu Matryoshka** (OpenAI text-embedding-3, nomic, một số e5). Cắt model thường → mất nhiều hơn.

## ⭐ Binary Quantization (1 bit/chiều)
```
vector float32 -> dấu mỗi chiều: >0 -> 1, <=0 -> 0  -> chuỗi BIT
so sánh: Hamming distance (đếm bit khác) thay cosine -> RẤT nhanh (XOR + popcount)
RAM: 384 float (1536B) -> 384 bit (48B) -> /32!
```
→ Nhanh + nhẹ kinh ngạc. Thường: binary để **lọc thô top-N** → rerank bằng vector gốc ([[ae07-reranking-deep]]).

## ⭐⭐ Kết quả thật (đo trên capstone — BẤT NGỜ)
```
dim    recall@5   bytes/vec
384      88%       1536B   (đầy đủ)
256     100%       1024B   (cắt nhẹ — thậm chí tốt hơn, golden nhỏ nên nhiễu)
128      75%        512B
 64      62%        256B   (cắt sâu -> tụt)
binary   88%         48B   (/32 RAM mà GIỮ recall!)
```
**Phát hiện**:
1. **Binary quant giữ 88% recall ở 1/32 RAM** — cực kỳ đáng giá ở corpus này! (Hamming trên 384 bit đủ phân biệt.)
2. **Cắt 256 chiều OK** (bge không phải Matryoshka mà vẫn ổn ở mức vừa); **cắt 64 tụt** (quá tay).
3. → **Trade-off RAM⇄recall KHÔNG đoán được** — lại bài học "ĐO trên data của bạn" ([[ah02-embedding-benchmark]], [[ag04-drift-detection]]).

## ⭐ Mẫu hình production: nén để LỌC + rerank để ĐÚNG
```
triệu/tỉ vector ─> [binary/cắt chiều] lọc nhanh top-100 (rẻ RAM)
              ─> [vector gốc] rerank top-100 -> top-10 (chính xác)
=> RAM thấp (đa số ở dạng nén) + recall cao (rerank bù phần mất)
```
→ Cùng tư duy IVF-PQ + rerank ([[af04-vector-db-internals]]): coarse rẻ → fine chính xác.

## Cạm bẫy
- **Cắt chiều model KHÔNG Matryoshka quá sâu** → recall sập (64 chiều: 62%) → đo trước.
- **Binary/nén mà không rerank** → mất phần chính xác cuối → rerank vector gốc top-N.
- **Giả định nén = luôn tụt** → SAI (binary giữ 88% đây) → đo, đừng đoán.
- **Giả định nén = luôn an toàn** → cũng SAI (64 chiều tụt) → đo cả hai chiều.
- **Golden nhỏ** → số nhiễu (256 ra 100%) → golden đủ lớn để tin.
- **Quên Hamming cần phần cứng** → popcount nhanh trên CPU/GPU hiện đại (tận dụng).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vấn đề RAM ở tỉ-vector → cần nén.
- [ ] Matryoshka: prefix vector dùng được (cần train đúng kiểu).
- [ ] Binary quant: dấu→bit, Hamming, /32 RAM.
- [ ] ⭐ Đo thật: binary giữ 88%, cắt 64 tụt → trade-off phải ĐO.
- [ ] Mẫu hình: nén lọc thô → rerank vector gốc.
- 🔭 Tự mò: sửa `vector_compression.py` thêm **binary + rerank**: lọc top-20 bằng Hamming rồi rerank 20 cái đó bằng cosine vector gốc → đo recall@5 (kỳ vọng bù lại phần mất); thử `int8` quantization (chia thang [-1,1] thành 256 mức) so với binary.

➡️ Tiếp [[aj05-case-healthcare-ai]] — case study y tế.
