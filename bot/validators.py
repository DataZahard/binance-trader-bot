def validate_order_params(order_type, price):
    if order_type.upper() == "LIMIT" and not price:
        raise ValueError("Price is required for LIMIT orders.")
    return True
