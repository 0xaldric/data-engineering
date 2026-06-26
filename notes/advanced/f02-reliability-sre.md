# F02 — Pipeline Reliability & Incident Management (SRE cho Data)

> Áp tư duy SRE (Site Reliability Engineering) vào data: đo độ tin cậy, xử lý sự cố có quy trình. Liên hệ [[43-airflow-reliability]], [[62-observability]].

## SLI / SLO / SLA cho data
- **SLI** (Indicator): chỉ số đo được — vd freshness (gold cập nhật trong bao lâu), completeness (% record đủ), uptime pipeline, error rate.
- **SLO** (Objective): mục tiêu nội bộ — vd "gold tươi < 1h, 99% số ngày".
- **SLA** (Agreement): cam kết với người dùng (có thể kèm hậu quả nếu vi phạm) — thường lỏng hơn SLO.
- **Error budget**: 100% − SLO. Vd SLO 99% → được "sai" 1%. Hết error budget → ưu tiên ổn định hơn tính năng mới. Giúp cân bằng tốc độ vs độ tin cậy.

## Data SLI hay dùng
freshness (độ trễ data), volume (số record vs kỳ vọng), completeness, accuracy (reconciliation pass), pipeline success rate, latency end-to-end. → Đo qua observability ([[62-observability]] 5 trụ cột).

## Incident lifecycle ⭐
```
DETECT → TRIAGE → MITIGATE → RESOLVE → POSTMORTEM
```
1. **Detect**: observability/alert phát hiện (freshness miss, volume drop, test fail). Giảm **TTD** (time to detect).
2. **Triage**: mức độ nghiêm trọng (P1 tiền/báo cáo lãnh đạo sai vs P3 dashboard phụ); dùng **lineage** xác định ai bị ảnh hưởng ([[63-lineage-catalog]]).
3. **Mitigate**: giảm tác động ngay — vd dừng publish data bẩn (circuit breaker), rollback bằng **time travel** ([[34-delta-lake]]), thông báo consumer.
4. **Resolve**: sửa root cause (nguồn/logic), **backfill/replay** khoảng ảnh hưởng (idempotent → an toàn — [[40-pipeline-patterns]]). Giảm **TTR** (time to resolve).
5. **Postmortem**: **blameless** — phân tích vì sao, thêm test/contract/alert ngăn tái diễn.

## On-call cho data
- Rotation, runbook, escalation. Alert phải **hành động được** (ai làm gì), tránh fatigue.
- Severity levels + response time tương ứng.

## Runbook (sổ tay xử lý)
Tài liệu "khi X xảy ra thì làm Y": vd "pipeline orders fail → kiểm CDC connector → nếu schema đổi, cập nhật contract → backfill từ Kafka offset Z". Giảm TTR, ai on-call cũng xử được.

## Thiết kế để reliable (phòng > chữa)
- **Idempotency** (rerun/backfill an toàn) — nền tảng.
- **Retry + backoff** lỗi tạm thời ([[43-airflow-reliability]]).
- **Atomic publish** (staging→swap) → consumer không thấy data nửa vời.
- **Dead-letter queue** cho bad records (không chặn cả pipeline).
- **DQ gates** chặn data bẩn lan ([[f01-testing-strategy]]).
- **Replayability** (giữ raw/Kafka retention → tính lại được).

## Blameless postmortem
Tập trung **hệ thống/quy trình** sai ở đâu, không đổ lỗi cá nhân → người ta dám báo cáo sự cố thật → học được. Output: action items (thêm test, sửa runbook, cải tiến alert).

## ⚠️ Cạm bẫy
- Chỉ alert "job fail", bỏ qua data đúng/tươi (job success vẫn ra rác).
- Alert quá nhiều → fatigue → bỏ lỡ sự cố thật.
- Không runbook → mỗi sự cố tự mò, TTR dài.
- Postmortem đổ lỗi → che giấu sự cố.
- Recovery không idempotent → backfill nhân đôi.

## ✅ "Tự mò"
🔭 Viết runbook cho 1 sự cố giả định pipeline e-commerce (CDC orders fail vì schema đổi): các bước detect→mitigate→resolve→postmortem + action items. Định nghĩa 3 SLO (freshness/volume/success rate).

➡️ Tiếp: [[f03-modern-data-stack]].
