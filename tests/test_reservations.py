import unittest
from tempfile import TemporaryDirectory

from src.models import Hotel, Customer, Reservation
from src.services import HotelService, CustomerService, ReservationService
from src.storage import FileStore


class TestReservationService(unittest.TestCase):

    def setUp(self):
        self.tmp = TemporaryDirectory()

        self.hotel_store = FileStore(f"{self.tmp.name}/hotels.json")
        self.customer_store = FileStore(f"{self.tmp.name}/customers.json")
        self.reservation_store = FileStore(f"{self.tmp.name}/reservations.json")

        self.hotel_service = HotelService(self.hotel_store)
        self.customer_service = CustomerService(self.customer_store)
        self.reservation_service = ReservationService(
            self.reservation_store,
            self.hotel_service,
            self.customer_service
        )

        # crear datos base
        self.hotel_service.create(Hotel("H001", "Hotel Test", 1, 1))
        self.customer_service.create(Customer("C001", "Andrea", "mail@test.com"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_reservation_success(self):
        reservation = Reservation("R001", "H001", "C001")
        result = self.reservation_service.create(reservation)
        self.assertTrue(result)

    def test_reservation_hotel_not_found(self):
        reservation = Reservation("R002", "H999", "C001")
        result = self.reservation_service.create(reservation)
        self.assertFalse(result)

    def test_reservation_customer_not_found(self):
        reservation = Reservation("R003", "H001", "C999")
        result = self.reservation_service.create(reservation)
        self.assertFalse(result)

    def test_reservation_no_rooms_available(self):
        reservation1 = Reservation("R004", "H001", "C001")
        self.reservation_service.create(reservation1)

        reservation2 = Reservation("R005", "H001", "C001")
        result = self.reservation_service.create(reservation2)

        self.assertFalse(result)

    def test_cancel_nonexistent_reservation(self):
        result = self.reservation_service.cancel("R999")
        self.assertFalse(result)

    def test_cancel_reservation_success(self):
    reservation = Reservation("R100", "H001", "C001")
    self.assertTrue(self.reservation_service.create(reservation))

    result = self.reservation_service.cancel("R100")
    self.assertTrue(result)


def test_create_duplicate_reservation_fails(self):
    reservation = Reservation("R200", "H001", "C001")
    self.assertTrue(self.reservation_service.create(reservation))

    duplicate = Reservation("R200", "H001", "C001")
    result = self.reservation_service.create(duplicate)
    self.assertFalse(result)    