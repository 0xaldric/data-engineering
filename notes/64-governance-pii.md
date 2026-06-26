# 64 — Governance, PII, GDPR & Security

> Dữ liệu là tài sản **và** trách nhiệm pháp lý. DE phải bảo vệ dữ liệu nhạy cảm và tuân thủ luật — không chỉ "làm cho chạy".

## Data Governance là gì?
Khung **chính sách + quy trình + vai trò** đảm bảo dữ liệu: chính xác, an toàn, tuân thủ, dùng đúng. Gồm: ownership (ai sở hữu), quality ([[60-data-quality]]), security/quyền, compliance, catalog/lineage ([[63-lineage-catalog]]), lifecycle (giữ/xoá).

## PII & phân loại dữ liệu ⭐
- **PII** (Personally Identifiable Information): tên, email, điện thoại, địa chỉ, CMND, IP, vị trí... Trong dataset e-commerce: `name`, `email`, `city` là PII.
- **Phân loại** mức nhạy cảm: public / internal / confidential / **restricted (PII/PHI/PCI)**. Gắn tag để áp chính sách (mã hoá, hạn chế truy cập, audit).
- **Data minimization**: chỉ thu thập/giữ những gì **thực sự cần**.

## Bảo vệ dữ liệu nhạy cảm
| Kỹ thuật | Mô tả | Khi dùng |
|----------|-------|----------|
| **Encryption at-rest** | mã hoá dữ liệu trên đĩa/S3 | luôn (mặc định bật) |
| **Encryption in-transit** | TLS khi truyền | luôn |
| **Masking** | che một phần (`a***@gmail.com`) | hiển thị cho user ít quyền |
| **Tokenization** | thay PII bằng token, map giữ riêng | cần dùng nhưng không lộ giá trị |
| **Hashing/pseudonymization** | hash định danh (giữ join được, ẩn giá trị) | analytics trên PII |
| **Aggregation** | chỉ lộ số tổng hợp | báo cáo |

## Access control
- **RBAC** (role-based): cấp quyền theo vai trò (analyst đọc gold, không đọc raw PII).
- **ABAC** (attribute-based): theo thuộc tính (team, region, độ nhạy cảm).
- **Row-level / column-level security**: cùng bảng, mỗi user thấy phần được phép (cột PII ẩn với analyst; chỉ thấy row của region mình).
- **Least privilege** ([[55-cloud-fundamentals]]) + **audit log** (ai truy cập gì khi nào).

## GDPR / Compliance ⭐
Luật bảo vệ dữ liệu (GDPR-EU, CCPA-California, PDPA, Nghị định 13 ở VN...). DE cần hỗ trợ:
- **Consent**: chỉ xử lý khi có đồng ý; theo dõi mục đích.
- **Right to access**: xuất mọi dữ liệu của một người.
- **Right to be forgotten** ⭐: **xoá** dữ liệu một người khi yêu cầu → khó với hệ phân tán (dữ liệu ở lake/warehouse/backup/Kafka). Cần lineage ([[63-lineage-catalog]]) để biết PII ở đâu; table format hỗ trợ DELETE (Delta/Iceberg — [[34-delta-lake]]).
- **Data residency**: dữ liệu phải ở đúng region/quốc gia ([[55-cloud-fundamentals]]).
- **Retention policy**: giữ bao lâu rồi xoá (lifecycle).

## Trong pipeline (thực hành)
- Tag cột PII trong catalog/contract; mask/hash ở tầng **silver/gold** cho consumer thường, giữ raw PII hạn chế truy cập.
- Không **log** PII ([[13-logging-config]] redact); không đẩy PII vào nơi không kiểm soát.
- Tách dataset PII riêng + quyền chặt; cung cấp view đã mask cho số đông.

## ⚠️ Cạm bẫy
- Lộ PII trong log/notebook/dataset chia sẻ.
- Bucket S3/quyền quá rộng → rò rỉ ([[55-cloud-fundamentals]]).
- Không xoá được dữ liệu khi có yêu cầu (right to be forgotten) vì không biết PII nằm đâu.
- Copy PII vô tội vạ sang nhiều bảng/môi trường → bề mặt rủi ro lớn.
- Coi governance là "việc của team khác" — DE là người chạm dữ liệu, trách nhiệm trực tiếp.

## ✅ Tự kiểm tra & "tự mò"
- [ ] PII là gì; phân loại & data minimization.
- [ ] Masking/tokenization/hashing/encryption — khi nào dùng.
- [ ] RBAC/ABAC, row/column-level security, least privilege, audit.
- [ ] GDPR: consent, right to access/erasure, residency, retention; vì sao erasure khó.
- [ ] Thực hành PII trong pipeline (tag, mask ở gold, không log).
- 🔭 *Tự mò:* trong dbt project, tạo view `dim_customer_masked` che email (`regexp_replace`) + chỉ giữ thành phố; nghĩ xem ai được đọc bảng gốc vs view masked.

➡️ Tiếp: [[00-phase8-summary]].
