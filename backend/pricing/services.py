from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone

# MVP discount rates (can be moved to DB later)
DISCOUNT_MAP = {
    "SUMMER2026": Decimal("0.20"),
    "FALL2026": Decimal("0.15"),
    "WEEKENDDEAL": Decimal("0.10"),
    "FIRSTRENTAL": Decimal("0.20"),
    "HOLIDAYSALE": Decimal("0.15"),
}

def _money(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def validate_promo(promo_row) -> bool:
    """promo_row should have fields: is_active, expiry_date"""
    if promo_row is None:
        return False
    if not promo_row.is_active:
        return False
    if promo_row.expiry_date and promo_row.expiry_date < timezone.localdate():
        return False
    return True

def calculate_total_cost(hourly_rate, start_dt, end_dt, promo_code: str | None = None):
    """
    Total = hourly_rate * hours
    Apply promo discount if known.
    Returns dict: subtotal, discount_amount, total
    """
    if end_dt <= start_dt:
        raise ValueError("End date/time must be after start date/time.")

    seconds = (end_dt - start_dt).total_seconds()
    hours = Decimal(str(seconds)) / Decimal("3600")

    # minimum charge 1 hour
    if hours < 1:
        hours = Decimal("1")

    subtotal = _money(Decimal(str(hourly_rate)) * hours)

    discount_rate = Decimal("0.00")
    if promo_code:
        promo_code = promo_code.strip().upper()
        discount_rate = DISCOUNT_MAP.get(promo_code, Decimal("0.00"))

    discount_amount = _money(subtotal * discount_rate)
    total = _money(subtotal - discount_amount)

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "total": total,
        "promo_code": promo_code if promo_code else None,
    }