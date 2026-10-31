
import pytest
from self_storage import rent_due, access_allowed, payment_status


# RENT DUE TEST CASES

def test_rent_small_deposit():
    assert rent_due("small", 1, False, False) == 0


def test_rent_medium_deposit():
    assert rent_due("medium", 2, False, False) == 0


def test_rent_large_deposit():
    assert rent_due("large", 3, False, False) == 0


def test_rent_member_discount():
    assert rent_due("small", 3, False, True) == 80


def test_rent_climate_control():
    assert rent_due("small", 3, True, False) == 240


def test_rent_long_duration():
    assert rent_due("small", 8, False, False) == 490


def test_rent_long_climate_duration():
    assert rent_due("small", 8, True, False) == 735


def test_rent_member_large_unit():
    assert rent_due("large", 5, False, True) == 160


def test_rent_invalid_unit():
    with pytest.raises(ValueError):
        rent_due("extra", 2, False, False)


def test_rent_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


# ACCESS ALLOWED TEST CASES

def test_owner_access_allowed():
    assert access_allowed(10, 4, True) is True


def test_owner_access_denied():
    assert access_allowed(10, 5, True) is False


def test_non_owner_access_allowed():
    assert access_allowed(12, 2, False) is True


def test_non_owner_too_many_visitors():
    assert access_allowed(12, 3, False) is False


def test_access_before_opening():
    assert access_allowed(5, 1, False) is False


def test_access_after_closing():
    assert access_allowed(23, 1, False) is False


# PAYMENT STATUS TEST CASES

def test_payment_autopay_current():
    assert payment_status(0, True, False) == "current"


def test_payment_manual_current():
    assert payment_status(5, False, False) == "current"


def test_payment_prior_late_current():
    assert payment_status(10, False, True) == "grace"


def test_payment_grace_period():
    assert payment_status(-10, False, False) == "grace"


def test_payment_prior_late_grace():
    assert payment_status(0, False, True) == "grace"


def test_payment_lien():
    assert payment_status(-11, False, False) == "lien"


def test_payment_autopay_lien():
    assert payment_status(-16, True, False) == "lien"
