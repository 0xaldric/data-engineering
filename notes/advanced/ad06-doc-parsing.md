# AD06 — Document Parsing & Extraction sâu

> "Rác vào, rác ra": chất lượng RAG **bắt đầu từ khâu PARSE**, không phải embedding. Parse hỏng → chunk sai → retrieve sai → mọi thứ sau vô nghĩa. Khâu ít hào nhoáng nhưng quyết định nhất. Liên hệ [[ai03-chunking]], [[aa08-multimodal]].

## Vì sao parse là nền móng
- Tài liệu thật **bẩn**: PDF scan, bảng phức tạp, nhiều cột, header/footer, watermark, công thức, code.
- Parse cẩu thả → text dính liền, mất cấu trúc, bảng vỡ thành chuỗi vô nghĩa → chunk theo đó càng sai.
- **Garbage in, garbage out**: embedding xịn cỡ nào cũng không cứu được text parse hỏng.
- → Đầu tư vào parse thường cho ROI cao hơn tinh chỉnh model.

## ⭐ Thử thách theo định dạng
| Định dạng | Khó ở đâu | Cách xử lý |
|-----------|-----------|------------|
| **PDF (text)** | thứ tự đọc (multi-column), header/footer lặp | layout-aware parser (giữ thứ tự, bỏ boilerplate) |
| **PDF (scan)** | ảnh, không có text | **OCR** (Tesseract/cloud) → text + độ tin |
| **Bảng** | cấu trúc 2D → flatten mất nghĩa | table extraction → giữ quan hệ hàng/cột (markdown/HTML table) |
| **HTML** | thẻ, nav, quảng cáo lẫn nội dung | bóc main content, bỏ boilerplate |
| **DOCX** | style, track-changes, comment | đọc theo cấu trúc đoạn/heading |
| **Code** | ngữ cảnh theo hàm/khối | chunk theo ranh giới cú pháp, không cắt giữa hàm |
| **Công thức/biểu đồ** | toán/hình | LaTeX/alt-text; ảnh → multimodal ([[aa08-multimodal]]) |

## ⭐ Giữ CẤU TRÚC cho chunking (mấu chốt)
Parse tốt = **giữ được cấu trúc logic** để chunk theo nó ([[ai03-chunking]] structure-aware):
```
PDF/HTML thô
   ─> parse ─> [heading H1/H2, đoạn, list, bảng, code block] có ranh giới
   ─> chunk theo heading + size (không cắt giữa câu/bảng)
   ─> mỗi chunk mang metadata: nguồn, trang, heading, loại (text/table/code)
```
- Mất heading → không chunk structure-aware được → chunk cắt bừa → ngữ cảnh vỡ.
- Bảng nên giữ nguyên khối + có caption → embed cả ngữ cảnh "bảng này về gì".

## Pipeline parse → clean → normalize
```
raw file
 ─> [1 parse] đúng định dạng (PDF/HTML/OCR...) -> text + cấu trúc + metadata
 ─> [2 clean] bỏ boilerplate (header/footer/nav), sửa lỗi OCR, gộp dòng vỡ
 ─> [3 normalize] unicode, khoảng trắng, encoding, ngày/số chuẩn
 ─> [4 enrich] gắn metadata (nguồn, trang, ngôn ngữ, loại) -> sẵn sàng chunk
```
Đây là **ETL cho tài liệu** — đúng tư duy DE (extract → clean → normalize → load).

## Công cụ (biết tên)
- Layout/PDF: **unstructured.io**, PyMuPDF, pdfplumber, Docling, LlamaParse.
- OCR: Tesseract, PaddleOCR, cloud OCR.
- HTML: trafilatura, readability, BeautifulSoup.
→ Bản chất: biến tài liệu bẩn → text sạch + có cấu trúc + metadata.

## ⭐ Đo chất lượng parse (đừng tin mù)
- **Spot-check**: mở vài chunk ngẫu nhiên — đọc có nghĩa không? bảng còn nguyên không?
- **Coverage**: % tài liệu parse được (OCR fail? trang trống?).
- **Retrieval downstream**: parse tốt lên → recall@k tốt lên ([[ab02-rag-eval-harness]]) → đo bằng harness.
- Lỗi parse **âm thầm**: không crash, chỉ ra text vô nghĩa → phải chủ động kiểm.

## Cạm bẫy
- **Coi parse là "đọc text xong"** → bỏ qua cấu trúc/bảng → chunk vỡ.
- **PDF multi-column đọc sai thứ tự** → câu trộn lẫn vô nghĩa → layout-aware parser.
- **OCR không kiểm độ tin** → text rác lẫn vào → lọc theo confidence.
- **Giữ boilerplate** (header/footer lặp mọi trang) → nhiễu retrieval → bóc bỏ.
- **Bảng flatten thành chuỗi** → mất quan hệ → giữ markdown/HTML table.
- **Không đo parse** → lỗi âm thầm phá RAG mà không biết → spot-check + harness.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao parse là nền móng RAG ("rác vào rác ra").
- [ ] Thử thách theo định dạng (PDF text/scan, bảng, HTML, code).
- [ ] Giữ cấu trúc (heading/bảng) để chunk structure-aware.
- [ ] Pipeline parse→clean→normalize→enrich = ETL tài liệu.
- [ ] Đo parse: spot-check + coverage + retrieval downstream.
- 🔭 Tự mò: lấy 1 PDF có bảng, parse bằng `pymupdf` và `pdfplumber`, so text ra — xem bảng/thứ tự đọc khác nhau thế nào; chunk cả hai bản, embed, chạy `rag_eval_harness.py` style để thấy parse tốt → retrieve tốt hơn.

➡️ Tiếp [[ad07-agent-data]] — hạ tầng data cho agent production.
