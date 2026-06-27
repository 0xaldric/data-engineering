# K03 — Case: Real Estate / PropTech Platform

> Listing + định giá (AVM) + market analytics. Đa nguồn + geospatial + slowly changing. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: quản listing (đăng/cập nhật/bán), search/discovery, **AVM** (Automated Valuation Model — ước giá nhà), market analytics (giá theo khu vực/thời gian), lead/agent analytics.
- **Scale**: triệu listing, lịch sử giao dịch nhiều năm, nhiều nguồn (MLS, public records, web).
- **Latency**: search ~giây; valuation/analytics batch.
- **Đặc thù**: ingest **đa nguồn** không đồng bộ (MLS feed, sổ đăng ký công, scraping), geospatial, **listing thay đổi** (giá/status → SCD), price history quan trọng.

## 2. Kiến trúc
```
MLS feed ──┐
Public records ──► ingest (chuẩn hoá địa chỉ, dedup property) ──► BRONZE
Web/scraping ──┘                                                    │
        │  MDM: hợp nhất "property" across nguồn (address matching)
        ▼
   SILVER:
     - dim_property (SCD2: giá/status đổi → price history)
     - fct_listing_events (list/price-change/sale)
     - dim_geo (region/neighborhood, geospatial)
        │
        ▼
   GOLD: market analytics (median price/region/time), AVM features, days-on-market
        │
        ▼
   search + AVM model (price estimate) + BI
```

## 3. ⭐ Đặc thù modeling
- **MDM / address matching**: cùng property ở nhiều nguồn (MLS + public records) → resolve về một entity (địa chỉ chuẩn hoá khó: viết tắt, sai chính tả) — như govtech MDM ([[j04-case-govtech]]).
- **SCD2 cho listing** ([[18-scd]]): giá/status đổi theo thời gian → price history (phân tích "giá giảm bao nhiêu lần trước khi bán").
- **Slowly changing price**: track mọi lần đổi giá (event) → days-on-market, price reduction patterns.
- Geospatial (region, comparable nearby — [[c05-case-ridesharing]] H3).

## 4. AVM (định giá tự động) — data cho ML
- Features: diện tích, phòng, vị trí, **comparables** (nhà tương tự gần đó bán gần đây — nearest neighbor theo geo + time, **as-of** — [[k01-sql-interview-8]]), market trend.
- Feature pipeline (như recsys — [[c09-case-recsys]]); point-in-time (giá comparable **tại thời điểm** định giá, không tương lai → tránh leakage).

## 5. Analytics
- **Median price** theo region/time (median per group — [[a04-sql-interview-1]]).
- **Days-on-market** (list → sale), price reduction.
- **Market trend** (YoY, inventory levels — supply như marketplace [[h02-case-marketplace]]).
- **Absorption rate** (tốc độ bán).

## 6. DQ & observability
- Address/property dedup quality (MDM).
- Listing freshness (feed MLS cập nhật?).
- Outlier giá (data lỗi vs nhà đặc biệt).

## Câu hỏi đào sâu
- "Hợp nhất property đa nguồn?" → MDM + address standardization/matching.
- "Price history?" → SCD2 / event mỗi lần đổi giá.
- "AVM comparables không leakage?" → as-of join (comparable bán **trước** thời điểm định giá).

## ✅ "Tự mò"
🔭 Thiết kế dim_property SCD2 + fct_price_change; query days-on-market, số lần giảm giá trước khi bán, median price theo region/quý; comparable bằng as-of + geo.

➡️ Tiếp: [[k04-case-agritech]].
