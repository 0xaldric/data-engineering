# AK09 — AI Review 10 + Tổng Kết Vertical Case Studies

> Tổng kết **AI-Advanced 10** (AK01–AK08): bảng "ngành → nhấn gì → kỹ thuật", pattern chung vs đặc thù, tổng kết **10 batch** Module AI. Nối [[aj09-ai-review9]], [[af09-ai-review6]].

## 🏁 Batch này (AK01–AK08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AK01 | E-commerce AI | — | real-time tồn kho + cold-start + conversion |
| AK02 | Legal AI | — | citation tuyệt đối + không bịa luật |
| AK03 | Education AI | — | personalization sư phạm + an toàn trẻ em |
| AK04 | Government AI | — | minh bạch + fairness + accessibility |
| AK05 | Manufacturing/IoT AI | — | time-series edge + không tự dừng máy |
| AK06 | Data labeling | ✅ `annotation_agreement.py` | Cohen's kappa lộ annotator ẩu |
| AK07 | KG construction | — | trích triple + entity resolution |
| AK08 | Time-series/tabular FM | — | FM cho data có cấu trúc; cây vẫn vua |

→ Kho AI: **23 script chạy được** + ~100 note AI (10 batch).

## ⭐⭐ Bảng "Ngành → Nhấn gì → Kỹ thuật" (interview gold)
| Ngành | Nhấn mạnh nhất | Kỹ thuật chủ đạo |
|-------|----------------|------------------|
| **E-commerce** | real-time + conversion | search hybrid, reco, filter tồn-kho, cache |
| **Legal** | citation tuyệt đối | grounding nghiêm, citation verify, freshness luật |
| **Healthcare** ([[aj05-case-healthcare-ai]]) | an toàn + PHI | grounding tuyệt đối, self-host, human bác sĩ |
| **Finance** ([[aj06-case-finance-ai]]) | real-time + compliance | point-in-time, audit, LLM-không-tự-quyết |
| **Education** | sư phạm + an toàn trẻ | personalization độ-khó, đo tiến bộ |
| **Government** | minh bạch + công bằng | fairness audit, accessibility, đa ngữ |
| **Manufacturing** | edge + an toàn vật lý | time-series, edge, không-tự-dừng-máy |

## ⭐ Pattern CHUNG mọi ngành (khung 7 bước [[af09-ai-review6]])
```
1. clarify  -> mục tiêu + ràng buộc đặc thù ngành
2. data flow -> ingest/chunk/embed/index + freshness
3. retrieve  -> hybrid + rerank + filter (quyền/tenant)
4. SAFETY    -> guardrail + grounding + human-in-loop (mức gắt theo ngành)
5. eval      -> golden + metric (KINH DOANH theo ngành: conversion/tiến-bộ/deflection)
6. scale     -> vector DB + streaming + cache
7. cost      -> routing + cache + budget
```
→ **Khung không đổi**; mỗi ngành chỉ **chỉnh độ gắt** từng bước.

## ⭐ Trục "độ gắt an toàn" theo ngành (quan trọng)
```
THẤP ─────────────────────────────────────────> CAO
e-commerce   education   government   finance   legal   healthcare
(sai = mất    (sai = học   (sai = bất   (sai =    (sai =  (sai = tính
 đơn hàng)     sai)         công)        mất tiền) thua    mạng)
                                                   kiện)
-> càng phải: grounding nghiêm hơn, human-in-loop nhiều hơn, audit chặt hơn, không-tự-quyết
```
→ Nhận ra "ngành này gắt cỡ nào" → quyết định kiến trúc (tự động bao nhiêu, người duyệt bao nhiêu).

## ⭐ Đặc thù DATA theo ngành
- E-commerce: catalog + hành vi (real-time, cold-start).
- Legal/Healthcare: văn bản dài + privacy cực cao.
- Finance/Manufacturing: **time-series** + point-in-time ([[ak08-timeseries-tabular-fm]]).
- Government: đa ngôn ngữ + fairness.
→ "Danh từ đổi (PHI, sensor, án lệ), tư duy DE không đổi" ([[ai10-summary]]).

## 🏆 Tổng kết 10 batch Module AI
| Batch | Trọng tâm |
|-------|-----------|
| Module AI – AD | nền tảng → production (RAG/governance/eval/safety/cache) |
| AE – AF | frontier 1 + system design + scale |
| AG – AH | ops + infra (drift/agent/serving/benchmark) |
| AJ | đỉnh: reasoning/alignment/capstone-integration/flywheel |
| **AK** | **vertical case studies (7 ngành)** |
→ **10 batch · ~100 note AI · 23 script** = khoá AI-DE đầy đủ + áp dụng thực tế đa ngành.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Bảng ngành → nhấn → kỹ thuật (nói được mỗi ngành nhấn gì).
- [ ] Khung 7 bước chung; mỗi ngành chỉnh độ gắt.
- [ ] Trục độ-gắt-an-toàn (e-commerce → healthcare).
- [ ] Đặc thù data theo ngành.
- 🔭 Tự mò: chọn 1 ngành CHƯA có ở đây (vd logistics, du lịch, bất động sản, nông nghiệp), tự viết case study theo khung 7 bước — clarify ràng buộc đặc thù, đặt nó trên trục độ-gắt, chọn kỹ thuật. Đó là bài tập system-design ngành mới.

➡️ Hết AI-Advanced 10. Batch tiếp: ngành mới / đào sâu kỹ thuật / chủ đề frontier — vẫn ưu tiên AI/LLM.
