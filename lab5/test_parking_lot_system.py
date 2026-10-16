
"""Basic tests for the parking lot system."""

import unittest

import parking_lot_system as parking


class ParkingLotTests(unittest.TestCase):
    """Verify core parking lot behavior."""

    def test_available_slot(self):
        self.assertTrue(parking.check_slot_availability("P02"))

    def test_unknown_slot_is_not_available(self):
        self.assertFalse(parking.check_slot_availability("P99"))

    def test_parking_fee_with_surge(self):
        self.assertEqual(parking.calculate_parking_fee("P03", 1.5), 45.0)

    def test_ticket_pin_has_four_digits(self):
        pin = parking.generate_ticket_pin()
        self.assertGreaterEqual(pin, 1000)
        self.assertLessEqual(pin, 9999)


if __name__ == "__main__":
    unittest.main()
