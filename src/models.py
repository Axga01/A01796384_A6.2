"""
Data models for the hotel reservation system.

This module defines the core entities used by the services:
Hotel, Customer, and Reservation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Hotel:
    """Represents a hotel with a limited inventory of rooms."""
    hotel_id: str
    name: str
    rooms_total: int
    rooms_available: int

    def reserve_room(self) -> bool:
        """Decrease available rooms by one if possible."""
        if self.rooms_available <= 0:
            return False
        self.rooms_available -= 1
        return True

    def release_room(self) -> bool:
        """Increase available rooms by one, up to rooms_total."""
        if self.rooms_available >= self.rooms_total:
            return False
        self.rooms_available += 1
        return True


@dataclass
class Customer:
    """Represents a customer that can create reservations."""
    customer_id: str
    name: str


@dataclass
class Reservation:
    """Represents a reservation for a hotel made by a customer."""
    reservation_id: str
    hotel_id: str
    customer_id: str
    status: str = "ACTIVE"

    def cancel(self) -> None:
        """Mark the reservation as canceled."""
        self.status = "CANCELED"
