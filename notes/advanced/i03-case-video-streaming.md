# I03 — Case: Video Streaming Platform (Netflix/YouTube)

> Khối lượng playback event khổng lồ + QoE real-time + recommendation. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: track playback (start/play/pause/seek/buffer/quality-change/complete); **QoE** (Quality of Experience: buffering, startup time, bitrate); recommendation data; A/B test (encoding, UI, algo); CDN analytics; creator analytics (YouTube).
- **Scale**: tỉ playback event/ngày (cao nhất nhóm); triệu concurrent stream.
- **Latency**: QoE/alert real-time (giây); recommendation near-real-time; analytics batch.
- **Đặc thù**: event cực lớn, sessionization (xem 1 video = session), watch-time, schema evolution.

## 2. Kiến trúc
```
Player SDK ──► event collector ──► Kafka (Avro+Schema Registry)
        │
        ┌───────────────┼────────────────┐
        ▼ real-time      ▼                 ▼ batch
  QoE monitoring     Stream proc:       S3 BRONZE → Spark/dbt
  (buffering spike   real-time          SILVER: sessionize playback, conform
   → alert CDN)      concurrent viewers GOLD: watch-time, retention, QoE aggregate,
        │            engagement          recommendation features, A/B analysis
  real-time dashboard                          │
  (OLAP: Druid)                          BI + ML (recsys, encoding optimization)
```

## 3. ⭐ QoE (Quality of Experience) — đặc thù
Metric chất lượng phát:
- **Startup time** (bấm play → frame đầu), **rebuffering ratio** (% thời gian buffer/tổng), **bitrate** (chất lượng), **error rate**.
- Real-time: buffering spike ở region/CDN → alert → chuyển CDN/giảm bitrate.
- QoE ảnh hưởng retention trực tiếp (buffer nhiều → bỏ xem) → metric kinh doanh.

## 4. Watch-time & engagement
- **Watch-time** (tổng thời gian xem) = metric vàng (YouTube tối ưu cái này).
- **Completion rate** (% video xem hết), retention curve **trong video** (audience retention: bỏ ở giây nào).
- Sessionize playback (start→complete/abandon — [[a01-sql-gaps-islands]]); xử lý seek/pause.

## 5. Tech choices & trade-off
- **Schema Registry + Avro**: event schema đổi (player version) — contract ([[48-kafka-ecosystem]], [[61-data-contracts]]).
- **Real-time OLAP (Druid)** cho concurrent viewers / QoE dashboard sub-giây ([[h06-realtime-olap]]).
- **Sampling** cho phân tích nặng (tỉ event) + raw đầy đủ cho cái cần chính xác.
- **Recommendation features** (feature pipeline — [[c09-case-recsys]]).
- Lake (lịch sử) + OLAP (real-time) song song.

## 6. Scale & failure
- Partition Kafka theo user/session; scale ngang tỉ event.
- Dedup playback heartbeat (gửi định kỳ → trùng) → đếm watch-time đúng.
- Late events (mobile offline) → event time + watermark.
- Bad QoE event (player bug) → quarantine.

## Câu hỏi đào sâu
- "Đo watch-time đúng từ heartbeat?" → sessionize + sum khoảng giữa heartbeat (cẩn thận gap/seek/dedup).
- "QoE real-time alert?" → stream aggregate rebuffering theo region/CDN, ngưỡng → alert.
- "Tỉ event lưu rẻ?" → Parquet + partition + sampling + OLAP cho hot.

## ✅ "Tự mò"
🔭 Thiết kế playback event schema (session_id, event, ts, position, bitrate, buffer_ms); SQL tính watch-time per session + rebuffering ratio; audience retention curve (% còn xem theo position).

➡️ Tiếp: [[i04-case-banking]].
