"""
Unit tests for CustomerService.

Covers create/get/update/delete and edge cases using an isolated
temporary JSON store per test.
"""

import unittest
from tempfile import TemporaryDirectory

from src.models import Customer
from src.services import CustomerService
from src.storage import FileStore


class TestCustomerService(unittest.TestCase):
    """Tests for CRUD operations and validations in CustomerService."""

    def test_create_customer_success(self):
        """Creating a new customer should return True."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = Customer("C001", "Andrea")
            result = service.create(customer)

            self.assertTrue(result)

    def test_duplicate_customer(self):
        """Creating a customer twice with same id should return False."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = Customer("C001", "Andrea")
            service.create(customer)

            result = service.create(customer)
            self.assertFalse(result)

    def test_get_nonexistent_customer(self):
        """Getting a missing customer should return None."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = service.get("X999")
            self.assertIsNone(customer)

    def test_delete_nonexistent_customer(self):
        """Deleting a missing customer should return False."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            result = service.delete("X999")
            self.assertFalse(result)

    def test_update_nonexistent_customer_fails(self):
        """Updating a missing customer should return False."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            self.assertFalse(service.update("C404", name="X"))

    def test_update_invalid_record_fails(self):
        """Updating when stored record is not a dict should return False."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            store.save({"C001": "not-a-dict"})

            service = CustomerService(store)
            self.assertFalse(service.update("C001", name="X"))

    def test_get_malformed_record_returns_none(self):
        """Getting a malformed stored record should return None."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            # Missing required fields for Customer(**record)
            # -> TypeError -> None
            store.save({"C001": {"customer_id": "C001"}})

            service = CustomerService(store)
            self.assertIsNone(service.get("C001"))

    def test_update_customer_success(self):
        """Updating an existing customer should persist changes."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            service = CustomerService(store)

            customer = Customer("C010", "Old")
            self.assertTrue(service.create(customer))

            result = service.update("C010", name="New")
            self.assertTrue(result)

            updated = service.get("C010")
            self.assertIsNotNone(updated)
            self.assertEqual(updated.name, "New")

    def test_list_all_returns_empty_if_not_dict(self):
        """list_all should return {} if underlying store isn't a dict."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/customers.json")
            store.save(["not", "a", "dict"])

            service = CustomerService(store)
            self.assertEqual(service.list_all(), {})


if __name__ == "__main__":
    unittest.main()
