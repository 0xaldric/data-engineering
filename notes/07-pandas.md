# 07 — pandas fundamentals

> Code: [`projects/02-python-de/01_pandas_basics.py`](../projects/02-python-de/01_pandas_basics.py)
> Chạy: `python projects/02-python-de/01_pandas_basics.py`

pandas là thư viện xử lý dữ liệu dạng bảng phổ biến nhất của Python. DE dùng để clean/transform dữ liệu vừa phải (vài trăm MB), prototyping, glue code. Dữ liệu lớn hơn RAM → polars/Spark (Phase sau).

## Hai cấu trúc cốt lõi
- **Series** = 1 cột (mảng 1 chiều có **index**). `products["unit_price"]` ra Series.
- **DataFrame** = bảng 2 chiều = tập Series chung index. `products[["a","b"]]` ra DataFrame.
- **Index** là "nhãn hàng" — khác SQL (không có khái niệm index hàng). Index cho phép align tự động khi tính toán giữa các Series; nhưng cũng hay gây nhầm → nhiều khi `reset_index()` cho gọn.

## Đọc/ghi
`pd.read_parquet/read_csv/read_json`, `df.to_parquet/to_csv`. Ưu tiên **Parquet** (nhanh, giữ kiểu, nén — xem [[09-file-formats]]). CSV không lưu kiểu → `order_ts` đọc lên là `object` (chuỗi), phải `pd.to_datetime` để thành `datetime64`.

## Selection & filtering
- `df["col"]` chọn cột; `df.loc[mask, ["a","b"]]` lọc theo nhãn + chọn cột; `df.iloc[0:5]` theo vị trí.
- **Boolean indexing:** `df[(df.cat=="Electronics") & (df.price>200)]`. Dùng `&  |  ~` (KHÔNG `and/or`) và **bọc ngoặc** từng điều kiện (do thứ tự ưu tiên toán tử).

## groupby + agg (≈ GROUP BY của SQL)
```python
customers.groupby("country").agg(
    n=("customer_id", "count"),
    pct_active=("is_active", "mean"),   # mean của bool = tỉ lệ True
)
```
Cú pháp named-aggregation `tên=("cột","hàm")` rõ ràng nhất. `mean()` của cột boolean = tỉ lệ — mẹo hay dùng.

## merge (≈ JOIN)
```python
items.merge(orders, on="order_id").merge(products, on="product_id")
```
- `how=` : `inner` (mặc định), `left`, `right`, `outer` — như SQL.
- ⚠️ Vẫn dính **fan-out** như SQL (xem [[02-sql-joins]]): merge 1-nhiều nhân hàng → cẩn thận khi sum cột mức-đơn-hàng. Kiểm `validate="one_to_many"` để pandas báo lỗi nếu quan hệ sai kỳ vọng.
- ✅ Doanh thu theo category tính bằng pandas **khớp chính xác** kết quả SQL → cùng một logic, hai công cụ.

## pivot_table & resample
- `pd.pivot_table(df, index=, columns=, values=, aggfunc=, fill_value=0)` — xoay dữ liệu (category × channel).
- Time series: đặt cột thời gian làm index rồi `.resample("MS").sum()` (MS = month start) để gộp theo tháng — tương đương `date_trunc('month', ...)` trong SQL.

## ⭐ Vectorization vs apply (bài học hiệu năng quan trọng)
```python
df["price"] * df["qty"] * (1 - df["discount"])   # vectorized — chạy ở C, cực nhanh
df.apply(lambda r: ..., axis=1)                  # apply theo hàng — Python loop, RẤT chậm
```
Đo thực tế trên 30k hàng: vectorized **0.2ms** vs apply **141ms** → chậm hơn **~600×**. Quy tắc: **luôn vectorize**, tránh `apply(axis=1)` và vòng `for` trên hàng. apply chỉ dùng khi bất khả kháng (logic phức tạp không vectorize được).

## NULL trong pandas
- NaN/None/`pd.NA`. Phát hiện: `df.isna().sum()`. Xử lý: `fillna(value)`, `dropna()`.
- ⚠️ NaN là float → cột int có NaN bị ép thành float. Dùng nullable dtype `Int64` (chữ I hoa) nếu cần int + NULL.

## pandas vs SQL (bảng dịch nhanh)
| SQL | pandas |
|-----|--------|
| `SELECT a,b` | `df[["a","b"]]` |
| `WHERE` | `df[mask]` / `df.query(...)` |
| `GROUP BY ... agg` | `df.groupby(...).agg(...)` |
| `JOIN` | `df.merge(...)` |
| `ORDER BY` | `df.sort_values(...)` |
| `LIMIT n` | `df.head(n)` |
| window `OVER(PARTITION BY)` | `df.groupby(...).transform(...)` |

## ✅ Tự kiểm tra
- [ ] Phân biệt Series vs DataFrame vs Index
- [ ] Viết boolean indexing đúng (`&`/`|`, ngoặc)
- [ ] groupby+agg và merge nhiều bảng; nhớ fan-out
- [ ] Giải thích vì sao vectorization >> apply (đo được)
- [ ] Xử lý NULL và bẫy int→float

➡️ Tiếp theo: [[08-polars]] — nhanh hơn, lazy, cho dữ liệu lớn hơn.
