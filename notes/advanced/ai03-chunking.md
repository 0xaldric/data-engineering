# AI03 — Chunking Strategies sâu

> Chunking là bước transform quan trọng nhất của RAG — quyết định chất lượng retrieval. Sâu hơn [[k05-vector-rag-deep]], áp vào [[ai02-rag-capstone-writeup]].

## Vì sao chunking quan trọng
LLM/embedding có **giới hạn context** + retrieval trả về cả chunk. Chunk sai →:
- Quá **to**: nhiều chủ đề lẫn lộn → embedding "trung bình hoá" → kém phân biệt; tốn context.
- Quá **nhỏ**: mất ngữ cảnh → chunk không tự đứng vững (thiếu chủ ngữ/định nghĩa).
→ Chunking tốt = mỗi chunk **một ý mạch lạc, tự đứng được**.

## Các chiến lược (từ thô đến tinh)
| Chiến lược | Cách | Ưu / Nhược |
|-----------|------|-----------|
| **Fixed-size** | cắt mỗi N token/char + overlap | đơn giản, nhanh; cắt giữa câu/ý |
| **Sentence/paragraph** | cắt theo câu/đoạn | tự nhiên hơn; đoạn dài vẫn cần cắt |
| **Structure-aware** ⭐ | theo heading/section (Markdown ##, HTML, code block) | giữ ngữ cảnh logic; cần parser cho format |
| **Semantic** | cắt khi nghĩa "đổi" (embedding các câu, tách khi cosine giảm) | mạch lạc nhất; tốn compute (embed để chia) |
| **Parent-child / small-to-big** | embed chunk NHỎ (chính xác retrieval), trả chunk CHA (đủ ngữ cảnh cho LLM) | cân chính xác vs ngữ cảnh; phức tạp |
| **Late chunking** | embed cả tài liệu rồi mới chia (giữ ngữ cảnh toàn cục trong mỗi chunk) | mới, cần model long-context |

## ⭐ Overlap
Chồng lấn giữa chunk kề nhau (vd 10–20%) → ý ở **ranh giới** không bị cắt mất, xuất hiện trong cả 2 chunk → retrieval bắt được dù query rơi vào ranh giới. Trade-off: dư thừa (lưu/embed nhiều hơn).

## Chunk size — chọn thế nào
- Phụ thuộc: loại tài liệu (code/prose/table khác nhau), embedding model (context limit), use case.
- Quy tắc thực dụng: prose ~512–1024 token; code theo function/class; bảng giữ nguyên hàng+header.
- **Đo, đừng đoán**: thử vài size → đo recall@k ([[ai05-retrieval-eval]]) → chọn.

## Chunk metadata (đừng quên)
Mỗi chunk kèm: nguồn (file/url), heading/section, vị trí, **doc_id** (cho incremental/delete), timestamp, model. → filter (metadata + vector — [[k05-vector-rag-deep]]), incremental ([[ai02-rag-capstone-writeup]]), citation (chỉ nguồn cho LLM).

## Snippet (structure-aware, như capstone)
```python
# cắt theo heading Markdown, section dài thì cắt size + overlap
parts = re.split(r"(?m)^(#{1,4}\s+.*)$", text)   # tách theo dòng heading
for heading, body in sections:
    if len(body) <= MAX:
        chunks.append({"heading": heading, "text": f"{heading}\n{body}"})
    else:
        start = 0
        while start < len(body):
            chunks.append({"heading": heading, "text": f"{heading}\n{body[start:start+MAX]}"})
            start += MAX - OVERLAP        # overlap
```
Mẹo: nhét **heading vào text chunk** → embedding biết ngữ cảnh section (capstone làm vậy).

## ⚠️ Cạm bẫy
- Fixed-size cắt giữa câu/code → chunk vô nghĩa.
- Không overlap → mất ý ở ranh giới.
- Chunk không kèm metadata → không incremental/citation được.
- Một size cho mọi loại tài liệu (code vs prose vs table khác nhau).
- Không đo recall → chọn size theo cảm tính.

## ✅ "Tự mò"
🔭 Trong capstone, đổi `MAX_CHUNK_CHARS` (vd 600 vs 1500) + `OVERLAP_CHARS`, re-index, chạy eval xem recall@k đổi thế nào → chọn size tốt nhất bằng SỐ.

➡️ Tiếp: [[ai04-embedding-versioning]].
