# 08 — polars & so sánh với pandas

> Code: [`projects/02-python-de/02_polars_basics.py`](../projects/02-python-de/02_polars_basics.py)
> Chạy: `python projects/02-python-de/02_polars_basics.py`

**polars** là thư viện DataFrame viết bằng **Rust**, dùng **Apache Arrow** làm bộ nhớ cột, chạy **đa luồng** và có **lazy evaluation + query optimizer**. Là lựa chọn hiện đại thay pandas khi cần tốc độ / dữ liệu lớn hơn.

## Vì sao polars nhanh hơn pandas?
1. **Columnar (Arrow)** — dữ liệu lưu theo cột, cache-friendly, vectorized SIMD.
2. **Đa luồng mặc định** — tận dụng mọi core (pandas chủ yếu 1 luồng).
3. **Lazy + optimizer** — không chạy ngay; xây *kế hoạch* rồi tối ưu (đẩy filter/chọn cột xuống sát nguồn) trước khi thực thi.
4. **Không dùng index** — bỏ overhead align index của pandas.
5. Quản lý bộ nhớ Rust, ít copy.

Benchmark trong bài (join 3 bảng + filter + group_by, 30k hàng): pandas 7.7ms · polars eager 4.4ms (**1.7×**) · polars lazy 2.3ms (**3.4×**). Dữ liệu càng lớn, khoảng cách càng giãn.

## Expression API — khác biệt tư duy lớn nhất
polars không dùng `df[mask]` kiểu pandas mà dùng **biểu thức** `pl.col(...)`:
```python
df.filter((pl.col("category") == "Electronics") & (pl.col("unit_price") > 200))
  .with_columns((pl.col("unit_price") - pl.col("unit_cost")).alias("margin"))
  .select("product_name", "unit_price", "margin")
  .sort("margin", descending=True)
```
Expression mô tả "tính gì", engine quyết định "tính thế nào" (song song, tối ưu). Chuỗi method đọc như pipeline. Các method chính: `select / filter / with_columns / group_by().agg() / join / sort`.

## group_by + agg
```python
df.group_by("country").agg(n=pl.len(), pct_active=pl.col("is_active").mean())
```
Nhiều aggregate chạy **song song** trong một `agg()`. `pl.len()` đếm hàng; `pl.col(x).mean()` v.v.

## ⭐ Lazy evaluation — "linh hồn" của polars
```python
lf = pl.scan_parquet(path)...        # KHÔNG đọc gì cả — chỉ build plan
print(lf.explain())                   # xem kế hoạch đã tối ưu
df = lf.collect()                     # tới đây mới thực thi
```
- `scan_parquet` (lazy) vs `read_parquet` (eager đọc ngay).
- Optimizer tự làm **projection pushdown** (chỉ đọc cột cần — trong demo: `PROJECT 3/7 COLUMNS`) và **predicate pushdown** (đẩy `filter` xuống sát scan để đọc ít hàng hơn). Đây chính là tư tưởng tối ưu của warehouse/Spark, áp ngay trên file Parquet.
- Quy tắc: với pipeline nhiều bước trên file lớn → **luôn dùng lazy** rồi `collect()` một lần.

## Streaming (dữ liệu > RAM)
`lf.collect(streaming=True)` xử lý theo từng phần, cho phép chạy dataset lớn hơn RAM — cầu nối tới tư duy Spark ([[ROADMAP]] Phase 4).

## polars vs pandas — bảng dịch
| pandas | polars |
|--------|--------|
| `df[df.x > 2]` | `df.filter(pl.col("x") > 2)` |
| `df.assign(y=...)` | `df.with_columns((...).alias("y"))` |
| `df.groupby("c").agg(...)` | `df.group_by("c").agg(...)` |
| `df.merge(o, on=...)` | `df.join(o, on=...)` |
| `df["a"]*df["b"]` | `pl.col("a")*pl.col("b")` |
| eager mặc định | lazy (`scan_*` + `collect`) |

## Khi nào dùng cái nào?
- **pandas**: hệ sinh thái rộng (matplotlib, sklearn, nhiều lib nhận DataFrame pandas), dữ liệu nhỏ, prototyping.
- **polars**: ETL nặng, dữ liệu lớn, cần tốc độ/đa luồng, pipeline nhiều bước. Có thể `df.to_pandas()` khi cần bắc cầu.
- Cả hai đọc/ghi Arrow & Parquet nên chuyển qua lại rẻ.

## ✅ Tự kiểm tra
- [ ] Nêu 3 lý do polars nhanh hơn pandas
- [ ] Viết pipeline bằng expression API (`filter/with_columns/select`)
- [ ] Giải thích lazy vs eager; đọc được `explain()`
- [ ] Hiểu projection & predicate pushdown (đọc ít cột/ít hàng)
- [ ] Biết khi nào chọn pandas vs polars

➡️ Tiếp theo: [[09-file-formats]] — vì sao Parquet thắng (deep dive + benchmark).
