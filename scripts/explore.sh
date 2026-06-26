#!/usr/bin/env bash
# explore.sh — phân tích nhanh dataset CSV CHỈ bằng Unix shell tools
# (wc, head, cut, sort, uniq, grep, awk) — không cần Python/SQL.
# Minh hoạ vì sao DE phải thạo shell: kiểm tra file nhanh trước khi nạp pipeline.
#
# Usage: bash scripts/explore.sh
set -euo pipefail

RAW="$(cd "$(dirname "$0")/.." && pwd)/data/raw"
ORDERS="$RAW/orders.csv"
PRODUCTS="$RAW/products.csv"
ITEMS="$RAW/order_items.csv"
CUSTOMERS="$RAW/customers.csv"

hr() { printf '%s\n' "----------------------------------------------------------"; }

echo "Dataset: $RAW"
hr
# 1) wc -l : đếm số dòng mỗi file (trừ 1 dòng header)
echo "[1] Số bản ghi mỗi bảng (wc -l, đã trừ header):"
for f in "$CUSTOMERS" "$PRODUCTS" "$ORDERS" "$ITEMS"; do
    rows=$(($(wc -l < "$f") - 1))
    printf "    %-14s %'d rows\n" "$(basename "$f")" "$rows"
done

hr
# 2) head + cột: xem header và vài dòng đầu
echo "[2] Header của orders.csv (head -1):"
head -1 "$ORDERS" | sed 's/^/    /'

hr
# 3) cut + sort + uniq -c : phân phối giá trị 1 cột (order status, cột 4)
echo "[3] Phân phối 'status' trong orders (cut|sort|uniq -c):"
cut -d',' -f4 "$ORDERS" | tail -n +2 | sort | uniq -c | sort -rn | sed 's/^/   /'

hr
# 4) cut cột 'channel' (cột 5)
echo "[4] Phân phối 'channel':"
cut -d',' -f5 "$ORDERS" | tail -n +2 | sort | uniq -c | sort -rn | sed 's/^/   /'

hr
# 5) Top category theo số sản phẩm (products cột 3)
echo "[5] Top 5 category theo số sản phẩm:"
cut -d',' -f3 "$PRODUCTS" | tail -n +2 | sort | uniq -c | sort -rn | head -5 | sed 's/^/   /'

hr
# 6) awk : aggregate số học — tổng & trung bình line_total (order_items cột 7)
echo "[6] Doanh thu (order_items.line_total, cột 7) bằng awk:"
awk -F',' 'NR>1 { sum += $7; n++ }
           END { printf "    rows=%d  total=%.2f  avg=%.2f\n", n, sum, sum/n }' "$ITEMS"

hr
# 7) awk group-by : doanh thu theo discount level (cột 6)
echo "[7] Doanh thu theo mức discount (awk associative array):"
awk -F',' 'NR>1 { rev[$6] += $7 }
           END { for (d in rev) printf "    discount=%-4s  revenue=%.2f\n", d, rev[d] }' "$ITEMS" \
    | sort

hr
# 8) grep -c : đếm nhanh không cần parse (số đơn completed)
echo "[8] Đếm đơn 'completed' (grep -c):"
printf "    %s completed orders\n" "$(grep -c ',completed,' "$ORDERS")"

hr
# 9) Pipeline thực chiến: top 5 quốc gia khách hàng (customers cột 4)
echo "[9] Top 5 quốc gia theo số khách:"
cut -d',' -f4 "$CUSTOMERS" | tail -n +2 | sort | uniq -c | sort -rn | head -5 | sed 's/^/   /'

hr
echo "Done. (Lưu ý: parse CSV bằng cut/awk chỉ an toàn khi field KHÔNG chứa"
echo "dấu phẩy/quote. Dữ liệu thật có quoting → dùng csvkit/duckdb/miller.)"
