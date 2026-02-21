import unittest
from tempfile import TemporaryDirectory

from src.models import Customer, Hotel, Reservation
from src.services import CustomerService, HotelService, ReservationService
from src.storage import FileStore


class TestReservationService(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        base = self.tmp.name

        self.hotels_store = FileStore(f"{base}/hotels.json")
        self.customers_store = FileStore(f"{base}/customers.json")
        self.reservation_store = FileStore(f"{base}/reservations.json")

        self.hotel_service = HotelService(self.hotels_store)
        self.customer_service = CustomerService(self.customers_store)
        self.reservation_service = ReservationService(
            self.reservation_store,
            self.hotel_service,
            self.customer_service,
        )

        # Seed base hotel + customer used in many tests
        hotel = Hotel("H001", "Hotel A", 1, 1)
        customer = Customer("C001", "Customer A", "a@test.com")
        self.hotel_service.create(hotel)
        self.customer_service.create(customer)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_reservation_success(self):
        reservation = Reservation("R001", "H001", "C001")
        result = self.reservation_service.create(reservation)
        self.assertTrue(result)

    def test_reservation_hotel_not_found(self):
        reservation = Reservation("R002", "H404", "C001")
        result = self.reservation_service.create(reservation)
        self.assertFalse(result)

    def test_reservation_customer_not_found(self):
        reservation = Reservation("R003", "H001", "C404")
        result = self.reservation_service.create(reservation)
        self.assertFalse(result)

    def test_reservation_no_rooms_available(self):
        reservation1 = Reservation("R010", "H001", "C001")
        reservation2 = Reservation("R011", "H001", "C001")

        self.assertTrue(self.reservation_service.create(reservation1))
        # hotel had only 1 room available
        self.assertFalse(self.reservation_service.create(reservation2))

    def test_create_duplicate_reservation_fails(self):
        reservation = Reservation("R020", "H001", "C001")
        self.assertTrue(self.reservation_service.create(reservation))

        duplicate = Reservation("R020", "H001", "C001")
        self.assertFalse(self.reservation_service.create(duplicate))

    def test_cancel_nonexistent_reservation(self):
        result = self.reservation_service.cancel("R404")
        self.assertFalse(result)

    def test_cancel_reservation_success(self):
        reservation = Reservation("R100", "H001", "C001")
        self.assertTrue(self.reservation_service.create(reservation))

        result = self.reservation_service.cancel("R100")
        self.assertTrue(result)

    def test_cancel_already_canceled_returns_true(self):
        reservation = Reservation("R200", "H001", "C001")
        self.assertTrue(self.reservation_service.create(reservation))

        self.assertTrue(self.reservation_service.cancel("R200"))
        # second cancel should return True per your service
        self.assertTrue(self.reservation_service.cancel("R200"))

    def test_cancel_malformed_record_returns_false(self):
        # Force malformed reservation record
        self.reservation_store.save({"RBAD": {"reservation_id": "RBAD"}})
        self.assertFalse(self.reservation_service.cancel("RBAD"))

    def test_list_all_returns_empty_if_not_dict(self):
        self.reservation_store.save(["not", "a", "dict"])
        self.assertEqual(self.reservation_service.list_all(), {})


if __name__ == "__main__":
    unittest.main()