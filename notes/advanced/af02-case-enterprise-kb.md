# AF02 — Case Study: Enterprise Knowledge Assistant (multi-source + permissions)

> Thiết kế RAG nội bộ doanh nghiệp: nhiều nguồn (Confluence/Drive/Slack/DB), **phân quyền** (mỗi người chỉ thấy doc được phép), nhiều nguồn cập nhật khác nhau. Thách thức lớn nhất: **permission-aware retrieval**. Liên hệ [[ac06-kb-freshness]], [[ad03-privacy-compliance]], [[aa03-rag-production]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: nhân viên hỏi tự nhiên → trả lời từ tài liệu nội bộ, **chỉ những gì họ được xem**.
- **Nguồn**: Confluence, Google Drive, Slack, Notion, DB nội bộ — mỗi nguồn quyền riêng.
- **Ràng buộc cứng**: **KHÔNG được rò** doc ngoài quyền (vd nhân viên thấy lương sếp) — đây là yêu cầu sống còn.
- **Quy mô**: triệu doc, nghìn nhân viên, quyền phức tạp (theo nhóm/dự án/cấp).

## 2. ⭐⭐ Permission-aware retrieval (vấn đề cốt lõi)
RAG thường bỏ qua quyền → rò data. Phải nhúng quyền vào retrieval:
```
SAI: retrieve top-k theo cosine -> trả (có thể lộ doc cấm)
ĐÚNG: retrieve top-k VỚI filter quyền user -> chỉ doc user được xem
```
| Cách | Mô tả | Đánh đổi |
|------|-------|----------|
| **Pre-filter** | lọc theo ACL user TRƯỚC/TRONG vector search ([[ab07-vector-search-opt]]) | chính xác, an toàn; cần index hỗ trợ metadata filter |
| **Post-filter** | retrieve rồi bỏ doc ngoài quyền | rủi ro: lọc xong < k; vẫn phải lấy dư |
| **Per-group index** | mỗi nhóm quyền 1 partition | cách ly mạnh; phức tạp khi quyền chồng |
→ **Pre-filter theo ACL** là chuẩn: mỗi chunk mang metadata `allowed_groups`; query kèm `user.groups` → chỉ match giao nhau. **An toàn > tiện**: thà thiếu kết quả còn hơn rò.

## 3. ⭐ Kiến trúc đa nguồn
```
Confluence ─┐
Drive      ─┤ [connector mỗi nguồn] ─> chuẩn hoá: text + metadata + ACL + updated_at
Slack      ─┤    (giữ quyền GỐC từ nguồn!)
DB/Notion  ─┘ ─> parse ([[ad06-doc-parsing]]) ─> chunk ─> embed
              ─> vector store (chunk + ACL + source + version)
query + user.groups ─> permission-aware retrieve ─> rerank ─> LLM + citation (nguồn nào)
```
- **Mỗi connector** lo: đọc nguồn, lấy **ACL gốc**, phát hiện đổi (CDC/poll), incremental ([[ad01-streaming-rag]]).
- **Đồng bộ quyền**: quyền ở nguồn đổi (thu hồi access) → phải cập nhật ACL trong index → nếu trễ = rò.

## 4. Freshness đa nguồn (mỗi nguồn nhịp khác)
| Nguồn | Nhịp đổi | Cách |
|-------|----------|------|
| Slack | liên tục | streaming/webhook |
| Confluence/Drive | giờ | poll/CDC incremental |
| DB | tuỳ | CDC |
→ Mỗi nguồn 1 freshness SLA ([[ac06-kb-freshness]]); ACL đổi phải **ưu tiên cao** (rò = nghiêm trọng).

## 5. Thông tin mâu thuẫn & chất lượng
- Nhiều nguồn nói khác nhau (Slack tin đồn vs Confluence chính thức) → **authority rank** ([[ac06-kb-freshness]]): doc chính thức > chat.
- Slack nhiều nhiễu (chitchat) → lọc chất lượng trước index ([[ae03-training-data-quality]]).
- Citation rõ nguồn → người dùng tự đánh giá độ tin.

## 6. Cạm bẫy (nhấn mạnh permission)
- **⭐ Bỏ qua quyền trong retrieval** → rò data nghiêm trọng → pre-filter ACL bắt buộc.
- **ACL trễ** (thu hồi access nhưng index chưa update) → vẫn rò → đồng bộ quyền ưu tiên cao.
- **LLM tóm tắt lộ doc cấm** (dù không hiển thị) → chỉ đưa doc được phép VÀO context, không lọc ở đầu ra.
- **Multi-tenancy lẫn** → user A thấy data B → cách ly theo tenant ([[ad03-privacy-compliance]]).
- **Treat mọi nguồn như nhau** → tin đồn = chính sách → authority rank.
- **Cache không theo user** → trả cache của người khác → key cache theo quyền/user.

## ✅ "Tự kiểm tra & tự mò"
- [ ] ⭐ Permission-aware retrieval: pre-filter ACL; an toàn > tiện.
- [ ] Connector đa nguồn giữ ACL gốc + incremental + đồng bộ quyền.
- [ ] Freshness mỗi nguồn 1 nhịp; ACL đổi ưu tiên cao.
- [ ] Mâu thuẫn → authority rank; Slack lọc nhiễu.
- [ ] Cạm bẫy rò quyền (ACL trễ, LLM tóm tắt lộ, cache theo user).
- 🔭 Tự mò: thêm cột `allowed_groups` vào bảng chunks trong `rag_over_notes.py` (gán nhóm giả cho mỗi note); sửa `search` thêm filter `WHERE list_has_any(allowed_groups, user_groups)`; thử 2 user khác quyền hỏi cùng câu → thấy kết quả khác nhau (permission-aware).

➡️ Tiếp [[af03-case-coding-assistant]] — coding assistant data platform.
