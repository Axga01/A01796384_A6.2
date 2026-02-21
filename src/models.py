"""
Domain models for the hotel reservation system.

Includes basic entities: Hotel, Customer, and Reservation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Hotel:
    """Represents a hotel and its room availability."""

    hotel_id: str
    name: str
    rooms_total: int
    rooms_available: int

    def reserve_room(self) -> bool:
        """Reserve one room if available. Returns True on success."""
        if self.rooms_available <= 0:
            return False
        self.rooms_available -= 1
        return True

    def release_room(self) -> None:
        """Release one room back if it does not exceed rooms_total."""
        if self.rooms_available < self.rooms_total:
            self.rooms_available += 1


@dataclass
class Customer:
    """Represents a customer.

    Email is optional to keep the model flexible and test-friendly.
    """

    customer_id: str
    name: str
    email: Optional[str] = None


@dataclass
class Reservation:
    """Represents a reservation made by a customer for a hotel."""

    reservation_id: str
    hotel_id: str
    customer_id: str
    status: str = "ACTIVE"  # ACTIVE | CANCELED

    def cancel(self) -> None:
        """Mark the reservation as canceled."""
        self.status = "CANCELED"
