# C04 — Case: IoT / Sensor Data Platform

> Đặc trưng: **khối lượng ghi cực lớn**, time-series, out-of-order, edge. Áp [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: thu telemetry từ hàng triệu thiết bị (nhiệt độ, vị trí, trạng thái); dashboard real-time + phân tích lịch sử + alert ngưỡng (vd máy quá nhiệt).
- **Scale**: 1M thiết bị × 1 reading/10s ≈ **100K writes/s**, ~8.6 tỉ điểm/ngày. Dữ liệu nhỏ/điểm nhưng cực nhiều.
- **Latency**: alert vài giây; dashboard ~giây; phân tích lịch sử batch.
- **Đặc thù**: out-of-order (thiết bị offline rồi gửi bù), mạng chập chờn, edge có thể tiền xử lý.

## 2. Kiến trúc
```
Devices ──(MQTT/HTTP)──► Edge gateway (lọc/gộp/nén) ──► Kafka/Kinesis "telemetry"
                                                              │
                          ┌───────────────────────────────────┤
                          ▼ (hot path: alert)                  ▼ (cold path: lưu trữ)
                  Stream proc (windowed)               Sink → S3 BRONZE (Parquet, partition by dt/device)
                  - ngưỡng → alert                            │ batch rollup (Spark/dbt)
                  - downsample real-time                      ▼
                          │                            SILVER/GOLD: rollup theo phút/giờ/ngày
                          ▼                                    │
                  Time-series DB (dashboard)            Lake/warehouse (phân tích lịch sử, ML predictive maintenance)
```

## 3. Tech choices & trade-off
- **Edge preprocessing**: lọc/gộp tại gateway → giảm khối lượng gửi lên (không gửi mọi reading thô). Trade-off: mất chi tiết thô.
- **Time-series DB** (InfluxDB/TimescaleDB) hoặc lakehouse + downsampling cho dashboard nóng; lake (Parquet partition theo time+device) cho lịch sử rẻ.
- **Downsampling/rollup** ⭐: giữ raw ngắn hạn (vài ngày), rollup phút/giờ/ngày cho dài hạn → tiết kiệm storage khổng lồ. Retention tiered ([[55-cloud-fundamentals]], [[59-cost-finops]]).
- **Out-of-order**: event time + watermark; rollup chấp nhận cập nhật muộn (recompute partition) ([[49-stream-processing]]).

## 4. Scale & failure
- Partition Kafka theo device_id (hoặc region) để scale ghi 100K/s.
- **Hot partition**: thiết bị "nói nhiều" → cân bằng key.
- Compaction small files (nhiều thiết bị → nhiều file nhỏ) — vấn đề kinh điển IoT.
- Backpressure khi peak; buffer ở edge khi mất mạng rồi gửi bù (out-of-order).

## 5. Storage & retention
- Raw telemetry: giữ 7–30 ngày (nóng) → rollup → lưu lâu (lạnh/Glacier).
- Partition theo `dt` + (device hoặc region) cho pruning.
- Schema: cột timestamp, device_id, metric, value + tags; tránh quá nhiều cột partition (cardinality device cao!).

## 6. DQ & observability
- Phát hiện thiết bị **ngừng gửi** (freshness per device — gap detection, [[a01-sql-gaps-islands]]).
- Giá trị bất thường (sensor lỗi → spike/NaN); volume drop.
- Lineage rollup → raw.

## Câu hỏi đào sâu
- "Partition theo device_id có ổn với 1M device?" → cardinality quá cao cho partition file → partition theo time + bucket/region, device là cột thường.
- "Out-of-order xử lý sao?" → event time + watermark + cho phép recompute rollup partition khi data trễ tới.
- "Giảm chi phí?" → edge filter + downsampling + tiered storage.

## ✅ "Tự mò"
🔭 Thiết kế schema time-series + chính sách rollup (raw 7 ngày → 1' rollup 90 ngày → 1h rollup 2 năm); tính storage tiết kiệm so với giữ raw hết.

➡️ Tiếp: [[c05-case-ridesharing]].
