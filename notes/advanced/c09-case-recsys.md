# C09 — Case: Recommendation System Data Pipeline

> Góc nhìn **DE** cho recsys: không phải xây thuật toán ML, mà xây **data pipeline + feature store** nuôi model. Áp [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: cung cấp dữ liệu cho hệ gợi ý (sản phẩm/nội dung): training data, features (user/item/context), serving features real-time, feedback loop.
- **Scale**: nhiều user × item; event tương tác lớn (như clickstream — [[c06-case-clickstream]]).
- **Latency**: features online ms (lúc serve gợi ý); training batch.
- **Đặc thù**: train/serve consistency, feedback loop, cold start.

## 2. Kiến trúc (DE-centric)
```
Interaction events (view/click/buy/rate) ──► Kafka ──► lake BRONZE
        │                                                  │ batch (Spark/dbt)
        │ real-time features                               ▼
        ▼                                          SILVER: clean, sessionize
  Stream proc: recent activity                            │
  (last N viewed, real-time context)                      ▼
        │                                          FEATURE ENGINEERING:
        ▼                                          - user features (RFM, affinity, embeddings input)
  FEATURE STORE (online: Redis)  ◄──── sync ────   - item features (popularity, category, co-view)
        │                                          - offline store (lake/warehouse)
        ▼                                                  │
  Serving: model lấy features → gợi ý               TRAINING data (labeled) → train model (offline)
        │                                                  ▲
        └──────── feedback (click/ignore) ─────────────────┘ (đóng vòng lặp)
```

## 3. ⭐ Feature Store (khái niệm DE quan trọng)
Hệ quản lý feature cho ML, giải 2 vấn đề:
- **Train/serve consistency**: cùng định nghĩa feature lúc train (offline, lake) và lúc serve (online, Redis) → tránh **skew** (model thấy feature khác lúc train vs serve = lỗi âm thầm).
- **Reuse & governance**: feature dùng lại across models, versioned, có metadata/lineage.
| | Offline store | Online store |
|--|---------------|--------------|
| Dùng | training (batch, lịch sử lớn) | serving (low-latency lookup) |
| Công nghệ | lake/warehouse (Parquet) | Redis/DynamoDB |
| Tính | batch (Spark/dbt) | sync từ offline + real-time stream |
Công cụ: Feast, Tecton, hoặc tự build.

## 4. Tech choices & trade-off
- **Batch features** (RFM, popularity, co-view matrix) — Spark/dbt, cập nhật hằng ngày. **Real-time features** (vừa xem gì) — stream. Lai (đa số recsys).
- **Point-in-time correctness** ⭐: khi tạo training data, feature phải là giá trị **tại thời điểm event xảy ra** (không dùng feature tương lai → **data leakage**). Cần as-of join (giống SCD2 as-of — [[18-scd]]).
- **Cold start**: user/item mới chưa có feature → fallback (popular items, content-based).

## 5. Scale & failure
- Feature pipeline lớn → partition, incremental.
- Online store sync trễ → feature cũ; monitor freshness.
- Feedback loop bias (chỉ thấy cái đã gợi ý) → cần exploration/logging đầy đủ.

## 6. DQ & observability
- **Feature drift** (phân phối feature đổi → model kém) — observability ([[62-observability]]).
- Train/serve skew monitoring.
- Point-in-time correctness check (không leakage).

## Câu hỏi đào sâu
- "Train/serve skew là gì, tránh sao?" → feature store dùng chung định nghĩa; log feature lúc serve.
- "Data leakage trong training data?" → point-in-time/as-of join, không dùng feature sau thời điểm label.
- "Real-time vs batch features?" → lai; cái đổi nhanh (session) real-time, cái ổn định (popularity) batch.

## ✅ "Tự mò"
🔭 Trên e-commerce, tạo offline features cho user (RFM, top category) + item (popularity, co-purchase) bằng SQL; nghĩ cái nào cần online store cho serving.

➡️ Tiếp: [[00-moduleC-summary]].
