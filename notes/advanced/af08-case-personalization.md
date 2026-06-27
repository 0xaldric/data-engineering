# AF08 — Case Study: Real-time AI Personalization

> Thiết kế hệ cá nhân hoá real-time (feed/gợi ý/nội dung) dùng embedding + LLM: streaming features + user/item vector + point-in-time + LLM re-rank. Tổng hợp recsys + feature store + streaming. Liên hệ [[ac02-recsys-llm]], [[ac07-feature-store]], [[ai09-streaming-ai]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: mỗi user thấy nội dung **hợp gu**, cập nhật theo hành vi **gần nhất** (vừa xem/click → gợi ý đổi ngay).
- **Quy mô**: triệu user, triệu item, nghìn event/giây, latency gợi ý <100ms.
- **Ràng buộc**: freshness (hành vi mới phản ánh nhanh), cold-start (user/item mới), point-in-time (chống leakage), cost ở scale.

## 2. ⭐ Kiến trúc (2 nhịp: offline build + online serve)
```
OFFLINE (chậm, lượng lớn)                ONLINE (nhanh, mỗi request)
item embedding ([[ac02-recsys-llm]])      event (xem/click) ─stream─> cập nhật profile user
user lịch sử -> profile vector            request gợi ý:
candidate retrieval index (ANN)            ─> retrieve candidate (user vec × ANN item)
                                           ─> feature online (real-time [[ac07-feature-store]])
                                           ─> rank (model/LLM re-rank [[ae07-reranking-deep]])
                                           ─> filter (đã xem/quyền/policy) ─> trả top-N
```

## 3. ⭐ Streaming features + real-time profile (mấu chốt freshness)
Hành vi vừa xảy ra phải đổi gợi ý ngay:
```
user click item X ─event─> [stream: Kafka/Flink]
   ─> cập nhật profile user (vd thêm embedding X vào "gu gần đây")
   ─> feature online store cập nhật ([[ac07-feature-store]] — Redis low-latency)
   ─> request kế tiếp đã phản ánh click X
```
- **Kappa/Lambda** ([[ai09-streaming-ai]]): streaming cho real-time + batch cho tính nặng (re-train, embedding lớn).
- Profile = **rolling** (gu gần đây + gu dài hạn), không chỉ trung bình tĩnh ([[ac02-recsys-llm]] multi-interest).

## 4. ⭐ Point-in-time (chống leakage — DE thuần)
Train ranking model: feature phải **as-of thời điểm impression**, không "nhìn tương lai" ([[ac07-feature-store]]):
```
impression lúc T -> "user đã xem gì TRƯỚC T", "item phổ biến TRƯỚC T"
   KHÔNG dùng "user click cái này SAU T" làm feature -> leakage -> offline ảo đẹp, online tệ
```
→ As-of join ([[e04-bitemporal]]) bắt buộc khi build training data.

## 5. ⭐ LLM tăng cường ở đâu
| Vai trò | Làm gì |
|---------|--------|
| **Re-rank** | nhận top-N từ ANN, sắp lại theo ngữ cảnh tinh ([[ac02-recsys-llm]]) |
| **Giải thích** | "gợi ý vì bạn vừa xem X" (tăng tin tưởng) |
| **Cold-start** | user mới: hỏi sở thích / dùng content embedding thay lịch sử |
| **Sinh nội dung** | tiêu đề/tóm tắt cá nhân hoá theo user |
→ LLM **bổ sung** lớp ranking, không thay candidate retrieval (ANN vẫn lo tốc độ/scale).

## 6. Cold-start & cost
- **Cold-start user**: chưa có lịch sử → dùng popular + content + vài câu hỏi sở thích.
- **Cold-start item**: item mới → content embedding (gợi ý được ngay, không chờ tương tác — [[ac02-recsys-llm]]).
- **Cost**: LLM re-rank mọi request = đắt → chỉ re-rank top-N nhỏ, cache, model nhỏ ([[ac08-ai-cost-scale]]); ANN lo phần triệu item rẻ.

## Cạm bẫy
- **Point-in-time sai** → leakage → offline đẹp, online sập (lỗi recsys kinh điển).
- **Profile tĩnh** (không streaming) → gợi ý không phản ánh hành vi mới → mất "real-time".
- **LLM re-rank mọi item** → quá đắt/chậm → chỉ top-N.
- **Quên filter** (đã xem/policy) → gợi ý lại cái đã xem / nội dung cấm.
- **Filter bubble** (chỉ giống đã thích) → chán → thêm exploration/diversity (MMR [[ae07-reranking-deep]]).
- **Bỏ cold-start** → user/item mới gợi ý rác → content embedding + popular fallback.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Kiến trúc 2 nhịp: offline (embedding/index) + online (profile/rank).
- [ ] Streaming features → profile real-time (kappa/lambda).
- [ ] Point-in-time as-of join chống leakage.
- [ ] LLM bổ sung ranking (re-rank/giải thích/cold-start), không thay ANN.
- [ ] Cold-start (content embedding) + cost (re-rank top-N).
- 🔭 Tự mò: mở rộng `semantic_recsys.py` ([[ac02-recsys-llm]]) — mô phỏng "stream" 3 click liên tiếp, mỗi click cập nhật profile (rolling: weight cao cho click mới) → in gợi ý đổi sau mỗi click (real-time personalization); thêm filter loại item đã "xem".

➡️ Tiếp [[af09-ai-review6]] — review 6 + system-design drill.
