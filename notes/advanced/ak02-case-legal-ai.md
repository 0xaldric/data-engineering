# AK02 — Case Study: Legal AI Platform

> AI cho pháp lý: phân tích hợp đồng, RAG luật/án lệ. **Citation chính xác tuyệt đối** (trích điều luật thật, sai = hậu quả pháp lý). Cùng độ gắt y tế ([[aj05-case-healthcare-ai]]). Liên hệ [[ag02-hallucination-detection]], [[af02-case-enterprise-kb]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: hỗ trợ luật sư tra cứu luật/án lệ, rà soát hợp đồng, soạn thảo — KHÔNG thay luật sư.
- **Ràng buộc sống còn**: citation đúng (trích sai điều luật/án lệ = thua kiện), bảo mật tài liệu (privilege), giải trình.
- **Đặc thù**: văn bản DÀI (hợp đồng/luật trăm trang), ngôn ngữ chuyên ngành, cập nhật luật.

## 2. ⭐ Nguyên tắc (citation là vua)
| Nguyên tắc | Vì sao |
|-----------|--------|
| **Citation chính xác tuyệt đối** | trích điều luật/án lệ THẬT + verify tồn tại ([[ag02-hallucination-detection]] citation check) |
| **Không bịa luật** | LLM hay bịa số điều/tên vụ án → grounding nghiêm + chỉ từ corpus luật có thật |
| **Privilege/bảo mật** | tài liệu khách hàng tối mật → self-host + quyền chặt ([[ad03-privacy-compliance]]) |
| **Human (luật sư) quyết** | AI hỗ trợ, luật sư chịu trách nhiệm ([[ad04-llm-security]]) |
| **Audit** | mọi truy vấn/trích dẫn log (trách nhiệm nghề) |

## 3. Kiến trúc
```
corpus luật/án lệ (cập nhật) ─> parse văn bản dài ([[ad06-doc-parsing]]) ─> chunk theo điều/khoản
   ─> embed (model hiểu pháp lý) -> vector store + metadata (luật nào, năm, hiệu lực)
hợp đồng khách ─> [bảo mật] phân tích: trích điều khoản, rủi ro, so chuẩn
truy vấn luật sư ─> retrieve điều luật/án lệ liên quan ─> LLM phân tích + CITATION
   ─> [verify citation] điều luật trích CÓ THẬT? còn hiệu lực? -> luật sư review
```

## 4. ⭐ Citation verification (mấu chốt — chống bịa luật)
```
LLM trả lời + trích "Điều 123 Luật X"
   ─> KIỂM: điều đó CÓ trong corpus không? nội dung KHỚP không?
   ─> không khớp/không tồn tại -> CỜ BỊA -> không hiển thị / cảnh báo ([[ag02-hallucination-detection]])
   ─> còn hiệu lực không? (luật sửa đổi) -> freshness ([[ac06-kb-freshness]])
```
→ Luật sư phải click citation → ra đúng điều luật thật. Bịa citation pháp lý = thảm hoạ (đã có vụ luật sư bị phạt vì nộp án lệ AI bịa).

## 5. Đặc thù & eval
- **Văn bản dài**: chunk theo điều/khoản (cấu trúc pháp lý), giữ ngữ cảnh tham chiếu chéo.
- **Hiệu lực thời gian**: luật sửa đổi → version + effective_date ([[e04-bitemporal]], [[ac06-kb-freshness]]).
- **Eval với luật sư** (đúng pháp lý, không chỉ recall); regulatory.
- **Đa thẩm quyền**: luật khác theo quốc gia/bang → filter jurisdiction.

## Cạm bẫy (pháp lý thật)
- **Bịa điều luật/án lệ** → thua kiện + phạt → citation verification bắt buộc.
- **Trích luật hết hiệu lực** → tư vấn sai → effective_date + freshness.
- **Rò tài liệu privilege** → vi phạm nghề → self-host + quyền chặt.
- **AI tự kết luận pháp lý** → luật sư phải quyết → human-in-loop.
- **Chunk cắt giữa điều khoản** → mất ngữ cảnh → chunk theo cấu trúc pháp lý.
- **Bỏ qua jurisdiction** → áp luật sai nơi → filter thẩm quyền.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Nguyên tắc: citation tuyệt đối + không bịa luật + privilege + human quyết.
- [ ] Citation verification: điều luật trích có thật + khớp + còn hiệu lực.
- [ ] Văn bản dài: chunk theo điều/khoản; hiệu lực thời gian.
- [ ] Eval luật sư + jurisdiction filter.
- [ ] Cạm bẫy: bịa luật, luật hết hiệu lực, rò privilege.
- 🔭 Tự mò: thêm vào `ai_product.py` ([[aj03-capstone-integration]]) tầng **citation verify**: bắt mock-LLM trả "answer + note_id trích"; kiểm note_id có trong index + cosine(answer, note đó) cao; nếu trích note không tồn tại/không liên quan → CỜ BỊA, không trả. Đó là "legal-grade grounding".

➡️ Tiếp [[ak03-case-education-ai]] — case study giáo dục.
