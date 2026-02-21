import unittest
from tempfile import TemporaryDirectory

from src.models import Customer
from src.services import CustomerService
from src.storage import FileStore


class TestCustomerService(unittest.TestCase):
    def test_create_customer_success(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = Customer("C001", "Andrea", "andrea@mail.com")
            result = service.create(customer)

            self.assertTrue(result)

    def test_duplicate_customer(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = Customer("C001", "Andrea", "andrea@mail.com")
            service.create(customer)

            result = service.create(customer)
            self.assertFalse(result)

    def test_get_nonexistent_customer(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = service.get("X999")
            self.assertIsNone(customer)

    def test_delete_nonexistent_customer(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            result = service.delete("X999")
            self.assertFalse(result)

    def test_update_nonexistent_customer_fails(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            self.assertFalse(service.update("C404", name="X"))

    def test_update_invalid_record_fails(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            store.save({"C001": "not-a-dict"})

            service = CustomerService(store)
            self.assertFalse(service.update("C001", name="X"))

    def test_get_malformed_record_returns_none(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            # Falta "name" y "email" -> Customer(**c) lanza TypeError -> None
            store.save({"C001": {"customer_id": "C001"}})

            service = CustomerService(store)
            self.assertIsNone(service.get("C001"))

    def test_update_customer_success(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = Customer("C010", "Old", "old@test.com")
            self.assertTrue(service.create(customer))

            result = service.update("C010", name="New", email="new@test.com")
            self.assertTrue(result)

            updated = service.get("C010")
            self.assertIsNotNone(updated)
            self.assertEqual(updated.name, "New")
            self.assertEqual(updated.email, "new@test.com")

    def test_list_all_returns_empty_if_not_dict(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            store.save(["not", "a", "dict"])

            service = CustomerService(store)
            self.assertEqual(service.list_all(), {})


if __name__ == "__main__":
    unittest.main()