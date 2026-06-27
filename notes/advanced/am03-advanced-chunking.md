# AM03 — Advanced Chunking Strategies

> Sâu hơn [[ai03-chunking]]: các chiến lược chunk hiện đại (semantic, parent-child, late chunking). Chunk quyết định RAG quality nhiều hơn ta tưởng. Liên hệ [[ad06-doc-parsing]], [[ae08-rag-for-code]], [[am01-rag-debugging]].

## Nhắc: vì sao chunk khó
- Chunk **quá nhỏ** → mất ngữ cảnh (câu lẻ vô nghĩa). **Quá to** → loãng (nhiều chủ đề, embedding "trung bình" mờ).
- Cắt sai chỗ → chunk vô nghĩa → retrieve sai ([[am01-rag-debugging]]).
- → Chiến lược chunk = cân **đủ ngữ cảnh** vs **tập trung 1 ý**.

## ⭐ Bảng chiến lược chunking
| Chiến lược | Cách | Ưu / Nhược |
|-----------|------|-----------|
| **Fixed-size** | cắt N token + overlap | đơn giản / cắt giữa ý |
| **Structure-aware** | theo heading/đoạn ([[ai03-chunking]]) | giữ cấu trúc / phụ thuộc format |
| **Semantic** | cắt ở điểm ĐỔI ngữ nghĩa (cosine câu liền kề tụt) | ranh giới tự nhiên / tốn tính |
| **Propositional** | tách thành mệnh đề độc lập (atomic facts) | precision cao / nhiều chunk, tốn |
| **Parent-child** | chunk NHỎ để tìm, trả context CHA | tìm chính xác + context đủ / phức tạp |
| **Late chunking** | embed CẢ doc (long-context) rồi mới cắt embedding | giữ ngữ cảnh toàn doc / cần model long-context |

## ⭐ Semantic chunking
```
chia câu -> embed mỗi câu -> đo cosine câu i vs i+1
   cosine TỤT mạnh = điểm đổi chủ đề -> CẮT ở đó
-> chunk theo ranh giới NGỮ NGHĨA tự nhiên, không cắt giữa ý
```
→ Tốt hơn fixed-size (không cắt ngang ý) nhưng tốn (embed mọi câu). Ngưỡng tụt phải calibrate.

## ⭐ Parent-child (small-to-big) — rất hiệu quả
```
INDEX:    chunk NHỎ (câu/đoạn ngắn) -> embed -> tìm chính xác
RETRIEVE: tìm chunk nhỏ khớp -> nhưng TRẢ VỀ chunk CHA (đoạn lớn chứa nó)
   -> precision của nhỏ + ngữ cảnh của lớn cho LLM đọc
```
→ Giải mâu thuẫn "nhỏ để tìm đúng, to để đủ context": tìm bằng nhỏ, đưa LLM bằng to. Mẫu hình mạnh, phổ biến.

## ⭐ Late chunking (mới)
```
THƯỜNG: cắt chunk TRƯỚC -> embed mỗi chunk RIÊNG (mất ngữ cảnh quanh)
LATE:   embed CẢ doc (model long-context) -> rồi pool embedding theo chunk
   -> mỗi chunk embedding "biết" ngữ cảnh toàn doc -> giải coreference ("nó", "điều này")
```
→ Cần model long-context; giữ ngữ cảnh xa mà chunk riêng lẻ mất.

## Overlap & metadata
- **Overlap** (chồng lấn) giữ liên tục giữa chunk (câu ở ranh giới không mất) — tune ~10-20%.
- **Metadata** mỗi chunk: nguồn, heading, vị trí, parent-id → filter + parent-child + citation.

## Chọn chiến lược
```
doc có cấu trúc rõ (md/heading)  -> structure-aware
văn xuôi dài, đổi chủ đề          -> semantic
cần precision cao + context       -> parent-child (mặc định tốt)
code                              -> theo AST/hàm ([[ae08-rag-for-code]])
có model long-context             -> late chunking
```

## Cạm bẫy
- **Fixed-size cắt giữa ý** → chunk vô nghĩa → structure-aware/semantic.
- **Chunk quá to** → embedding loãng, retrieve mờ → nhỏ hơn / parent-child.
- **Chunk quá nhỏ** → mất ngữ cảnh → overlap / parent-child.
- **Không overlap** → mất câu ở ranh giới → thêm overlap.
- **Quên metadata** → không filter/citation/parent → luôn gắn.
- **Semantic không calibrate ngưỡng** → cắt bừa → tune trên data.
- **Chunk 1 kiểu cho mọi loại doc** → code/bảng/văn xuôi khác nhau → theo loại.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 6 chiến lược + ưu/nhược.
- [ ] Semantic (cắt điểm đổi nghĩa); parent-child (nhỏ tìm, to trả).
- [ ] Late chunking (embed cả doc rồi cắt — giữ ngữ cảnh).
- [ ] Overlap + metadata; chọn theo loại doc.
- [ ] Cạm bẫy: cắt giữa ý, quá to/nhỏ, không overlap.
- 🔭 Tự mò: trong `rag_over_notes.py`, thử **parent-child**: chunk nhỏ (size 300) để index nhưng lưu parent-id (note); khi retrieve chunk nhỏ, trả thêm cả note cha; chạy `rag_eval_harness.py` so với chunk hiện tại → đo recall/độ-đủ-context.

➡️ Tiếp [[am04-hybrid-fusion]] — RRF & fusion (chạy được).
