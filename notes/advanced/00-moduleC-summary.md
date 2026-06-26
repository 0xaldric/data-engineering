# 🏁 Module C — Tổng kết: System Design for Data Engineering

> Framework + 8 case study. Kỹ năng "thiết kế hệ thống dữ liệu" — vòng phỏng vấn quan trọng cho mid/senior.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| C01 | Framework 6 bước | [c01](c01-system-design-framework.md) |
| C02 | E-commerce analytics | [c02](c02-case-ecommerce.md) |
| C03 | Real-time fraud | [c03](c03-case-fraud.md) |
| C04 | IoT / sensor | [c04](c04-case-iot.md) |
| C05 | Ride-sharing | [c05](c05-case-ridesharing.md) |
| C06 | Clickstream / social | [c06](c06-case-clickstream.md) |
| C07 | Fintech ledger | [c07](c07-case-fintech.md) |
| C08 | Ad-tech / RTB | [c08](c08-case-adtech.md) |
| C09 | Recommendation | [c09](c09-case-recsys.md) |

## 📑 Khung trả lời (mọi case)
**Requirements** (functional + scale/velocity/latency/consistency) → **Scale ước lượng** → **Data model** → **Pipeline** (ingest→process→store→serve) → **Tech choices + trade-off** → **Scale & failure** → **DQ/observability**. ([[c01-system-design-framework]])

## So sánh các case (mẫu hình lặp lại)
| Case | Trục then chốt | Kiến trúc | Điểm đặc thù |
|------|----------------|-----------|--------------|
| E-commerce | analytics + chút real-time | batch + CDC + lakehouse | SCD2, inventory stream |
| Fraud | **latency ms + stateful** | streaming (Flink) | feature store, exactly-once-ish |
| IoT | **ghi cực lớn**, time-series | stream + rollup | edge, out-of-order, downsample |
| Ride-sharing | geospatial + real-time | lambda | H3, accumulating snapshot |
| Clickstream | **volume tỉ event** | stream + batch | schema evolution, OBT, sampling |
| Fintech | **chính xác tuyệt đối** | transactional + immutable | double-entry, reconciliation, idempotency |
| Ad-tech | **latency + volume + attribution** | lambda | bidder cache, attribution window |
| Recsys | feature pipeline | batch+stream features | feature store, train/serve consistency |

## Mẫu hình tái dùng (nhận ra → ăn điểm)
- **Latency ms + stateful** → Flink streaming + feature store.
- **Chính xác tiền** → idempotency + immutable + reconciliation.
- **Volume khổng lồ** → partition + Parquet + sampling/OLAP store + compaction.
- **Real-time + chính xác lịch sử** → Lambda (hoặc Kappa nếu log đủ).
- **Time-series/IoT** → rollup + tiered retention + out-of-order handling.
- **Luôn nêu**: idempotency, failure/replay, DQ/observability, trade-off cost/latency/complexity.

## ✅ Self-assessment Module C
- [ ] Đi qua framework 6 bước cho 1 case lạ trong 15 phút.
- [ ] Nhận ra mẫu hình (latency→Flink, tiền→reconciliation, volume→partition/sampling).
- [ ] Luôn nêu trade-off + failure handling + DQ.

## 🔭 Để "tự mò"
Tự thiết kế 1 case chưa có ở đây (vd: log analytics platform, ML feature platform, healthcare data, gaming telemetry) theo framework 6 bước.

## ➡️ Tiếp theo: Module D — Advanced Tool Deep-dives
Spark internals, dbt advanced (semantic layer), Kafka internals, Snowflake/BigQuery deep, Airflow advanced, Iceberg deep. (Loop sinh Batch #14.)
