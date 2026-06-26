# B07 — Behavioral & Scenario Interview (STAR)

> Phỏng vấn DE không chỉ kỹ thuật — còn hỏi **cách bạn làm việc & xử lý tình huống**. Khung STAR giúp trả lời mạch lạc.

## ⭐ Phương pháp STAR
Trả lời câu behavioral theo 4 bước:
- **S**ituation: bối cảnh ngắn gọn (1–2 câu).
- **T**ask: nhiệm vụ/vấn đề bạn phải giải.
- **A**ction: bạn **cụ thể** đã làm gì (nhấn vai trò *bạn*, dùng "tôi").
- **R**esult: kết quả đo được (số liệu nếu có) + bài học.

> Mẹo: chuẩn bị sẵn 5–6 "câu chuyện" từ kinh nghiệm (hoặc dự án/capstone), mỗi câu xoay được nhiều câu hỏi. Kết quả nên có **con số** ("giảm thời gian pipeline 40%", "tiết kiệm $X/tháng").

## 10 câu behavioral DE hay gặp + hướng trả lời
1. **"Kể về một pipeline production bị lỗi và cách bạn xử lý."**
   → S: pipeline X lỗi lúc đêm. A: alert → đọc log/Spark UI tìm task lỗi → vì **idempotent** nên rerun/backfill khoảng ảnh hưởng → root cause (vd schema nguồn đổi) → thêm **data contract + test** ngăn tái diễn. R: khôi phục trong N phút, không tái diễn.

2. **"Lần bạn phát hiện dữ liệu sai?"**
   → A: nhận ra số dashboard lệch → dùng **lineage** lần ngược upstream → tìm bug (vd fan-out join / sai grain) → sửa + thêm **dbt test/DQ check** + backfill. R: số đúng lại, có guardrail.

3. **"Tối ưu một job chậm/đắt."**
   → A: `EXPLAIN`/Spark UI tìm nghẽn → partition/pushdown, broadcast bảng nhỏ, Parquet, incremental. R: nhanh hơn X lần / rẻ hơn $Y ([[a06-sql-optimization]], [[59-cost-finops]]).

4. **"Xung đột với stakeholder/đội khác."**
   → Nhấn: lắng nghe nhu cầu, dữ liệu/đánh đổi rõ ràng, đề xuất phương án, **data contract** để thống nhất kỳ vọng.

5. **"Deadline gấp, làm sao?"**
   → Ưu tiên (MVP trước), cắt phạm vi có chủ đích (nói rõ trade-off), giao tiếp sớm, không hy sinh test/chất lượng dữ liệu quan trọng.

6. **"Quyết định kỹ thuật khó (chọn công cụ/kiến trúc)."**
   → Nêu tiêu chí (scale, chi phí, team skill, vận hành), so sánh phương án, **vì sao chọn** + điều sẽ làm khác nếu khác bối cảnh.

7. **"Học công nghệ mới nhanh."**
   → Cách bạn học (docs, build thử nhỏ, đọc source), ví dụ cụ thể.

8. **"Sai lầm lớn nhất & bài học."**
   → Trung thực, nhấn **bài học + thay đổi quy trình** (vd thêm CI/test sau khi đẩy bug).

9. **"Cân bằng tốc độ vs chất lượng."**
   → Tuỳ ngữ cảnh: prototype có thể nhanh-bẩn; pipeline production cần test/idempotency. Biết khi nào nào.

10. **"Vì sao chọn data engineering?"**
   → Câu chuyện cá nhân chân thật + thứ bạn thích (build hệ thống, dữ liệu tin cậy, tác động).

## Câu nên HỎI NGƯỢC nhà tuyển dụng
Thể hiện sự nghiêm túc:
- Stack data hiện tại & điểm đau lớn nhất?
- Data quality/observability đang làm thế nào?
- On-call/incident cho data ra sao?
- Team cấu trúc thế nào (centralized vs embedded/data mesh)?
- Roadmap & cơ hội học/phát triển?

## ⚠️ Cạm bẫy
- Trả lời chung chung "chúng tôi đã..." → dùng "tôi", nói hành động cụ thể.
- Kể quá dài phần Situation, thiếu Action/Result.
- Không có con số kết quả.
- Đổ lỗi người khác thay vì rút bài học.

## ✅ "Tự mò"
🔭 Viết sẵn 5 câu chuyện STAR từ chính 3 capstone/project trong khoá này (pipeline lỗi, dữ liệu sai, tối ưu, quyết định Delta vs Iceberg, idempotency cứu backfill). Mỗi câu ≤ 90 giây nói.

➡️ Tiếp: [[b08-explain-senior]].
