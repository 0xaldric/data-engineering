# 🏁 Module F — Tổng kết: DataOps, Architecture & Career

> Module cuối ADVANCED.md. Vận hành, tổ chức, và phát triển nghề — phần "phi-coding" phân biệt senior DE.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| F01 | Data testing strategy | [f01](f01-testing-strategy.md) |
| F02 | Reliability & incident (SRE) | [f02](f02-reliability-sre.md) |
| F03 | Modern data stack & chọn tool | [f03](f03-modern-data-stack.md) |
| F04 | Cost optimization cases | [f04](f04-cost-cases.md) |
| F05 | Data mesh & team topology | [f05](f05-data-mesh.md) |
| F06 | DataOps & CI/CD | [f06](f06-dataops.md) |
| F07 | Career roadmap | [f07](f07-career-roadmap.md) |

## 📑 Cheat-Sheet
- **Testing**: kim tự tháp (unit→schema→DQ→integration→e2e); test code **và** data; shift-left.
- **Reliability**: SLI/SLO/error budget; incident detect→triage→mitigate→resolve→postmortem (blameless); runbook; idempotent recovery.
- **MDS**: modular best-of-breed quanh warehouse; build vs buy theo scale/skill/cost; tránh tool sprawl.
- **Cost**: quét ít (Parquet+partition+cột) → 90–99%; auto-suspend; compaction; incremental; FinOps audit.
- **Data mesh**: 4 nguyên tắc (domain ownership, data as product, self-serve, federated governance); chỉ khi scale lớn (đừng hype).
- **DataOps**: automation + test/monitor + version everything; CI/CD đầy đủ; blue-green data deploy.
- **Career**: scope of impact (task→hệ thống→tổ chức); T-shaped; concept > tool; AI/LLM dịch DE lên thiết kế/giám sát.

## ✅ Self-assessment Module F
- [ ] Thiết kế chiến lược test cho 1 pipeline (kim tự tháp).
- [ ] Định nghĩa SLO + viết runbook incident.
- [ ] Vẽ MDS + build vs buy; tránh tool sprawl.
- [ ] Áp đòn bẩy cost với số liệu.
- [ ] Giải thích data mesh & khi nào KHÔNG dùng.
- [ ] Biết cần gì để lên cấp tiếp.

## ➡️ Hết ADVANCED.md (6 module A–F)
Theo PROTOCOL bước 5, các batch sau sẽ **đào sâu**: bộ bài tập SQL mới (set 3+), case study system design mới (log analytics, gaming, healthcare, ML platform...), hoặc đào sâu chủ đề bất kỳ. Xem [[00-INDEX]].
