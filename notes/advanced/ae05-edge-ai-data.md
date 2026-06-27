# AE05 — On-device / Edge AI Data

> AI chạy **ngay trên thiết bị** (điện thoại, IoT, trình duyệt) thay vì gọi server. Đổi lại cách làm data: model nhỏ/lượng tử hoá, eval phân tán, update OTA, federated. Liên hệ [[ad03-privacy-compliance]], [[c04-case-iot]], [[ac08-ai-cost-scale]].

## ⭐ Vì sao chạy AI trên thiết bị (4 động lực)
| Động lực | Giải thích |
|----------|-----------|
| **Privacy** | data **không rời thiết bị** → không gửi PII ra server ([[ad03-privacy-compliance]]) |
| **Latency** | không round-trip mạng → phản hồi tức thì |
| **Offline** | chạy không cần mạng (vùng sóng yếu, IoT xa) |
| **Cost** | không trả tiền API/server mỗi request → rẻ ở scale lớn |
→ Đánh đổi: thiết bị **yếu** (CPU/RAM/pin) → model phải **nhỏ + tối ưu**.

## ⭐ Làm model vừa thiết bị
| Kỹ thuật | Ý tưởng | (đã gặp ở) |
|----------|---------|-----------|
| **Quantization** | float32 → int8/int4, giảm RAM + nhanh | [[ab07-vector-search-opt]] |
| **Distillation** | model lớn dạy model nhỏ làm 1 task | [[ac08-ai-cost-scale]] |
| **Pruning** | bỏ trọng số ít quan trọng | — |
| **Model nhỏ chuyên** | model bé cho 1 việc thay LLM khổng lồ | — |
| **Runtime tối ưu** | ONNX/GGUF/Core ML/TFLite chạy hiệu quả trên thiết bị | fastembed dùng ONNX! |
> 💡 **fastembed** (capstone dùng) chính là edge-friendly: ONNX, không cần GPU/torch/API → chạy được trên máy yếu. Embedding **local** là một dạng edge AI.

## ⭐ Thách thức DATA đặc thù edge
```
SERVER AI: 1 model trung tâm, data về 1 chỗ, dễ eval/update
EDGE AI:   N thiết bị, data PHÂN TÁN, mỗi cái 1 trạng thái -> khó hơn nhiều
```
| Thách thức | Vấn đề |
|-----------|--------|
| **Model update (OTA)** | đẩy model mới tới triệu thiết bị; versioning; rollback khi lỗi |
| **Eval phân tán** | không thấy data thiết bị (privacy) → đo chất lượng kiểu gì? (metric tổng hợp ẩn danh) |
| **Data sync** | kết quả/feedback từ thiết bị → gửi về (khi online) → tổng hợp |
| **Drift cục bộ** | mỗi thiết bị/người dùng phân phối khác → model lệch theo |
| **Tài nguyên** | pin/nhiệt/RAM → giới hạn tần suất chạy |

## ⭐ Federated Learning (khái niệm)
Train model **không gom data về trung tâm** (data ở lại thiết bị):
```
server gửi model ─> mỗi thiết bị train trên data CỦA NÓ (local)
   ─> gửi VỀ chỉ GRADIENT/cập nhật (không gửi data thô)
   ─> server tổng hợp (average) ─> model mới ─> lặp
```
- **Privacy**: data thô không rời thiết bị ([[ad03-privacy-compliance]]) — chỉ gradient đi.
- Kết hợp **differential privacy** (thêm nhiễu vào gradient) để không suy ngược ra cá nhân.
- Thách thức: thiết bị không đồng nhất, online/offline thất thường, gradient cũng có thể rò chút thông tin.

## Vai trò DE
- **Pipeline OTA**: đóng gói + version + rollout model (canary/blue-green [[f06-dataops]]) tới thiết bị.
- **Thu metric ẩn danh**: đo chất lượng/usage không lấy data thô (aggregate + DP).
- **Sync layer**: nhận feedback/kết quả khi thiết bị online → tổng hợp → cải tiến.
- **Embedding/inference local**: chuẩn bị model nhỏ (quantize/distill) + runtime (ONNX) cho thiết bị.

## Cạm bẫy
- **Nhồi model to lên thiết bị yếu** → chậm/nóng/hết pin → phải quantize/distill.
- **OTA không rollback** → đẩy model lỗi → triệu thiết bị hỏng → cần canary + rollback.
- **Eval mù** (không thấy data) → không biết model edge tốt không → metric ẩn danh + spot-check opt-in.
- **Federated nhưng gửi quá nhiều** → vẫn rò → DP + chỉ gửi gradient tối thiểu.
- **Bỏ qua drift cục bộ** → model lệch theo từng người mà không biết.
- **Quên versioning model trên thiết bị** → không debug được "thiết bị này chạy bản nào".

## ✅ "Tự kiểm tra & tự mò"
- [ ] 4 động lực edge AI (privacy/latency/offline/cost) + đánh đổi (thiết bị yếu).
- [ ] Kỹ thuật làm model nhỏ (quantize/distill/prune/runtime ONNX).
- [ ] Thách thức data phân tán (OTA/eval mù/sync/drift cục bộ).
- [ ] Federated learning: gửi gradient không gửi data; + DP.
- [ ] Vai trò DE: OTA pipeline, metric ẩn danh, sync, model nhỏ.
- 🔭 Tự mò: đo `fastembed` (đang dùng) chạy local mất bao lâu/embedding trên máy bạn (đó là "edge inference"); thử quantize ý tưởng: cắt vector float32→int8 (như [[ab07-vector-search-opt]]) đo RAM giảm + recall đổi — chính là đánh đổi edge.

➡️ Tiếp [[ae06-query-understanding]] — hiểu & định tuyến câu hỏi.
