# 61 — Data Contracts

> Nguyên nhân #1 pipeline gãy: **producer đổi schema** (đổi tên/xoá cột, đổi kiểu) mà consumer không biết. **Data contract** ngăn điều đó.

## Data contract là gì?
Một **thoả thuận chính thức** (machine-readable) giữa **producer** (đội tạo dữ liệu) và **consumer** (đội dùng dữ liệu) về:
- **Schema**: cột, kiểu, nullable.
- **Ngữ nghĩa**: ý nghĩa từng field, đơn vị, miền giá trị hợp lệ.
- **SLA**: tần suất cập nhật, freshness, độ trễ, cam kết chất lượng.
- **Ownership**: ai chịu trách nhiệm, liên hệ, quy trình đổi.
- **Versioning & chính sách thay đổi**: đổi thế nào (backward compatible), thông báo ra sao.

```yaml
# minh hoạ một data contract (YAML)
dataset: orders
owner: order-team
schema:
  - {name: order_id, type: bigint, nullable: false, unique: true}
  - {name: amount, type: decimal(10,2), nullable: false, min: 0}
  - {name: status, type: string, enum: [completed, shipped, cancelled, returned]}
sla:
  freshness: 1h
  availability: 99.9%
```

## Vì sao cần
- Không có contract → producer refactor DB → cột biến mất → mọi dashboard/model downstream **gãy âm thầm** hoặc ra số sai.
- Contract biến **giả định ngầm** thành **cam kết rõ ràng, kiểm tra được**.
- Cho phép **shift-left** ([[60-data-quality]]): bắt lỗi tại nguồn, không để lan xuống.

## Enforcement (làm sao "ép" hợp đồng)
- **Schema Registry** cho stream (Kafka/Avro): từ chối schema phá vỡ tương thích ([[48-kafka-ecosystem]], [[10-json-avro]]).
- **CI check**: PR đổi schema producer → pipeline kiểm tra có vi phạm contract không (diff schema, compatibility test) → chặn merge ([[58-cicd]]).
- **Validation runtime**: kiểm dữ liệu vào có khớp contract (GE/Soda/pydantic — [[60-data-quality]], [[12-testing-de]]).
- **dbt contracts**: dbt cho khai báo `contract: {enforced: true}` trên model → build fail nếu schema lệch.

## Vòng đời thay đổi
- **Backward-compatible** (thêm cột optional có default) → an toàn, thông báo. Giống schema evolution Avro ([[10-json-avro]]).
- **Breaking change** (xoá/đổi cột) → phải **versioning** (v1/v2 song song), thông báo, deprecate có lộ trình, đợi consumer migrate.

## Liên hệ tổ chức: Data as a Product / Data Mesh
Contract là nền của tư duy **"dữ liệu là sản phẩm"**: mỗi domain team **sở hữu** dataset của mình như một sản phẩm có SLA/contract cho người dùng nội bộ. (Data Mesh = phân quyền sở hữu dữ liệu theo domain + contract + self-serve platform.)

## ⚠️ Cạm bẫy
- Contract chỉ là tài liệu (không enforce) → vẫn bị phá. Phải có **kiểm tra tự động**.
- Quá cứng nhắc → cản tiến hoá; cần chính sách thay đổi rõ + tương thích.
- Không có owner → contract "mồ côi", không ai bảo trì.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Data contract gồm gì (schema/semantics/SLA/owner/versioning).
- [ ] Vì sao cần (breaking change âm thầm); shift-left.
- [ ] Enforcement: schema registry / CI / runtime validation / dbt contracts.
- [ ] Backward-compatible vs breaking change; versioning.
- 🔭 *Tự mò:* viết một file contract YAML cho `orders` (như trên), rồi viết pydantic model + GE suite khớp contract đó → chạy validate trên `data/raw`.

➡️ Tiếp: [[62-observability]].
