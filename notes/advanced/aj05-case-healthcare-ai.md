# AJ05 — Case Study: Healthcare AI Data Platform

> Thiết kế RAG/AI cho y tế — nơi **sai = nguy hiểm tính mạng** và **privacy là luật**. Đề system-design nhấn mạnh an toàn + grounding tuyệt đối + privacy. Liên hệ [[ad03-privacy-compliance]], [[ag02-hallucination-detection]], [[af01-case-support-ai]].

## 1. Làm rõ yêu cầu (ràng buộc gắt nhất)
- **Mục tiêu**: hỗ trợ bác sĩ/bệnh nhân tra cứu y văn, tóm tắt hồ sơ, gợi ý (KHÔNG tự chẩn đoán thay bác sĩ).
- **Ràng buộc sống còn**: KHÔNG bịa (sai thuốc/liều = chết người), privacy PHI tuyệt đối (HIPAA/luật), giải trình được.
- **Người dùng**: bác sĩ (chuyên môn cao) + bệnh nhân (cần đơn giản, an toàn).

## 2. ⭐ Nguyên tắc thiết kế (an toàn là số 1)
| Nguyên tắc | Vì sao |
|-----------|--------|
| **Grounding tuyệt đối** | mọi câu phải bám y văn có thật + **citation** (bác sĩ kiểm) ([[ag02-hallucination-detection]]) |
| **Không chắc → từ chối** | thà nói "tham khảo bác sĩ" còn hơn bịa ([[aj02-ai-alignment]] refusal) |
| **Human-in-loop bác sĩ** | AI gợi ý, **bác sĩ quyết** — không tự hành động ([[ad04-llm-security]] excessive agency) |
| **Self-host** | PHI không ra API ngoài ([[ad03-privacy-compliance]]) |
| **Audit đầy đủ** | mọi truy vấn/gợi ý log được (pháp lý) |

## 3. Kiến trúc
```
y văn (guideline, paper, drug DB) ─> parse ([[ad06-doc-parsing]]) ─> chunk ─> embed
   ─> vector store self-host (PHI tách riêng, mã hoá [[ad03-privacy-compliance]])
hồ sơ bệnh nhân (PHI) ─> [tách + kiểm soát quyền chặt] ─> chỉ bác sĩ điều trị xem
truy vấn bác sĩ ─> [guardrail PHI] ─> retrieve y văn + (nếu có quyền) hồ sơ
   ─> generate + CITATION bắt buộc ─> [grounding check NGHIÊM] ─> bác sĩ review ─> quyết định
   ─> audit log (ai hỏi gì, AI gợi gì, bác sĩ quyết gì)
```

## 4. ⭐ Privacy PHI (gắt hơn mọi domain)
- **PHI** (Protected Health Info): tên, bệnh, thuốc, ảnh y tế → mã hoá, kiểm soát quyền theo vai (bác sĩ điều trị) ([[af02-case-enterprise-kb]] permission-aware).
- **De-identification**: bỏ định danh khi dùng cho nghiên cứu/train ([[ad03-privacy-compliance]] differential privacy).
- **Self-host bắt buộc** (đa số): không gửi PHI ra API ngoài.
- **Audit + consent**: bệnh nhân đồng ý, log mọi truy cập (pháp lý).

## 5. ⭐ Eval đặc thù (sai số khác support thường)
- **False negative nguy hiểm** (bỏ sót cảnh báo tương tác thuốc) → recall an toàn cao.
- **Hallucination = không chấp nhận** → grounding tuyệt đối + bác sĩ verify.
- **Eval với chuyên gia y tế** (không chỉ metric tự động) → đúng lâm sàng.
- **Regulatory** (FDA/CE cho medical device AI) → cao hơn eval thường.

## Cạm bẫy (sinh tử)
- **Để AI tự chẩn đoán/kê đơn** → nguy hiểm + pháp lý → AI gợi ý, bác sĩ quyết.
- **Bịa/không citation** → bác sĩ tin nhầm → grounding tuyệt đối + citation bắt buộc.
- **PHI ra API ngoài** → vi phạm HIPAA → self-host + redact.
- **Quyền lỏng** (bác sĩ A xem bệnh nhân B không liên quan) → permission-aware chặt.
- **Eval chỉ metric tự động** → bỏ lỡ sai lâm sàng → chuyên gia review.
- **Over-refuse mọi câu** → vô dụng → cân bằng (giúp tra cứu, từ chối chẩn đoán).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Ràng buộc y tế: không bịa, PHI privacy, giải trình.
- [ ] Nguyên tắc: grounding tuyệt đối + citation + human-in-loop + self-host + audit.
- [ ] PHI: mã hoá, permission-aware, de-id, consent.
- [ ] Eval: recall an toàn cao, chuyên gia review, regulatory.
- [ ] Cạm bẫy: AI tự chẩn đoán, PHI ra ngoài, quyền lỏng.
- 🔭 Tự mò: lấy `ai_product.py` ([[aj03-capstone-integration]]), tăng `CONF_MIN` rất cao + bắt buộc citation (chỉ trả lời nếu top-score cao VÀ có nguồn) + thêm câu "đây là tham khảo, hỏi bác sĩ"; thử câu y tế bịa → xác nhận nó ESCALATE thay vì trả lời. Đó là "safety-first" mode.

➡️ Tiếp [[aj06-case-finance-ai]] — case study tài chính.
