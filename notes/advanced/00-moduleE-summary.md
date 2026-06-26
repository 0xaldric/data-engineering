# 🏁 Module E — Tổng kết: Advanced Data Modeling

> Vượt khỏi star schema: các paradigm modeling hiện đại & chuyên biệt.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| E01 | Data Vault 2.0 | [e01](e01-data-vault.md) |
| E02 | One Big Table / Wide / Activity schema | [e02](e02-obt-wide.md) |
| E03 | Event / Clickstream modeling | [e03](e03-event-modeling.md) |
| E04 | Bitemporal modeling | [e04](e04-bitemporal.md) |
| E05 | Semantic layer & metrics | [e05](e05-semantic-layer.md) |

## 📑 So sánh các paradigm modeling
| Paradigm | Tối ưu | Khi nào |
|----------|--------|---------|
| **Kimball star** ([[17-dimensional-modeling]]) | BI dễ hiểu, đọc nhanh | mart/BI mặc định |
| **Inmon 3NF EDW** | tích hợp chuẩn hoá | EDW truyền thống |
| **Data Vault** | audit + linh hoạt + parallel load | nhiều nguồn, regulated, đổi nhiều |
| **OBT / Wide** | không join, đơn giản, columnar | mart BI cụ thể, feature table |
| **Activity schema** | customer journey linh hoạt | clickstream/behavioral |
| **Bitemporal** | 2 trục thời gian (audit hồi tố) | tài chính/bảo hiểm/pháp lý |

## Mẫu hình thực tế kết hợp
```
Nguồn → Raw Vault (audit/lịch sử, Data Vault) → Star marts (Kimball) → OBT/Wide (BI cụ thể) → Semantic layer (metric)
```
Không "một paradigm cho tất cả": chọn theo tầng & use case. Star vẫn là nền tảng; DV cho tích hợp regulated; OBT cho BI columnar; semantic layer cho nhất quán metric.

## Điểm cốt lõi
- **Grain** vẫn là quyết định đầu tiên ở mọi paradigm.
- **Lịch sử/audit**: SCD2 (1 trục) → bitemporal (2 trục) → Data Vault (audit bẩm sinh).
- **Columnar warehouse** làm OBT/wide khả thi (đọc cột không phạt bảng rộng).
- **Semantic layer** giải "metric drift" — một định nghĩa, mọi nơi.

## ✅ Self-assessment Module E
- [ ] Hub/Link/Satellite & vì sao Data Vault (audit/linh hoạt).
- [ ] OBT vs star — khi nào denormalize hoàn toàn.
- [ ] Model event (JSON/STRUCT property, sessionization).
- [ ] Bitemporal: valid time vs transaction time (backdated correction).
- [ ] Semantic layer giải metric drift thế nào.

## 🔭 Để "tự mò"
Mô hình hoá e-commerce theo 3 cách (star đã có / Data Vault / OBT) và so query + bảo trì. Định nghĩa 2 metric bằng semantic layer.

## ➡️ Tiếp theo: Module F — DataOps, Architecture & Career
Data testing strategy, reliability/incident, modern data stack, cost case studies, data mesh/products, roadmap senior. (Loop sinh Batch #16.)
