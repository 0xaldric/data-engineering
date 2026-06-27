# AC07 — Feature Store cho ML/LLM

> Kho **feature** dùng chung cho train & serve, đảm bảo **online/offline parity** + **point-in-time correctness** (chống leakage). Nơi DE kinh điển gặp ML/AI. Liên hệ [[ab05-embedding-finetune]], [[e04-bitemporal]], [[ac02-recsys-llm]].

## Feature store giải bài toán gì
| Vấn đề không có FS | Feature store cứu |
|--------------------|-------------------|
| **Train/serve skew**: feature tính khác nhau lúc train (SQL batch) vs serve (code online) → model lệch | **một định nghĩa** feature, dùng cả hai phía |
| **Leakage**: train dùng giá trị "tương lai" → offline đẹp, online tệ | **point-in-time** lookup |
| Mỗi team tính lại cùng feature | **reuse** + catalog feature |
| Feature online chậm | **online store** low-latency (Redis/KV) |

## ⭐ Online vs Offline store (parity)
```
              ┌─ OFFLINE store (warehouse/parquet) ─> TRAIN (lượng lớn, lịch sử)
feature ──────┤        ↑ cùng định nghĩa, cùng giá trị ↓
              └─ ONLINE store (Redis/KV)          ─> SERVE (1 entity, <10ms)
```
- **Parity**: giá trị feature lúc serve phải khớp lúc train → cùng logic, đồng bộ online từ offline.
- Lệch parity = nguồn lỗi model khó tìm nhất.

## ⭐⭐ Point-in-time correctness (chống leakage)
Train phải dùng giá trị feature **đúng tại thời điểm sự kiện**, không phải giá trị hiện tại.
```
Sự kiện: user mua hàng lúc T.
  feature "tổng chi 30 ngày qua" phải tính tới mốc T   ✅ (as-of T)
  KHÔNG được dùng tổng chi tính tới HÔM NAY            ❌ (nhìn tương lai = leakage)
```
→ Cần **as-of join** (bitemporal [[e04-bitemporal]]): với mỗi nhãn ở thời điểm T, lấy feature có hiệu lực ≤ T. Đây là kỹ năng DE thuần (window/temporal join) áp cho ML.

## ⭐ Embedding như feature (cầu nối tới LLM/AI)
- Vector embedding ([[ab05-embedding-finetune]]) **là một feature** → lưu/serve qua feature store hoặc vector store.
- Recsys ([[ac02-recsys-llm]]): user/item embedding = feature, cần point-in-time (embedding tại lúc đó, không phải bây giờ).
- LLM app: feature ngữ cảnh (hồ sơ user, lịch sử) đưa vào prompt cũng nên qua kho có kiểm soát → nhất quán, có lineage.

## Kiến trúc & lineage
```
nguồn (events/DB) ─> [feature pipeline: định nghĩa 1 nơi] ─┬─> offline store ─> train
   (batch + streaming)                                    └─> online store  ─> serve
   feature có: tên, owner, định nghĩa, version, freshness, lineage  (như data contract [[k06-data-contract-impl]])
```
- **Versioning** feature: đổi định nghĩa → version mới, model ghi rõ dùng version nào (reproducibility [[ab08-finetune-pipeline]]).
- **Freshness**: feature streaming (gần real-time) vs batch (hàng ngày) — SLA theo nhu cầu.

## Công cụ (biết tên)
Feast (open-source), Tecton, Databricks/Vertex/SageMaker Feature Store. Bản chất: **offline + online store + định nghĩa feature + point-in-time serving**. Vector store (Qdrant...) lo riêng phần embedding.

## Cạm bẫy
- **Train/serve skew** vì 2 đường tính feature khác nhau → luôn 1 định nghĩa dùng chung.
- **Leakage** vì quên point-in-time → as-of join bắt buộc cho feature lịch sử.
- **Online store cũ** (không đồng bộ kịp) → serve giá trị lỗi thời → monitor freshness.
- **Quá kỹ thuật hoá**: dự án nhỏ chưa cần FS đầy đủ → đừng over-engineer.
- **Không version feature** → đổi định nghĩa âm thầm phá model đang chạy.
- **Embedding không point-in-time** (recsys) → leakage tinh vi → offline ảo đẹp.

## ✅ "Tự kiểm tra & tự mò"
- [ ] FS giải gì: train/serve parity + point-in-time + reuse + online low-latency.
- [ ] Online vs offline store; parity nghĩa là gì.
- [ ] Point-in-time correctness + as-of join chống leakage.
- [ ] Embedding như feature; liên hệ recsys/LLM.
- [ ] Cạm bẫy skew, leakage, online cũ, over-engineer.
- 🔭 Tự mò: bằng DuckDB, dựng `events(user, ts, amount)` + bảng nhãn `labels(user, event_ts)`; viết **as-of join** tính "tổng chi 30 ngày trước event_ts" cho mỗi nhãn (point-in-time đúng) rồi so với phiên bản SAI dùng tổng-chi-hiện-tại — thấy leakage làm feature "biết tương lai" thế nào.

➡️ Tiếp [[ac08-ai-cost-scale]] — tối ưu cost AI ở scale.
