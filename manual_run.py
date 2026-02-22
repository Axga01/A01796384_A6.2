# manual_run.py
"""
Manual functional flow (no unittest) for Hotel/Customer/Reservation services.

It uses the real JSON files under data/ and writes evidence-ready output.
Run:
  python manual_run.py | tee results/functional_run.txt
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from src.models import Customer, Hotel, Reservation
from src.services import CustomerService, HotelService, ReservationService
from src.storage import FileStore


def _new_id(prefix: str) -> str:
    # short unique id to avoid collisions with existing data
    return f"{prefix}{uuid4().hex[:6].upper()}"


def main() -> None:
    print("=== Manual Functional Run ===")
    print("Timestamp:", datetime.now().isoformat(timespec="seconds"))

    # Ensure folders exist
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("results").mkdir(parents=True, exist_ok=True)

    # Real persistence files
    hotels_path = "data/hotels.json"
    customers_path = "data/customers.json"
    reservations_path = "data/reservations.json"

    print("\n[Paths]")
    print(" hotels      =", hotels_path)
    print(" customers   =", customers_path)
    print(" reservations=", reservations_path)

    # Services
    hotel_service = HotelService(FileStore(hotels_path))
    customer_service = CustomerService(FileStore(customers_path))
    reservation_service = ReservationService(
        FileStore(reservations_path),
        hotel_service,
        customer_service,
    )

    # Use unique IDs so we don't break existing JSON data
    hotel_id = _new_id("HF")
    customer_id = _new_id("CF")
    reservation_id = _new_id("RF")

    print("\n[Generated IDs]")
    print(" hotel_id      =", hotel_id)
    print(" customer_id   =", customer_id)
    print(" reservation_id=", reservation_id)

    # 1) Create hotel
    print("\n[1] Create hotel")
    hotel = Hotel(hotel_id, "Hotel Funcional", 3, 3)
    ok = hotel_service.create(hotel)
    print(" create ->", ok)

    # 2) Create customer
    print("\n[2] Create customer")
    customer = Customer(customer_id, "Cliente Funcional")
    ok = customer_service.create(customer)
    print(" create ->", ok)

    # 3) Create reservation
    print("\n[3] Create reservation")
    reservation = Reservation(reservation_id, hotel_id, customer_id)
    ok = reservation_service.create(reservation)
    print(" create ->", ok)

    # 4) Validate hotel rooms decreased (read-back)
    print("\n[4] Validate hotel rooms availability decreased")
    h = hotel_service.get(hotel_id)
    if h is None:
        print(" get -> None (unexpected)")
    else:
        print(" rooms_total     =", h.rooms_total)
        print(" rooms_available =", h.rooms_available)

    # 5) Cancel reservation
    print("\n[5] Cancel reservation")
    ok = reservation_service.cancel(reservation_id)
    print(" cancel ->", ok)

    # 6) Validate hotel rooms restored (read-back)
    print("\n[6] Validate hotel rooms availability restored")
    h = hotel_service.get(hotel_id)
    if h is None:
        print(" get -> None (unexpected)")
    else:
        print(" rooms_total     =", h.rooms_total)
        print(" rooms_available =", h.rooms_available)

    # 7) Final check: reservation status (read raw store)
    print("\n[7] Validate reservation status in store")
    reservations = reservation_service.list_all()
    rec = reservations.get(reservation_id)
    if not isinstance(rec, dict):
        print(" reservation record missing/invalid:", rec)
    else:
        print(" status =", rec.get("status"))

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
