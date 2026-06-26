# G05 — Case: Healthcare Data Platform (compliance-heavy)

> Đặc trưng: **governance & chính xác là vua**, PII cực nhạy (PHI), audit/compliance. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: tích hợp dữ liệu bệnh nhân (EHR, lab, đơn thuốc, thiết bị), phân tích lâm sàng/vận hành, hỗ trợ nghiên cứu, báo cáo tuân thủ.
- **Compliance**: **HIPAA** (Mỹ) / GDPR — PHI (Protected Health Information) cực nhạy; audit mọi truy cập; consent; quyền xoá/đính chính.
- **Consistency**: **chính xác tuyệt đối** (sai = nguy hiểm tính mạng); audit/immutability.
- **Đặc thù**: HL7/FHIR (chuẩn trao đổi y tế), bệnh án có **lịch sử** (chẩn đoán thay đổi → bitemporal).

## 2. Kiến trúc (governance-first)
```
Nguồn (EHR/HL7/FHIR, lab, devices) ──► ingest (validate + chuẩn hoá FHIR)
        │  (PHI mã hoá từ đầu)
        ▼
   BRONZE (raw, mã hoá at-rest, access chặt)
        │  de-identify / tokenize PHI cho analytics
        ▼
   SILVER: clean + FHIR conform + bitemporal (lịch sử chẩn đoán)
        │
        ▼
   GOLD: 
     - clinical analytics (de-identified)        ← analyst/researcher (KHÔNG thấy PHI)
     - operational (có PHI, access hạn chế)       ← clinician (cần PHI, audit)
Xuyên suốt: Catalog + lineage (PHI chảy đâu) · Audit log mọi truy cập · Consent management
```

## 3. ⭐ Governance & bảo mật (trọng tâm)
- **De-identification/tokenization** PHI cho analytics: tách PHI (tên/SSN/ngày sinh) ra, thay token; analyst thấy data đã ẩn danh ([[64-governance-pii]]).
- **Column/row-level security**: clinician thấy PHI bệnh nhân mình; researcher chỉ thấy de-identified. RBAC + ABAC chặt.
- **Encryption** at-rest + in-transit; key management.
- **Audit log** ⭐: ai truy cập bệnh án nào, khi nào (HIPAA bắt buộc) — immutable audit.
- **Consent**: chỉ dùng data theo đồng ý bệnh nhân; theo mục đích.
- **Lineage** (PHI chảy tới đâu) → hỗ trợ quyền xoá/đính chính + audit.

## 4. Modeling đặc thù
- **FHIR resources** (Patient, Observation, Encounter, Medication) — chuẩn hoá về model này.
- **Bitemporal** ([[e04-bitemporal]]): chẩn đoán có thể sửa hồi tố; cần "as-of valid + as-known" để tái dựng "lúc đó bác sĩ biết gì". Audit pháp lý.
- Immutability (không xoá bệnh án; sửa = bản ghi mới + audit) — như ledger ([[c07-case-fintech]]).

## 5. Scale & failure
- Scale vừa (so với clickstream) nhưng **chính xác + bảo mật > tốc độ**.
- Data quality nghiêm (sai lab/đơn thuốc = nguy hiểm) → DQ gates mạnh ([[f01-testing-strategy]]).
- Recovery idempotent; không mất bản ghi.

## 6. DQ & observability
- Validate FHIR schema/contract; range check (giá trị lab hợp lý).
- Audit completeness (mọi truy cập có log?).
- PII leak detection (PHI lọt vào dataset de-identified?).

## Câu hỏi đào sâu
- "Analyst phân tích mà không lộ PHI?" → de-identify/tokenize, row/column security, dataset tách.
- "Chẩn đoán sửa hồi tố, báo cáo cũ?" → bitemporal.
- "Quyền xoá (GDPR) vs lưu trữ y tế?" → cân bằng pháp lý; lineage để biết PHI ở đâu; xoá có kiểm soát.

## ✅ "Tự mò"
🔭 Thiết kế lớp bảo mật: dataset `patient_phi` (access hạn chế) + view `patient_deidentified` (token thay tên, tuổi nhóm thay ngày sinh) cho analyst; nghĩ audit log schema.

➡️ Tiếp: [[g06-case-ml-llm-data]].
