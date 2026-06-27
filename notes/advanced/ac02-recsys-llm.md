# AC02 — Recommendation + LLM (Semantic Recsys) ⭐ (có code chạy được)

> Gợi ý bằng **embedding** (content-based / two-tower) + LLM re-rank & giải thích. Giải **cold-start** nhờ embedding nội dung. **Vai trò DE: pipeline item/user embedding + serving + point-in-time.** Code: [`semantic_recsys.py`](../../projects/06-ai-data-engineering/semantic_recsys.py). Liên hệ [[c09-case-recsys]], [[ab07-vector-search-opt]].

## Recsys gặp embedding/LLM
Recsys cổ điển (collaborative filtering) cần **lịch sử tương tác** → **cold-start** chết (item/user mới không có lịch sử). Embedding nội dung cứu: item mới chỉ cần **mô tả** là gợi ý được.

## ⭐ Two-tower (thu nhỏ trong code)
```
ITEM tower:  mô tả item ─embed─> vector item   (tính offline, 1 lần, lưu sẵn)
USER tower:  các item user thích ─embed─> trung bình ─> vector user (profile)
RECOMMEND:   cosine(user, item_chưa_xem) cao nhất ─> gợi ý
```
- "Tower" = hàm biến thực thể thành vector cùng không gian → so bằng cosine ([[ab07-vector-search-opt]]).
- Production: item vector tính sẵn + ANN index; user vector tính lúc request (online).

## ⭐ Kết quả thật (code chạy)
User thích `rag-chunking` + `llm-guardrail` (AI infra) → gợi ý:
```
item            score   vì gần với
vector-ann      0.770  ~ rag-chunking     <- AI infra, đúng gu
parquet-format  0.737  ~ rag-chunking
star-schema     0.723  ~ rag-chunking
```
→ Top = `vector-ann` (cũng AI infra) — **đúng ngữ nghĩa**, dù chưa từng "thích" nó. Kèm **"vì sao"** = item đã thích gần nhất → giải thích được (explainable).

## ⭐ LLM tăng cường recsys ở đâu
| Vai trò LLM | Làm gì |
|-------------|--------|
| **Re-rank** | nhận top-N từ embedding, sắp lại theo ngữ cảnh/hồ sơ tinh hơn ([[aa03-rag-production]] rerank) |
| **Giải thích** | sinh câu "gợi ý vì bạn quan tâm X" tự nhiên (từ trường "why") |
| **Sinh metadata** | viết mô tả/tag item từ nội dung thô → tăng chất lượng embedding |
| **Conversational** | "tìm khoá học giống cái này nhưng dễ hơn" → hiểu intent → query embedding |
| **Cold-start user** | hỏi vài câu sở thích → tạo profile ngay, không chờ lịch sử |

## Vai trò DE (phần bạn sở hữu)
- **Item embedding pipeline**: nội dung/metadata → embed → vector store; cập nhật khi item đổi ([[ai04-embedding-versioning]]).
- **User profile**: tổng hợp tương tác (click/mua/thích) → vector; **incremental** cập nhật ([[ai09-streaming-ai]]).
- **⭐ Point-in-time correctness** ([[e04-bitemporal]]): train/eval phải dùng **trạng thái tại thời điểm đó**, không "nhìn tương lai" → tránh leakage (giống feature store [[ac07-feature-store]]).
- **Serving**: ANN low-latency ([[ab07-vector-search-opt]]) + filter (đã xem/hết hàng/vùng).

## Cạm bẫy
- **Trung bình embedding mất sở thích đa dạng**: user thích cả "AI" lẫn "nấu ăn" → mean ra điểm "giữa" vô nghĩa → nên **multi-interest** (nhiều profile/cluster) thay 1 mean.
- **Filter bỏ item đã xem/không hợp lệ** — quên thì gợi ý lại cái đã mua.
- **Baseline cosine cao** (text cùng ngôn ngữ) → điểm nén sát nhau; xem **thứ hạng tương đối**, không ngưỡng tuyệt đối (đúng bài học [[aa02-guardrails]] grounding).
- **Popularity bias / filter bubble**: chỉ gợi cái giống đã thích → chán; cần thêm khám phá (diversity, exploration).
- **Point-in-time sai** → leakage → offline đẹp, online tệ.
- **Cold-start vẫn cần mô tả tốt**: item mô tả nghèo → embedding nghèo → gợi ý kém (LLM sinh metadata cứu).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Two-tower: item-tower vs user-tower; recommend = cosine.
- [ ] Vì sao embedding content giải được cold-start.
- [ ] 5 vai trò LLM trong recsys (re-rank/giải thích/metadata/conversational/cold-start).
- [ ] Vai trò DE: item/user embedding + point-in-time + serving.
- [ ] Cạm bẫy mean-embedding, filter bubble, point-in-time leakage.
- 🔭 Tự mò: sửa `semantic_recsys.py` — thêm **multi-interest** (user thích 2 nhóm khác hẳn: AI + Spark; tách 2 profile, gợi ý từ mỗi cái); thêm **filter** loại item cùng nhóm đã thích để tăng diversity; thử thêm 1 item "mới" chỉ có mô tả (cold-start) xem có lọt top không.

➡️ Tiếp [[ac03-eval-driven-dev]] — eval-first cho AI.
