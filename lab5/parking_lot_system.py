
"""Parking lot management system with safer, cleaner Python practices."""

import hashlib
import os
import secrets
from pathlib import Path

PARKING_SLOTS = {
    "P01": {
        "plate": "KA01AB1234",
        "hours": 2,
        "rate": 20.0,
        "is_occupied": True,
    },
    "P02": {
        "plate": "TN07CD5678",
        "hours": 0,
        "rate": 20.0,
        "is_occupied": False,
    },
    "P03": {
        "plate": "MH02EF9012",
        "hours": 4,
        "rate": 30.0,
        "is_occupied": True,
    },
}

# A mutable container lets functions update collections without global.
COLLECTIONS = {"total": 0.0}


def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle if the requested slot exists and is vacant."""
    if slot_id not in PARKING_SLOTS:
        return False

    slot = PARKING_SLOTS[slot_id]
    if slot["is_occupied"] or hours_booked < 1:
        return False

    if entry_logs is None:
        entry_logs = []

    slot["plate"] = plate_no
    slot["hours"] = hours_booked
    slot["is_occupied"] = True
    charge = slot["rate"] * hours_booked
    COLLECTIONS["total"] += charge
    entry_logs.append(
        f"Vehicle {plate_no} parked at slot {slot_id} "
        f"for {hours_booked} hours; charge: {charge:.2f}"
    )
    return True


def release_slot(slot_id):
    """Release an occupied slot, returning False for an unknown slot."""
    slot = PARKING_SLOTS.get(slot_id)
    if slot is None:
        return False

    slot["is_occupied"] = False
    slot["plate"] = ""
    slot["hours"] = 0
    return True


def check_slot_availability(slot_id):
    """Return whether a known parking slot is vacant."""
    slot = PARKING_SLOTS.get(slot_id)
    return slot is not None and not slot["is_occupied"]


def calculate_parking_fee(slot_id, surge_multiplier=1.0):
    """Calculate a parking fee using a numeric surge multiplier."""
    if slot_id not in PARKING_SLOTS:
        raise ValueError(f"Unknown parking slot: {slot_id}")
    if not isinstance(surge_multiplier, (int, float)):
        raise TypeError("Surge multiplier must be numeric.")
    if surge_multiplier < 0:
        raise ValueError("Surge multiplier cannot be negative.")

    base_rate = PARKING_SLOTS[slot_id]["rate"]
    return base_rate * surge_multiplier


def generate_vehicle_hash(plate_no):
    """Return a SHA-256 digest for a vehicle registration number."""
    return hashlib.sha256(plate_no.encode("utf-8")).hexdigest()


def generate_ticket_pin():
    """Generate a four-digit ticket PIN using a secure random generator."""
    return secrets.randbelow(9000) + 1000


def export_parking_manifest(filename="parking_manifest.txt"):
    """Write the current parking manifest to a UTF-8 text file."""
    output_path = Path(filename)
    output_path.write_text(
        f"{PARKING_SLOTS}\n",
        encoding="utf-8",
    )
    print(f"Parking manifest exported to: {output_path}")


def get_available_summary(slots):
    """Count the vacant slots in the supplied parking-slot mapping."""
    return sum(
        not details["is_occupied"] for details in slots.values()
    )


def main():
    """Run a short demonstration of the parking lot functions."""
    barrier_key_configured = bool(
        os.environ.get("BARRIER_GATE_SECRET_TOKEN")
    )

    park_vehicle("P02", "DL03GH3456", 3)
    release_slot("P01")
    print("Is P02 available:", check_slot_availability("P02"))
    print("Surge Parking Fee:", calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary(PARKING_SLOTS))
    print("Barrier Key configured:", barrier_key_configured)


if __name__ == "__main__":
    main()
