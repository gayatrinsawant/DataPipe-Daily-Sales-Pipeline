
from datetime import datetime


def transform_data(rows):
    valid_rows = []
    rejected_rows = []
    seen_order_ids = set()

    for row in rows:
        reason = ""

        order_id = str(row.get("order_id", "")).strip()
        store = row.get("store", "")
        date_text = str(row.get("date", "")).strip()
        product = str(row.get("product", "")).strip()
        
        try:
            qty = int(row.get("qty", ""))
            price = float(row.get("price", ""))
        except (ValueError, TypeError):
            qty = 0
            price = 0
            reason = "Invalid quantity or price"

        if not reason and not order_id:
            reason = "Missing order ID"

        if not reason and order_id in seen_order_ids:
            reason = "Duplicate order ID"

        if not reason:
            try:
                parsed_date = None
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                    try:
                        parsed_date = datetime.strptime(date_text, fmt)
                        break
                    except ValueError:
                        continue

                if parsed_date is None:
                    reason = "Invalid date"
            except ValueError:
                reason = "Invalid date"

        if not reason and not product:
            reason = "Missing product name"

        if not reason and qty <= 0:
            reason = "Quantity must be positive"

        if not reason and price <= 0:
            reason = "Price must be positive"

        if reason:
            rejected_rows.append({
                "store": store,
                "order_id": order_id,
                "date": date_text,
                "product": product,
                "qty": row.get("qty", ""),
                "price": row.get("price", ""),
                "reason": reason
            })
        else:
            seen_order_ids.add(order_id)
            valid_rows.append({
                "order_id": order_id,
                "store": store,
                "date": parsed_date.strftime("%Y-%m-%d"),
                "product": product.title(),
                "qty": qty,
                "price": price,
                "amount": qty * price
            })

    return valid_rows, rejected_rows
