"""Unit tests for ReservationService."""

import shutil
import tempfile
import unittest

from src.models import Customer, Hotel, Reservation
from src.services import CustomerService, HotelService, ReservationService
from src.storage import FileStore


class TestReservationService(unittest.TestCase):
    """Tests for reservation creation, cancellation and validations."""

    def setUp(self):
        """Prepare isolated stores for each test."""
        self.tmp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp_dir)

        self.hotels_store = FileStore(f"{self.tmp_dir}/hotels.json")
        self.customers_store = FileStore(f"{self.tmp_dir}/customers.json")
        self.reservation_store = FileStore(f"{self.tmp_dir}/reservations.json")

        self.hotel_service = HotelService(self.hotels_store)
        self.customer_service = CustomerService(self.customers_store)
        self.reservation_service = ReservationService(
            self.reservation_store,
            self.hotel_service,
            self.customer_service,
        )

        hotel = Hotel("H001", "Hotel A", 1, 1)
        customer = Customer("C001", "Customer A")

        self.hotel_service.create(hotel)
        self.customer_service.create(customer)

    def test_create_reservation_success(self):
        """Reservation is created when hotel and customer exist."""
        reservation = Reservation("R001", "H001", "C001")
        self.assertTrue(self.reservation_service.create(reservation))

    def test_reservation_hotel_not_found(self):
        """Creation fails if hotel does not exist."""
        reservation = Reservation("R002", "H404", "C001")
        self.assertFalse(self.reservation_service.create(reservation))

    def test_reservation_customer_not_found(self):
        """Creation fails if customer does not exist."""
        reservation = Reservation("R003", "H001", "C404")
        self.assertFalse(self.reservation_service.create(reservation))

    def test_reservation_no_rooms_available(self):
        """Creation fails when no rooms are available."""
        reservation1 = Reservation("R010", "H001", "C001")
        reservation2 = Reservation("R011", "H001", "C001")

        self.assertTrue(self.reservation_service.create(reservation1))
        self.assertFalse(self.reservation_service.create(reservation2))

    def test_create_duplicate_reservation_fails(self):
        """Duplicate reservation ids are rejected."""
        reservation = Reservation("R020", "H001", "C001")
        self.assertTrue(self.reservation_service.create(reservation))

        duplicate = Reservation("R020", "H001", "C001")
        self.assertFalse(self.reservation_service.create(duplicate))

    def test_cancel_nonexistent_reservation(self):
        """Cancel returns False when reservation does not exist."""
        self.assertFalse(self.reservation_service.cancel("R404"))

    def test_cancel_reservation_success(self):
        """Cancel releases the room and marks reservation canceled."""
        reservation = Reservation("R100", "H001", "C001")
        self.assertTrue(self.reservation_service.create(reservation))
        self.assertTrue(self.reservation_service.cancel("R100"))

    def test_cancel_already_canceled_returns_true(self):
        """Canceling twice returns True per service design."""
        reservation = Reservation("R200", "H001", "C001")
        self.assertTrue(self.reservation_service.create(reservation))
        self.assertTrue(self.reservation_service.cancel("R200"))
        self.assertTrue(self.reservation_service.cancel("R200"))

    def test_cancel_malformed_record_returns_false(self):
        """Malformed reservation data should not crash cancel."""
        self.reservation_store.save({"RBAD": {"reservation_id": "RBAD"}})
        self.assertFalse(self.reservation_service.cancel("RBAD"))

    def test_list_all_returns_empty_if_not_dict(self):
        """list_all returns empty dict when storage is invalid."""
        self.reservation_store.save(["not", "a", "dict"])
        self.assertEqual(self.reservation_service.list_all(), {})


if __name__ == "__main__":
    unittest.main()
