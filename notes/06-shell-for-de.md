# 06 — Shell & Linux cho Data Engineering

> Code: [`scripts/explore.sh`](../scripts/explore.sh) · Chạy: `bash scripts/explore.sh`

DE sống trên Linux/terminal: SSH vào server, đọc log, kiểm tra file trước khi nạp, viết cron/automation. Thạo shell giúp "soi" dữ liệu trong **giây** mà không cần mở Python/SQL.

## Bộ công cụ lõi (text processing)
| Lệnh | Công dụng | Ví dụ |
|------|-----------|-------|
| `wc -l` | đếm dòng | `wc -l file.csv` |
| `head` / `tail` | xem đầu/cuối; `tail -n +2` bỏ header | `head -5 f`, `tail -n +2 f` |
| `cut` | cắt cột theo delimiter | `cut -d',' -f4 f` |
| `sort` | sắp xếp (`-n` số, `-r` ngược, `-t -k` theo cột) | `sort -t',' -k7 -rn` |
| `uniq` | gộp dòng trùng kề nhau (`-c` đếm) | `sort \| uniq -c` |
| `grep` | lọc theo mẫu (`-c` đếm, `-v` đảo, `-E` regex) | `grep -c ',completed,'` |
| `sed` | thay thế/sửa stream | `sed 's/old/new/g'` |
| `awk` | xử lý theo cột + số học + group-by | xem dưới |

## Triết lý Unix: pipe `|`
Nối các lệnh nhỏ thành chuỗi xử lý. Pattern **đếm phân phối một cột** (cực hay dùng):
```bash
cut -d',' -f4 orders.csv | tail -n +2 | sort | uniq -c | sort -rn
#   lấy cột 4         bỏ header   sắp  đếm trùng   sắp giảm dần
```
→ ra ngay phân phối `status` mà không cần `GROUP BY`. `uniq -c` **bắt buộc** đứng sau `sort` (chỉ gộp dòng trùng *liền kề*).

## awk — "mini SQL" trên dòng lệnh
`awk` đọc từng dòng, tách field theo `-F`, biến `$1,$2...` là cột, `NR` là số dòng:
```bash
# Tổng + trung bình cột 7, bỏ header
awk -F',' 'NR>1 { sum+=$7; n++ } END { printf "total=%.2f avg=%.2f\n", sum, sum/n }' items.csv

# GROUP BY: doanh thu theo discount (mảng kết hợp = hash map)
awk -F',' 'NR>1 { rev[$6]+=$7 } END { for (d in rev) print d, rev[d] }' items.csv
```
`awk` làm được sum/avg/count/group-by trên file hàng triệu dòng, **streaming** (không nạp hết vào RAM) — hợp khi file quá lớn cho pandas.

## ⚠️ Cạm bẫy parse CSV bằng shell
`cut`/`awk -F','` **chỉ đúng khi field không chứa dấu phẩy hay dấu nháy**. CSV thật có quoting (`"Hanoi, VN"`) sẽ vỡ cột. Khi đó dùng công cụ hiểu CSV thật: **`csvkit`** (`csvstat`, `csvcut`), **`miller` (mlr)**, hoặc **DuckDB** (`SELECT * FROM read_csv_auto(...)`). Shell hợp để *soi nhanh*; ETL nghiêm túc dùng parser chuẩn.

## Vài thứ DE hay dùng thêm
- **Tổ hợp tìm & xử lý:** `find . -name '*.csv'`, `xargs`, `tee` (ghi vừa in).
- **Nén/luồng:** `zcat file.gz | awk ...` xử lý file nén không cần giải nén ra đĩa.
- **`jq`** — "awk cho JSON": lọc/biến đổi JSON từ API.
- **Quyền & môi trường:** `chmod +x`, biến môi trường, `export`, `.bashrc`.
- **Theo dõi job:** `ps`, `top/htop`, `df -h` (đĩa), `du -sh *` (dung lượng thư mục).

## cron — lập lịch (nền tảng của orchestration)
```
# phút giờ ngày tháng thứ   lệnh
0 2 * * *   /path/run_etl.sh   # chạy 2:00 sáng mỗi ngày
*/30 * * * *  /path/poll.sh    # mỗi 30 phút
```
Airflow/Dagster (Phase 5) bản chất là "cron có quản lý phụ thuộc, retry, backfill, UI". Hiểu cron trước giúp hiểu scheduler sau. Xem [[06-shell-for-de]] → orchestration.

## ✅ Tự kiểm tra
- [ ] Viết pipeline `cut|sort|uniq -c|sort -rn` để đếm phân phối một cột
- [ ] Dùng `awk` tính tổng/trung bình và group-by một cột
- [ ] Biết vì sao `uniq` phải đi sau `sort`
- [ ] Nêu được rủi ro parse CSV có quoting bằng shell và công cụ thay thế
- [ ] Đọc/viết được một dòng crontab

➡️ Tiếp theo: [[00-phase0-summary]] sau khi xong bài tập tổng hợp.
