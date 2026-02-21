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


def test_display_customer_info_nonexistent(self):
    with TemporaryDirectory() as tmp:
        store = FileStore(f"{tmp}/customers.json")
        service = CustomerService(store)

        result = service.display("C404")
        self.assertFalse(result)        