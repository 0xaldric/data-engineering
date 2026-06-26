# F05 — Data Mesh, Data Products & Team Topology

> Cách **tổ chức** dữ liệu ở quy mô lớn (không phải công nghệ). Data mesh là paradigm tổ chức gây tranh luận — hiểu để biết khi nào hợp (và khi nào hype).

## Vấn đề: data team tập trung thành nút thắt
Mô hình truyền thống: một **central data team** lo mọi pipeline cho mọi domain → quá tải, không hiểu sâu domain, thành bottleneck, chất lượng giảm khi scale. Data mesh đề xuất **phân quyền**.

## ⭐ 4 nguyên tắc Data Mesh (Zhamak Dehghani)
1. **Domain ownership**: mỗi domain (sales, marketing, payments) **sở hữu** data của mình (ai hiểu nhất thì làm), thay vì central team.
2. **Data as a product**: data được đối xử như **sản phẩm** — có owner, SLA, documentation, discoverable, đáng tin (không phải "byproduct" của app).
3. **Self-serve data platform**: nền tảng chung (central) cung cấp công cụ để domain tự build/deploy data product mà không cần chuyên gia hạ tầng.
4. **Federated computational governance**: chuẩn chung (security, quality, interoperability, **data contracts**) áp **tự động** xuyên domain, nhưng domain tự quản trong khuôn khổ.

## Data Product là gì?
Một dataset được đóng gói như sản phẩm:
- **Discoverable** (trong catalog), **addressable** (địa chỉ rõ), **trustworthy** (SLA + DQ), **self-describing** (schema + docs), **interoperable** (chuẩn chung), **secure**.
- Có **owner** chịu trách nhiệm, **data contract** với consumer ([[61-data-contracts]]).
- VD: "customer 360" do domain Customer sở hữu, SLA freshness 1h, schema versioned.

## Team Topology
| Mô hình | Mô tả | Khi nào |
|---------|-------|---------|
| **Centralized** | 1 data team lo tất cả | nhỏ, ít domain — đơn giản, nhất quán |
| **Embedded** | DE nhúng trong từng product team | vừa — gần domain hơn |
| **Hub & spoke** | central platform + analyst/DE trong domain | phổ biến — cân bằng |
| **Data Mesh** | domain tự sở hữu data product + central platform | **lớn, nhiều domain**, central thành bottleneck |

## ⚠️ Khi nào KHÔNG nên data mesh (chống hype)
- **Tổ chức nhỏ/vừa**: centralized đơn giản hơn, mesh thừa phức tạp + overhead governance.
- Chưa có **self-serve platform** chín → phân quyền = hỗn loạn (mỗi domain làm một kiểu).
- Chưa có văn hoá ownership/contract.
→ Data mesh là **giải pháp tổ chức cho vấn đề scale**, không phải "công nghệ mới phải theo". Nhiều nơi áp nửa vời → thất bại. Bắt đầu centralized, tiến tới hub-spoke, chỉ mesh khi thực sự cần.

## Vai trò data contract trong mesh
Khi domain tự sở hữu & trao đổi data product → **contract** ([[61-data-contracts]]) là keo dán: đảm bảo interface ổn định giữa domain, governance tự động (schema/quality/SLA) → tránh "phân quyền thành hỗn loạn".

## ⚠️ Cạm bẫy
- Áp data mesh khi chưa đủ scale/maturity → overhead governance > lợi ích.
- "Mesh" không có self-serve platform → mỗi domain reinvent, không nhất quán.
- Bỏ governance liên domain → data silo + không interoperable.
- Coi mesh là vấn đề công nghệ (mua tool) thay vì tổ chức/văn hoá.

## ✅ "Tự mò"
🔭 Cho một công ty giả định (5 domain, central data team quá tải): phác chuyển từ centralized → hub-spoke → có nên mesh không? Định nghĩa 1 "data product" (customer 360) với owner/SLA/contract.

➡️ Tiếp: [[f06-dataops]].
