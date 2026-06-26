# 62 — Data Observability ⭐

> Monitoring hệ thống (CPU/RAM/uptime) ≠ **data observability** (dữ liệu có *đúng & tươi* không). Pipeline "xanh" vẫn có thể ra dữ liệu sai → cần quan sát chính dữ liệu.

## 5 trụ cột của Data Observability ⭐
| Trụ cột | Theo dõi gì | Bất thường ví dụ |
|---------|-------------|------------------|
| **Freshness** | dữ liệu mới đến đâu | bảng không cập nhật từ 2 ngày |
| **Volume** | số dòng/kích thước | row count tụt 90% (nguồn lỗi) hoặc tăng 10× (trùng) |
| **Schema** | cấu trúc thay đổi | cột bị xoá/đổi kiểu (breaking — [[61-data-contracts]]) |
| **Distribution** | giá trị có hợp lý | NULL rate tăng vọt, giá trị âm, phân phối lệch |
| **Lineage** | dòng chảy dữ liệu | bảng nào ảnh hưởng khi nguồn lỗi ([[63-lineage-catalog]]) |

→ Giám sát 5 trụ này = phát hiện sớm "data incident" trước khi business phát hiện.

## Khác monitoring truyền thống
- **Monitoring hệ thống**: job chạy xong chưa, server sống không, latency. (Airflow UI, Prometheus — [[43-airflow-reliability]].)
- **Data observability**: *nội dung* dữ liệu có đúng/tươi/đầy đủ không. Job có thể "success" mà vẫn ghi ra dữ liệu rác.
→ Cần **cả hai**.

## Cách triển khai
- **Rule-based**: ngưỡng cố định (row_count > 0, freshness < 1h, NULL% < 5%) — dbt tests/Soda ([[60-data-quality]]).
- **ML/anomaly-based**: học baseline lịch sử, cảnh báo khi lệch bất thường (volume/distribution drift) — công cụ chuyên làm tự động.
- **SLA/SLO cho data**: định nghĩa cam kết (vd "gold tươi trong 1h sau nửa đêm, 99%") + cảnh báo khi vi phạm (SLA Airflow — [[43-airflow-reliability]]).

## Công cụ
- **Elementary** (open-source, gắn dbt — bắt freshness/volume/anomaly từ dbt artifacts).
- **Soda** (checks + monitoring).
- **Monte Carlo, Bigeye, Metaplane** (thương mại, ML anomaly + lineage).
- **OpenLineage** (chuẩn lineage — [[63-lineage-catalog]]).

## Incident management cho data
- **Detect** (observability cảnh báo) → **triage** (mức độ, ai bị ảnh hưởng — dùng lineage) → **resolve** (sửa nguồn/pipeline, có thể rollback bằng time travel [[34-delta-lake]]) → **postmortem** (ngăn tái diễn, thêm test/contract).
- Mục tiêu giảm **TTD** (time to detect) & **TTR** (time to resolve).

## ⚠️ Cạm bẫy
- Chỉ monitor "job success", bỏ qua nội dung dữ liệu → dữ liệu sai trôi xuống dashboard.
- Alert quá nhiều/không hành động được → fatigue.
- Không có lineage → biết bảng lỗi nhưng không biết ai bị ảnh hưởng (triage mù).
- Không đo freshness → "dữ liệu cũ" không ai biết.

## ✅ Tự kiểm tra & "tự mò"
- [ ] 5 trụ cột observability.
- [ ] Phân biệt monitoring hệ thống vs data observability.
- [ ] Rule-based vs anomaly-based; SLA/SLO cho data.
- [ ] Vòng đời data incident (detect→triage→resolve→postmortem); TTD/TTR.
- 🔭 *Tự mò:* viết script tính 5 metric đơn giản trên `data/raw` (freshness = max ngày, volume = row count, schema = list cột, NULL%, min/max) và in cảnh báo nếu vượt ngưỡng — đó là observability mini.

➡️ Tiếp: [[63-lineage-catalog]].
