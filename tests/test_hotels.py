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

    def test_create_invalid_rooms_fails(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            service = HotelService(store)

            hotel = Hotel("HNEG", "Bad Hotel", -1, -1)
            self.assertFalse(service.create(hotel))

    def test_update_hotel_success(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            service = HotelService(store)

            hotel = Hotel("H010", "Old Name", 2, 2)
            self.assertTrue(service.create(hotel))

            result = service.update("H010", name="New Name", rooms_available=1)
            self.assertTrue(result)

            updated = service.get("H010")
            self.assertIsNotNone(updated)
            self.assertEqual(updated.name, "New Name")
            self.assertEqual(updated.rooms_available, 1)

    def test_update_nonexistent_hotel_fails(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            service = HotelService(store)

            self.assertFalse(service.update("H404", name="X"))

    def test_update_invalid_record_fails(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            store.save({"H001": "not-a-dict"})

            service = HotelService(store)
            self.assertFalse(service.update("H001", name="X"))

    def test_get_malformed_record_returns_none(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            store.save({"H001": {"hotel_id": "H001"}})  # faltan campos

            service = HotelService(store)
            self.assertIsNone(service.get("H001"))

    def test_list_all_returns_empty_if_not_dict(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/hotels.json")
            store.save(["not", "a", "dict"])

            service = HotelService(store)
            self.assertEqual(service.list_all(), {})


if __name__ == "__main__":
    unittest.main()