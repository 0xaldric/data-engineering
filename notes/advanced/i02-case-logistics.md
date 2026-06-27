# I02 — Case: Logistics / Supply Chain Platform

> Theo dõi hàng hoá từ kho tới khách: shipment lifecycle, inventory, route, ETA. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: theo dõi shipment (picked→packed→in-transit→delivered), quản kho (inventory), tối ưu route, ETA, demand forecast, inventory optimization.
- **Scale**: triệu shipment, IoT tracking (vị trí xe/gói liên tục), nhiều kho/SKU.
- **Latency**: tracking real-time (giây); forecast/optimization batch.
- **Đặc thù**: **accumulating snapshot** (shipment nhiều mốc), geospatial (route/vị trí), inventory chính xác (như tiền).

## 2. Kiến trúc
```
WMS/ERP (OLTP) ──CDC──► shipment/inventory events
GPS trackers ──► Kafka "location" (high vol)
        │
        ▼
   BRONZE → SILVER:
     - fct_shipment_lifecycle (ACCUMULATING SNAPSHOT: order→pick→pack→ship→deliver + lag measures)
     - inventory movements (in/out per SKU per warehouse)
        │
        ▼
   GOLD:
     - delivery performance (on-time %, avg transit time, SLA)
     - inventory levels/turnover, stockout risk
     - route efficiency, courier utilization
        │
        ▼
   real-time tracking (Redis/OLAP) + BI + ML (ETA, demand forecast, inventory opt)
```

## 3. Modeling đặc thù
- **Accumulating snapshot** ⭐ cho shipment ([[19-fact-types]]): mỗi mốc (pick/pack/ship/deliver) là date role; lag measures (pick_to_ship_hours, transit_days); hàng được UPDATE khi tiến triển.
- **Inventory** = balance (semi-additive — [[19-fact-types]]): không SUM tồn theo thời gian; lấy snapshot cuối kỳ. Inventory movements (transaction) → snapshot ledger.
- Geospatial (route/vị trí) — H3/geohash ([[c05-case-ridesharing]]).

## 4. Bài toán phân tích
- **On-time delivery rate**, SLA breach (giao trễ).
- **Transit time** phân tích (đâu chậm — funnel của lifecycle).
- **Inventory turnover**, stockout (hết hàng), overstock; ABC analysis (RFM-like cho SKU).
- **Demand forecast** (ML) → reorder point, inventory optimization.
- **Route efficiency**, fuel, courier utilization.

## 5. Tech choices & trade-off
- **CDC từ WMS/ERP** → shipment/inventory near-real-time ([[51-cdc-debezium]]).
- **Stream** location/tracking (real-time ETA); **batch** analytics/forecast.
- Inventory chính xác → reconciliation (physical count vs system — như fintech [[c07-case-fintech]]).

## 6. Scale & failure
- Location stream lớn → downsample (như IoT [[c04-case-iot]]).
- Shipment "kẹt" (không tiến mốc) → alert (accumulating snapshot có mốc null lâu).
- Inventory invariant (không âm, in-out cân bằng) → DQ check.

## Câu hỏi đào sâu
- "Model shipment lifecycle?" → accumulating snapshot + lag measures.
- "Inventory level đúng?" → movements ledger + snapshot, không SUM theo thời gian (semi-additive).
- "Phát hiện shipment kẹt?" → mốc tiếp theo null quá lâu → alert.

## ✅ "Tự mò"
🔭 Thiết kế fct_shipment_lifecycle (order_date, pick_date, ship_date, deliver_date + lag); query on-time rate + avg transit + funnel mốc (như [[19-fact-types]] order lifecycle).

➡️ Tiếp: [[i03-case-video-streaming]].
