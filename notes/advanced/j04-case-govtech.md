# J04 — Case: GovTech / Public Data Platform

> Dữ liệu nhà nước: tích hợp nhiều nguồn, **privacy + governance + độ tin cậy** là trọng tâm. Khung [[c01-system-design-framework]]. Liên hệ [[e01-data-vault]], [[64-governance-pii]].

## 1. Requirements
- **Functional**: tích hợp dữ liệu liên ngành (dân cư/census, thuế, y tế công, giáo dục, giao thông); báo cáo chính sách; open data (công khai cho dân/nghiên cứu); phát hiện gian lận trợ cấp.
- **Consistency**: chính xác (quyết định chính sách), **audit + lineage** đầy đủ, **privacy** (PII công dân cực nhạy).
- **Compliance**: luật bảo vệ dữ liệu cá nhân, minh bạch, lưu trữ lâu dài.
- **Đặc thù**: nhiều nguồn không đồng bộ/schema khác nhau, chất lượng nguồn không đều, master data (1 công dân ở nhiều hệ).

## 2. Kiến trúc
```
Nguồn liên ngành (thuế, dân cư, y tế...) ──► ingest (mỗi nguồn schema khác)
        │
        ▼
   RAW VAULT (Data Vault: hub công dân/doanh nghiệp + link + satellite per nguồn)
        │  → audit/lineage bẩm sinh, thêm nguồn không phá cũ
        ▼
   BUSINESS VAULT (áp rule, MDM: hợp nhất công dân across nguồn)
        │
        ┌──────────────┼───────────────┐
        ▼ internal      ▼               ▼ public
   báo cáo chính sách  fraud (trợ cấp)  OPEN DATA (de-identified, aggregate)
   (có PII, access chặt)               công khai cho dân/nghiên cứu
```

## 3. ⭐ Vì sao Data Vault hợp govtech
- **Nhiều nguồn, schema đổi, audit**: Data Vault ([[e01-data-vault]]) — hub (business key công dân) + satellite per nguồn → thêm nguồn = thêm satellite, không phá; audit/lineage bẩm sinh (record_source + load_ts); regulated-friendly.
- **MDM** (Master Data Management): cùng công dân ở thuế/dân cư/y tế → resolve về một entity (hub) — matching/dedup khó (tên/địa chỉ khác nhau).

## 4. ⭐ Privacy & Open Data
- **Hai lớp**: internal (có PII, access chặt RBAC + audit — [[g05-case-healthcare]]) vs **open data** (de-identified + aggregate, công khai).
- **De-identification/anonymization**: bỏ PII; **k-anonymity** (mỗi nhóm ≥k người để không nhận diện được); differential privacy cho thống kê công khai.
- **Re-identification risk**: gộp nhiều dataset open có thể nhận diện lại → cẩn thận (đó là lý do aggregate + suppress nhóm nhỏ).
- Consent & purpose limitation; minh bạch (dân biết data dùng làm gì).

## 5. Tech & DQ
- Lineage/catalog nặng (data chảy đâu, dùng gì — minh bạch + audit).
- DQ nghiêm (nguồn chất lượng không đều → cleaning + validate mạnh).
- Lưu trữ dài hạn, bất biến cho audit.

## 6. Đặc thù
- Độ tin cậy & minh bạch là yêu cầu chính trị/pháp lý, không chỉ kỹ thuật.
- Open data: format chuẩn (CSV/JSON/API), documentation, versioning.

## Câu hỏi đào sâu
- "Tích hợp nhiều nguồn schema khác, audit?" → Data Vault (hub/link/sat) + MDM.
- "Công khai data mà không lộ cá nhân?" → de-identify + aggregate + k-anonymity + suppress nhóm nhỏ.
- "Re-identification từ nhiều open dataset?" → aggregate, differential privacy, giới hạn chi tiết.

## ✅ "Tự mò"
🔭 Mô hình hoá "công dân" theo Data Vault với 2 nguồn (thuế, y tế) — hub_citizen + 2 satellite; tạo open dataset aggregate (count theo region, suppress nhóm <5 người).

➡️ Tiếp: [[j05-streaming-eos]].
