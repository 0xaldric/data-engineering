# E01 — Data Vault 2.0 ⭐

> Một paradigm modeling warehouse khác Kimball (star) và Inmon (3NF) — tối ưu cho **audit, linh hoạt khi nguồn đổi, parallel load**.

## Vấn đề Data Vault giải
Star schema khó theo kịp khi: nhiều nguồn, nguồn đổi schema liên tục, cần audit đầy đủ (ai/khi/từ đâu), load song song quy mô lớn. DV tách **khoá nghiệp vụ**, **quan hệ**, **thuộc tính** thành 3 loại bảng → thêm nguồn/đổi schema chỉ thêm bảng, không phá cái cũ.

## 3 loại bảng cốt lõi
```
        ┌──────── HUB ────────┐         HUB = business key (định danh thực thể)
        │ hub_customer        │           hub_customer(customer_hk, customer_id, load_ts, source)
        │ (customer business  │
        │  key + surrogate)   │
        └──────────┬──────────┘
                   │
        ┌──────────┴──────────┐         LINK = quan hệ giữa các hub
        │ link_order          │           link_order(order_hk, customer_hk, product_hk, load_ts, source)
        │ (nối customer×product)│
        └──────────┬──────────┘
                   │
        ┌──────────┴──────────┐         SATELLITE = thuộc tính + LỊCH SỬ (descriptive, đổi theo thời gian)
        │ sat_customer_detail │           sat_customer(customer_hk, load_ts, name, country, hash_diff)
        │ (name, country...)  │
        └─────────────────────┘
```
- **Hub**: chỉ business key + hash key (surrogate, thường MD5 của business key) + metadata (load_ts, record_source). Không thuộc tính mô tả.
- **Link**: quan hệ nhiều-nhiều giữa hub (transaction, association). Chỉ hash key + metadata.
- **Satellite**: thuộc tính mô tả + **lịch sử thay đổi** (như SCD2 — nhiều dòng theo load_ts, `hash_diff` để phát hiện đổi). Gắn vào hub hoặc link.

## Vì sao DV (ưu điểm)
- **Auditability**: mọi bản ghi có `record_source` + `load_ts` → biết từ đâu, khi nào. Append-only, không update → audit hoàn hảo (giống ledger — [[c07-case-fintech]]).
- **Linh hoạt**: thêm nguồn mới = thêm satellite/link, **không** đụng cái cũ. Schema nguồn đổi → satellite mới.
- **Parallel load**: hub/link/sat độc lập (chỉ phụ thuộc business key) → load song song quy mô lớn.
- **Tách raw khỏi business logic**: raw vault (nguyên trạng) → business vault (áp rule).

## Kiến trúc 2 tầng
```
Nguồn → Raw Vault (DV nguyên trạng, append-only) → Business Vault (áp business rule)
                                                  → Marts (STAR schema cho BI — [[17-dimensional-modeling]])
```
→ DV thường là **tầng tích hợp/lịch sử**; vẫn build **star schema ở mart** cho người dùng cuối (DV khó query trực tiếp, nhiều join).

## So sánh paradigm
| | Kimball (star) | Inmon (3NF EDW) | Data Vault |
|--|----------------|------------------|------------|
| Tối ưu | đọc/BI dễ hiểu | tích hợp chuẩn hoá | audit + linh hoạt + load |
| Query trực tiếp | dễ | trung bình | khó (nhiều join) → cần mart |
| Đổi nguồn/schema | phải sửa | phải sửa | **thêm bảng, ít phá** |
| Audit/lịch sử | SCD | tuỳ | **bẩm sinh** |
| Khi nào | mart/BI | EDW truyền thống | nhiều nguồn, regulated, đổi nhiều |

## ⚠️ Cạm bẫy
- DV **nhiều join** → đừng cho BI query trực tiếp; build star mart phía trên.
- Over-engineer: dự án nhỏ/ít nguồn → Kimball star đủ, DV thừa phức tạp.
- Hash collision (hiếm) + chọn business key sai.

## ✅ "Tự mò"
🔭 Mô hình hoá e-commerce theo DV: hub_customer/hub_product/hub_order, link_order (customer×product×order), sat_customer (name/country lịch sử). So với star schema đã build (Phase 2) — DV nhiều bảng/join hơn nhưng audit/linh hoạt hơn.

➡️ Tiếp: [[e02-obt-wide]].
