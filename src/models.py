from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Hotel:
    hotel_id: str
    name: str
    rooms_total: int
    rooms_available: int

    def reserve_room(self) -> bool:
        if self.rooms_available <= 0:
            return False
        self.rooms_available -= 1
        return True

    def release_room(self) -> None:
        if self.rooms_available < self.rooms_total:
            self.rooms_available += 1


@dataclass
class Customer:
    customer_id: str
    name: str
    email: Optional[str] = None


@dataclass
class Reservation:
    reservation_id: str
    hotel_id: str
    customer_id: str
    status: str = "ACTIVE"  # ACTIVE | CANCELED

    def cancel(self) -> None:
        self.status = "CANCELED"