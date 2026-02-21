import unittest
from tempfile import TemporaryDirectory

from src.models import Hotel
from src.services import HotelService
from src.storage import FileStore


class TestHotelService(unittest.TestCase):

    def test_create_hotel_success(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            service = HotelService(store)

            hotel = Hotel("H001", "Hotel Test", 5, 5)
            result = service.create(hotel)

            self.assertTrue(result)

    def test_create_duplicate_hotel_fails(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            service = HotelService(store)

            hotel = Hotel("H001", "Hotel Test", 5, 5)
            service.create(hotel)

            duplicate = service.create(hotel)
            self.assertFalse(duplicate)

    def test_get_nonexistent_hotel(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            service = HotelService(store)

            hotel = service.get("NO_EXIST")
            self.assertIsNone(hotel)

    def test_delete_nonexistent_hotel(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            service = HotelService(store)

            result = service.delete("H999")
            self.assertFalse(result)
    def test_update_hotel_success(self):
    with TemporaryDirectory() as tmp:
        store = FileStore(f"{tmp}/hotels.json")
        service = HotelService(store)

        hotel = Hotel("H010", "Old Name", 2, 2)
        self.assertTrue(service.create(hotel))

        # update name and rooms_available
        result = service.update("H010", name="New Name", rooms_available=1)
        self.assertTrue(result)

        updated = service.get("H010")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "New Name")
        self.assertEqual(updated.rooms_available, 1)


def test_display_hotel_info_nonexistent(self):
    with TemporaryDirectory() as tmp:
        store = FileStore(f"{tmp}/hotels.json")
        service = HotelService(store)

        # should not crash; expected None/False depending on your implementation
        result = service.display("H404")
        self.assertFalse(result)