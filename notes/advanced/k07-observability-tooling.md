# K07 — Deep-dive: Data Observability Tooling

> Từ khái niệm 5 trụ ([[62-observability]]) → triển khai đo & cảnh báo thực tế.

## 5 trụ — đo thế nào (cụ thể)
| Trụ | Metric đo | Cách phát hiện bất thường |
|-----|-----------|---------------------------|
| **Freshness** | `now() - max(updated_at)` per table | > ngưỡng (vd 2h) → alert |
| **Volume** | row count mỗi lần load | lệch > X% so baseline (theo mùa) |
| **Schema** | snapshot cột/kiểu | diff so lần trước (cột mất/đổi kiểu) |
| **Distribution** | null%, min/max, distinct count, mean | lệch bất thường (null% tăng vọt) |
| **Lineage** | DAG ref/source | impact analysis khi node lỗi |

## Rule-based vs Anomaly-based
- **Rule-based**: ngưỡng cố định (`freshness < 1h`, `null% < 5%`). Đơn giản, rõ; nhưng data có **mùa vụ** (volume Tết khác) → ngưỡng cứng báo nhầm.
- **Anomaly-based (ML)**: học **baseline** lịch sử (trung bình + độ lệch theo thứ/giờ/mùa) → cảnh báo khi lệch bất thường. Tự thích nghi; ít false alert. Công cụ thương mại làm tự động.

## Công cụ
| Công cụ | Đặc điểm |
|---------|----------|
| **Elementary** | open-source, **dbt-native** (đọc dbt artifacts: test results, freshness, volume) — dễ tích hợp nếu đã dùng dbt |
| **Soda** | SodaCL checks + monitoring, CI-friendly |
| **Great Expectations** | DQ suite + data docs (thiên DQ hơn observability) |
| **Monte Carlo / Bigeye / Metaplane** | thương mại, ML anomaly + lineage + incident, end-to-end |
| **OpenLineage + Marquez** | chuẩn lineage |

### Elementary (nếu dùng dbt) — dễ nhất
```yaml
# tận dụng dbt: thêm elementary tests/monitors
models:
  - name: fct_sales
    config:
      elementary:
        volume_anomalies: true       # tự phát hiện row count bất thường
        freshness: { column: order_ts, threshold: 24h }
```
→ Sinh report observability + alert từ chính dbt run, ít công.

## SLO cho data
Định nghĩa cam kết đo được ([[f02-reliability-sre]]):
- "Gold tươi < 1h sau nửa đêm, 99% số ngày."
- "Volume trong ±20% baseline."
- "DQ score ≥ 95%."
→ Vi phạm SLO → alert + error budget tracking.

## Alerting & incident (tránh fatigue)
- Alert **hành động được** (ai làm gì), severity rõ (P1 tiền/exec vs P3 phụ).
- Route đúng người (owner từ catalog/contract).
- Dedup/group alert (1 nguồn lỗi → 1 alert, không 50).
- Incident lifecycle: detect→triage (lineage)→mitigate→resolve→postmortem ([[f02-reliability-sre]]).

## Triển khai từng bước
```
1. Bắt đầu rule-based đơn giản: freshness + volume + dbt tests (đã có)
2. Thêm schema + distribution monitoring
3. Lineage (dbt docs / OpenLineage) cho impact analysis
4. Anomaly-based khi rule-based gây fatigue (mùa vụ)
5. SLO + error budget + on-call
6. Incident process + postmortem
```

## ⚠️ Cạm bẫy
- Chỉ monitor "job success", bỏ nội dung data ([[62-observability]]).
- Ngưỡng cứng cho data mùa vụ → false alert → fatigue.
- Mua tool đắt nhưng không có owner/process → vỏ rỗng.
- Không lineage → biết lỗi nhưng không biết ai ảnh hưởng.
- Quá nhiều alert không gom → bị phớt lờ.

## ✅ "Tự mò"
🔭 Viết script Python tính 5 metric (freshness/volume/schema/null%/range) trên `data/raw`, lưu lịch sử qua các lần chạy, cảnh báo khi lệch > ngưỡng — đó là observability mini. Nếu dùng dbt: thử `elementary` package.

➡️ Tiếp: [[00-extraK-summary]].
