# AL05 — Case Study: HR/Recruiting AI (bias-critical)

> AI tuyển dụng: sàng lọc CV, match ứng viên-JD, tóm tắt phỏng vấn. **CỰC nhạy bias** — phân biệt đối xử = pháp lý + đạo đức. Nhấn: fairness audit nghiêm + human quyết + explainability. Liên hệ [[af06-ai-data-governance]], [[ak04-case-govt-ai]], [[aj02-ai-alignment]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: lọc nhanh nhiều CV, match đúng kỹ năng, giảm tải tuyển dụng.
- **Ràng buộc SỐNG CÒN**: **không phân biệt đối xử** (giới/tuổi/chủng tộc/vùng — pháp lý nghiêm), minh bạch (giải trình loại/chọn), không tự loại ứng viên.
- **Đặc thù**: dữ liệu lịch sử tuyển dụng **mang sẵn bias** (công ty xưa tuyển lệch) → AI học sẽ khuếch đại.

## 2. ⭐⭐ Bias là rủi ro số 1 (bài học Amazon)
```
data lịch sử: công ty xưa tuyển nam nhiều cho kỹ thuật
   -> AI học "nam = phù hợp hơn" -> loại CV nữ (kể cả gián tiếp: trường nữ, CLB nữ)
   -> phân biệt đối xử + kiện tụng (Amazon đã phải bỏ tool tuyển dụng AI vì lý do này)
```
→ **AI khuếch đại bias trong data** ([[ab01-synthetic-data]]). Phải:
- **Audit bias**: đo tỉ lệ pass/loại theo nhóm nhạy cảm → phát hiện lệch ([[af06-ai-data-governance]]).
- **Bỏ proxy bias**: tên/giới/tuổi/trường → có thể là proxy → cân nhắc loại khỏi feature.
- **Eval fairness**: đảm bảo chất lượng ĐỀU giữa nhóm ([[ak04-case-govt-ai]]).

## 3. ⭐ Nguyên tắc thiết kế (an toàn pháp lý)
| Nguyên tắc | Vì sao |
|-----------|--------|
| **Human quyết, AI hỗ trợ** | không để AI tự loại → người chịu trách nhiệm ([[ad04-llm-security]]) |
| **Explainability** | giải trình "vì sao match/không" bằng kỹ năng THẬT, không proxy |
| **Fairness audit** | đo bias theo nhóm định kỳ; mitigate |
| **Transparency** | ứng viên biết AI tham gia + quyền khiếu nại |
| **EU AI Act high-risk** | tuyển dụng = high-risk → governance chặt ([[af06-ai-data-governance]]) |

## 4. Kiến trúc
```
CV + JD ─> parse ([[ad06-doc-parsing]]) ─> trích kỹ năng/kinh nghiệm (structured)
   ─> match: kỹ năng ứng viên vs JD (embedding + rule) — KHÔNG dùng proxy nhạy cảm
   ─> [fairness check] tỉ lệ pass theo nhóm có lệch? -> cảnh báo
   ─> gợi ý xếp hạng + GIẢI THÍCH (kỹ năng nào khớp) -> NGƯỜI tuyển quyết
   ─> audit: mọi quyết định log (pháp lý)
```

## Cạm bẫy (pháp lý + đạo đức)
- **AI tự loại ứng viên** → phân biệt + kiện → human quyết.
- **Học bias từ data lịch sử** → khuếch đại → audit + de-bias + bỏ proxy.
- **Proxy bias ẩn** (trường/CLB/tên = giới/chủng tộc) → vẫn phân biệt gián tiếp → kiểm proxy.
- **Không explainability** → không giải trình loại → giải thích bằng kỹ năng thật.
- **Không fairness audit** → bias âm thầm → đo theo nhóm định kỳ.
- **Match chỉ keyword CV** → bỏ ứng viên diễn đạt khác → semantic + cẩn thận bias.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Bias = rủi ro #1 (AI khuếch đại data lịch sử — bài học Amazon).
- [ ] Audit bias theo nhóm + bỏ proxy + eval fairness.
- [ ] Human quyết + explainability + transparency + high-risk governance.
- [ ] Kiến trúc: match kỹ năng (không proxy) + fairness check + audit.
- [ ] Cạm bẫy: AI tự loại, học bias, proxy ẩn, không audit.
- 🔭 Tự mò: tạo 20 "CV" giả gắn nhãn nhóm (A/B) + điểm kỹ năng; "model" xếp hạng theo kỹ năng; đo tỉ lệ top-10 theo nhóm → nếu lệch dù kỹ năng tương đương = bias; thử thêm 1 "proxy" tương quan nhóm xem nó làm lệch thế nào (bài học proxy bias).

➡️ Tiếp [[al06-mock-interview-2]] — mock phỏng vấn 2.
