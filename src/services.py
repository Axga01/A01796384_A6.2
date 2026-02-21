"""
Business services for hotels, customers, and reservations.

These services use FileStore for persistence and provide CRUD operations
and reservation logic with basic validations.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Optional

from src.models import Customer, Hotel, Reservation
from src.storage import FileStore


class HotelService:
    """Service for managing Hotel records."""

    def __init__(self, store: FileStore) -> None:
        self.store = store

    def create(self, hotel: Hotel) -> bool:
        """Create a new hotel if it doesn't exist and values are valid."""
        hotels = self.store.load()
        if hotel.hotel_id in hotels:
            print("[ERROR] Hotel already exists.")
            return False
        if hotel.rooms_total < 0 or hotel.rooms_available < 0:
            print("[ERROR] Invalid room values.")
            return False
        hotels[hotel.hotel_id] = asdict(hotel)
        self.store.save(hotels)
        return True

    def get(self, hotel_id: str) -> Optional[Hotel]:
        """Return a Hotel by id, or None if not found/invalid."""
        hotels = self.store.load()
        h = hotels.get(hotel_id)
        if not isinstance(h, dict):
            return None
        try:
            return Hotel(**h)
        except TypeError:
            print("[WARN] Hotel record malformed.")
            return None

    def delete(self, hotel_id: str) -> bool:
        """Delete a hotel by id."""
        hotels = self.store.load()
        if hotel_id not in hotels:
            print("[ERROR] Hotel not found.")
            return False
        del hotels[hotel_id]
        self.store.save(hotels)
        return True

    def update(self, hotel_id: str, **changes) -> bool:
        """Update an existing hotel record with partial changes."""
        hotels = self.store.load()
        if hotel_id not in hotels:
            print("[ERROR] Hotel not found.")
            return False
        record = hotels[hotel_id]
        if not isinstance(record, dict):
            print("[ERROR] Hotel record invalid.")
            return False
        record.update(changes)
        hotels[hotel_id] = record
        self.store.save(hotels)
        return True

    def list_all(self) -> Dict[str, dict]:
        """Return all hotels as a dict."""
        data = self.store.load()
        return data if isinstance(data, dict) else {}


class CustomerService:
    """Service for managing Customer records."""

    def __init__(self, store: FileStore) -> None:
        self.store = store

    def create(self, customer: Customer) -> bool:
        """Create a new customer if it doesn't exist."""
        customers = self.store.load()
        if customer.customer_id in customers:
            print("[ERROR] Customer already exists.")
            return False
        customers[customer.customer_id] = asdict(customer)
        self.store.save(customers)
        return True

    def get(self, customer_id: str) -> Optional[Customer]:
        """Return a Customer by id, or None if not found/invalid."""
        customers = self.store.load()
        c = customers.get(customer_id)
        if not isinstance(c, dict):
            return None
        try:
            return Customer(**c)
        except TypeError:
            print("[WARN] Customer record malformed.")
            return None

    def delete(self, customer_id: str) -> bool:
        """Delete a customer by id."""
        customers = self.store.load()
        if customer_id not in customers:
            print("[ERROR] Customer not found.")
            return False
        del customers[customer_id]
        self.store.save(customers)
        return True

    def update(self, customer_id: str, **changes) -> bool:
        """Update an existing customer record with partial changes."""
        customers = self.store.load()
        if customer_id not in customers:
            print("[ERROR] Customer not found.")
            return False
        record = customers[customer_id]
        if not isinstance(record, dict):
            print("[ERROR] Customer record invalid.")
            return False
        record.update(changes)
        customers[customer_id] = record
        self.store.save(customers)
        return True

    def list_all(self) -> Dict[str, dict]:
        """Return all customers as a dict."""
        data = self.store.load()
        return data if isinstance(data, dict) else {}


class ReservationService:
    """Service for managing Reservation records and room availability updates."""

    def __init__(
        self,
        reservations_store: FileStore,
        hotel_service: HotelService,
        customer_service: CustomerService,
    ) -> None:
        self.store = reservations_store
        self.hotels = hotel_service
        self.customers = customer_service

    def create(self, reservation: Reservation) -> bool:
        """Create a reservation if ids exist and rooms are available."""
        reservations = self.store.load()
        if reservation.reservation_id in reservations:
            print("[ERROR] Reservation already exists.")
            return False

        hotel = self.hotels.get(reservation.hotel_id)
        if hotel is None:
            print("[ERROR] Hotel not found.")
            return False

        customer = self.customers.get(reservation.customer_id)
        if customer is None:
            print("[ERROR] Customer not found.")
            return False

        if not hotel.reserve_room():
            print("[ERROR] No rooms available.")
            return False

        # persist updated hotel availability
        self.hotels.update(
            hotel.hotel_id,
            rooms_total=hotel.rooms_total,
            rooms_available=hotel.rooms_available,
            name=hotel.name,
        )

        reservations[reservation.reservation_id] = asdict(reservation)
        self.store.save(reservations)
        return True

    def cancel(self, reservation_id: str) -> bool:
        """Cancel an existing reservation and release a room back to the hotel."""
        reservations = self.store.load()
        rec = reservations.get(reservation_id)
        if not isinstance(rec, dict):
            print("[ERROR] Reservation not found.")
            return False

        try:
            reservation = Reservation(**rec)
        except TypeError:
            print("[WARN] Reservation record malformed.")
            return False

        if reservation.status == "CANCELED":
            print("[WARN] Reservation already canceled.")
            return True

        hotel = self.hotels.get(reservation.hotel_id)
        if hotel is None:
            print("[ERROR] Hotel not found.")
            return False

        hotel.release_room()
        self.hotels.update(
            hotel.hotel_id,
            rooms_total=hotel.rooms_total,
            rooms_available=hotel.rooms_available,
            name=hotel.name,
        )

        reservation.cancel()
        reservations[reservation_id] = asdict(reservation)
        self.store.save(reservations)
        return True

    def list_all(self) -> Dict[str, dict]:
        """Return all reservations as a dict."""
        data = self.store.load()
        return data if isinstance(data, dict) else {}
