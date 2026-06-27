# AG07 — Conversational Memory & Long Context

> Hội thoại dài (chatbot, agent nhiều lượt) cần kiến trúc **memory** thông minh: nhớ gì, quên gì, nhồi-cả vs retrieve. Sâu hơn [[ab03-context-engineering]] (token budget) → kiến trúc memory đầy đủ. Liên hệ [[ad07-agent-data]], [[ag01-rag-bi-analytics]].

## Vì sao memory hội thoại khó
- Hội thoại dài → vượt context window → không nhồi hết được.
- Nhồi cả lịch sử (long-context) → tốn token + **lost-in-the-middle** ([[ab03-context-engineering]]) + đắt.
- Cần **nhớ đúng cái quan trọng**, quên cái nhiễu → như trí nhớ người.

## ⭐ 3 loại memory (mượn từ khoa học nhận thức)
| Loại | Là gì | Lưu ở đâu |
|------|-------|-----------|
| **Working** (ngắn hạn) | lượt hội thoại hiện tại, kết quả tool vừa rồi | trong context window |
| **Episodic** | "đã xảy ra gì" — lịch sử hội thoại, sự kiện | store + tóm tắt phân cấp |
| **Semantic** | fact bền về user/thế giới ("user thích Python") | vector store + structured (entity memory) |
→ Agent tốt dùng cả ba: working (ngay), episodic (đã nói gì), semantic (biết gì về user).

## ⭐ Long-context vs RAG-memory (quyết định kiến trúc)
```
LONG-CONTEXT: nhồi cả hội thoại vào context window lớn
  + đơn giản, model thấy hết       - đắt (token), lost-in-middle, vẫn có giới hạn
RAG-MEMORY: lưu hội thoại -> retrieve phần liên quan khi cần
  + rẻ, scale vô hạn, chọn lọc     - phức tạp, có thể miss context
```
→ Thực tế **kết hợp**: working memory (lượt gần, nhồi) + RAG-memory (lôi lượt cũ liên quan) + summary (nén phần giữa). "Context window lớn không xoá nhu cầu quản memory" — vẫn đắt + lost-in-middle.

## ⭐ Tóm tắt phân cấp (rolling/hierarchical summary)
```
lượt 1-3 ─┐
lượt 4-6 ─┼─> tóm tắt mức 1 ─┐
lượt 7-9 ─┘                  ├─> tóm tắt mức 2 (toàn hội thoại)
...                          ┘
context = [tóm tắt mức cao] + [vài lượt gần nhất nguyên văn] + [fact retrieve]
```
- Lượt cũ → nén dần thành tóm tắt (giảm token, giữ ý) ([[ab03-context-engineering]]).
- Lượt gần → giữ nguyên văn (chi tiết quan trọng).
- ⚠️ Tóm tắt **mất fact chính xác** (số, ID) → giữ riêng entity memory.

## ⭐ Entity memory (fact bền, chính xác)
```
trích fact dạng key-value: {user.tên: "An", user.thích: "Python", dự_án: "RAG"}
-> không nén/mất như summary text -> luôn chính xác khi cần
```
→ Cho fact cần **đúng tuyệt đối** (tên, số, lựa chọn) — bổ sung summary (cho mạch chuyện).

## Forgetting & TTL (quên có chủ đích)
- Không phải fact nào cũng giữ mãi → **TTL** (hết hạn), **relevance decay** (cũ → ít ưu tiên).
- Dọn memory mâu thuẫn/lỗi thời ([[ac06-kb-freshness]]); tách phiên/user (privacy [[ad03-privacy-compliance]]).
- "Quên" giúp memory gọn, đúng, rẻ — như người quên chi tiết vụn.

## Cạm bẫy
- **Nhồi cả lịch sử** → đắt + lost-in-middle → summary + RAG-memory.
- **Tóm tắt mất fact** (số/ID) → entity memory riêng cho fact chính xác.
- **Không tách phiên/user** → rò chéo memory người khác.
- **Memory không dọn** → phình + mâu thuẫn → TTL + decay + dedup.
- **Tin "context lớn xoá mọi vấn đề"** → vẫn đắt + lost-in-middle → vẫn cần quản.
- **Retrieve memory sai** (lôi lượt không liên quan) → nhiễu → rerank memory ([[ae07-reranking-deep]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] 3 loại memory (working/episodic/semantic).
- [ ] Long-context vs RAG-memory; vì sao kết hợp.
- [ ] Tóm tắt phân cấp (nén lượt cũ, giữ lượt gần).
- [ ] Entity memory cho fact chính xác (summary mất số/ID).
- [ ] Forgetting/TTL/decay; tách phiên chống rò.
- 🔭 Tự mò: viết vòng hội thoại nhiều lượt dùng `rag_over_notes.embed` làm "memory store": mỗi lượt lưu (text, vector); lượt mới → retrieve 2 lượt cũ liên quan nhất + giữ 2 lượt gần nhất nguyên văn + 1 "summary" (nối text) → ghép thành context; quan sát token tiết kiệm vs nhồi cả.

➡️ Tiếp [[ag08-ai-data-contracts]] — data contract cho AI I/O.
