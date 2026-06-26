# C08 — Case: Ad-tech / Real-time Bidding (RTB)

> Đặc trưng: **latency cực thấp + khối lượng cực lớn + attribution join**. Áp [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: RTB (đấu giá quảng cáo < 100ms), track impression/click/conversion, **attribution** (click nào dẫn tới conversion), budget pacing, báo cáo nhà quảng cáo.
- **Scale**: **hàng triệu request/giây** (cao nhất về velocity), tỉ event/ngày.
- **Latency**: bid response **< 100ms** (cứng); analytics near-real-time + batch.
- **Đặc thù**: join impression↔click↔conversion lệch thời gian (conversion có thể sau nhiều ngày), fraud (click giả), budget không được vượt.

## 2. Kiến trúc (Lambda điển hình)
```
Bid requests ──► Bidder service (<100ms, KHÔNG đụng warehouse — dùng cache/precomputed)
                      │ log impression/click/conversion
                      ▼
                  Kafka (impressions, clicks, conversions)
                      │
        ┌─────────────┴─────────────┐
        ▼ SPEED layer               ▼ BATCH layer
   Stream proc:                 S3 BRONZE → Spark/dbt
   - budget pacing real-time    - attribution join (impression↔click↔conversion)
   - rolling spend → cap        - chính xác, xử lý late conversion
   - real-time dashboard        - báo cáo nhà quảng cáo
        └─────────────┬─────────────┘
                      ▼ SERVING (gộp speed + batch)
                  dashboard / billing
```

## 3. Tech choices & trade-off
- **Bidder KHÔNG query warehouse** (100ms budget): dùng precomputed segment/feature trong cache (Redis/Aerospike), model nhẹ. Data platform **chuẩn bị** feature offline → push online.
- **Lambda architecture** ⭐: speed layer cho budget pacing/dashboard near-real-time (gần đúng); batch layer cho attribution **chính xác** + late conversion (con số billing đúng). Đây là case Lambda hợp lý nhất ([[52-lambda-kappa]]).
- **Attribution join lệch thời gian**: conversion tới sau impression/click nhiều ngày → stream-stream join với **state + watermark dài** khó; thường batch join trên lake với cửa sổ attribution (vd 7/30 ngày).
- **Idempotent counting**: dedup impression/click theo id (at-least-once → trùng làm sai billing).

## 4. Scale & failure
- Partition Kafka theo campaign/user; scale ngang cho triệu/s.
- Budget pacing: eventual consistency có thể **vượt budget nhẹ** (đánh đổi latency vs chính xác) → batch reconcile + refund; hoặc strict cap (chậm hơn).
- Fraud/bot clicks → lọc (rule + ML), giống fraud case ([[c03-case-fraud]]).
- Late conversion → batch recompute attribution window.

## 5. Attribution models
- Last-click / first-click / linear / time-decay (xem [[a03-analytics-patterns]] attribution). Join conversion về touchpoint trong cửa sổ.

## 6. DQ & observability
- Discrepancy impression vs billing (tiền!) → reconciliation ([[c07-case-fintech]] tương tự).
- Volume/latency p99 của bidder; fraud rate.
- Double-count check (dedup hiệu quả?).

## Câu hỏi đào sâu
- "100ms làm sao?" → bidder dùng cache/precomputed, không đụng pipeline nặng; data platform feed feature offline→online.
- "Budget vượt do eventual consistency?" → chấp nhận lệch nhỏ + batch reconcile, hoặc strict cap đánh đổi latency.
- "Attribution conversion trễ 7 ngày?" → batch join với attribution window, không stream-stream join state quá dài.

## ✅ "Tự mò"
🔭 Viết attribution last-click: với mỗi conversion, tìm click gần nhất trong 7 ngày trước (window/join); đếm conversion theo campaign.

➡️ Tiếp: [[c09-case-recsys]].
