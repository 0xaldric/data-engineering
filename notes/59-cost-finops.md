# 59 — Cost Optimization & FinOps cho Data

> Dữ liệu lớn = hoá đơn lớn nếu bất cẩn. DE giỏi tối ưu chi phí (không chỉ hiệu năng). FinOps = văn hoá quản chi phí cloud.

## Vì sao chi phí data dễ phình
- Quét toàn bộ dữ liệu cho mỗi query (Athena/BigQuery tính theo **bytes scanned**).
- Cụm compute (EMR/warehouse) để chạy 24/7 dù chỉ dùng vài giờ.
- Lưu mọi thứ ở storage nóng mãi mãi.
- Pipeline build lại toàn bộ mỗi lần (không incremental).
- Small files + dữ liệu trùng.

## ⭐ Đòn bẩy tối ưu (theo tác động)
1. **Quét ít dữ liệu** (lớn nhất với serverless SQL):
   - **Parquet** thay CSV ([[09-file-formats]]) → nhỏ + column pruning.
   - **Partition** theo cột hay lọc → chỉ quét partition cần ([[31-partitioning-shuffle]], [[55-cloud-fundamentals]]).
   - Chọn **đúng cột** (`select col` không `select *`), lọc sớm.
   - → Athena/BigQuery: cùng query có thể rẻ đi **10–100×**.
2. **Compute đúng lúc, đúng cỡ**:
   - Auto-terminate cụm EMR; serverless (Glue/Athena/Lambda) trả theo dùng.
   - **Spot instances** (rẻ 60–90%) cho job chịu được gián đoạn.
   - Auto-scaling warehouse; tắt khi không dùng (Snowflake auto-suspend).
3. **Storage tiering**: lifecycle policy chuyển dữ liệu cũ sang lớp lạnh (Glacier) / expire ([[55-cloud-fundamentals]]).
4. **Incremental thay full** ([[27-dbt-incremental]]): chỉ xử lý dữ liệu mới → ít compute.
5. **Materialization hợp lý** ([[23-dbt-marts]]): table (tính sẵn, đọc nhiều) vs view (rẻ lưu, tính mỗi lần). Cân theo tần suất đọc.
6. **Compaction** small files ([[33-spark-tuning]], [[34-delta-lake]]) → đọc nhanh & rẻ.

## Monitoring chi phí (FinOps)
- **Tag** tài nguyên (team/project/env) → biết ai tiêu gì.
- Dashboard chi phí (AWS Cost Explorer), **budget alert** khi vượt ngưỡng.
- Theo dõi query đắt (bytes scanned cao), cụm idle, storage phình.
- Văn hoá: kỹ sư **thấy chi phí** của job mình → tự tối ưu (shift-left cost).

## Đánh đổi cost vs performance vs effort
Không phải lúc nào cũng tối ưu tối đa — cân:
- Query chạy 1 lần/tháng: không cần tối ưu kỹ.
- Query/dashboard chạy nghìn lần/ngày: tối ưu (materialize, partition) đáng giá.
- Đơn giản & rẻ thường thắng "tối ưu sớm" phức tạp.

## ⚠️ Cạm bẫy
- `SELECT *` trên bảng lớn ở Athena/BigQuery → hoá đơn sốc.
- Quên tắt cụm/warehouse dev → đốt tiền âm thầm.
- Không tag → không biết tiền đi đâu.
- Tối ưu sớm cái không chạy thường xuyên (phí công).
- Lưu mọi thứ nóng mãi mãi → chi phí storage tích luỹ.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Vì sao Parquet + partition + chọn cột giảm chi phí query serverless.
- [ ] Spot/auto-scale/auto-terminate cho compute.
- [ ] Storage tiering & lifecycle.
- [ ] Incremental & materialization ảnh hưởng chi phí.
- [ ] FinOps: tag, budget alert, làm kỹ sư thấy chi phí.
- 🔭 *Tự mò:* đo lại benchmark [[09-file-formats]] (CSV vs Parquet, đọc full vs 1 cột) và quy ra "nếu Athena tính theo bytes scanned thì rẻ đi bao nhiêu lần".

➡️ Tiếp: [[00-phase7-summary]].
