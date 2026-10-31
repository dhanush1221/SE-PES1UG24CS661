
import pytest
from self_storage import rent_due, access_allowed, payment_status


# RENT DUE - BRANCH COVERAGE

def test_invalid_unit():
    with pytest.raises(ValueError):
        rent_due("extra", 2, False, False)


def test_valid_unit():
    assert rent_due("small", 1, False, False) == 0


def test_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


def test_non_negative_months():
    assert rent_due("small", 3, False, False) == 160


def test_member_small_unit():
    assert rent_due("small", 3, False, True) == 80


def test_member_large_unit():
    assert rent_due("large", 5, False, True) == 160


def test_extra_zero_or_negative():
    assert rent_due("small", 1, False, False) == 0


def test_climate_control_true():
    assert rent_due("small", 3, True, False) == 240


def test_climate_control_false():
    assert rent_due("small", 3, False, False) == 160


def test_extra_greater_than_six():
    assert rent_due("small", 8, False, False) == 490


def test_extra_greater_than_six_climate():
    assert rent_due("small", 8, True, False) == 735


# ACCESS ALLOWED - BRANCH COVERAGE

def test_owner_four_visitors():
    assert access_allowed(12, 4, True) is True


def test_owner_more_than_four_visitors():
    assert access_allowed(12, 5, True) is False


def test_non_owner_valid_access():
    assert access_allowed(12, 2, False) is True


def test_non_owner_too_many_visitors():
    assert access_allowed(12, 3, False) is False


def test_access_before_six():
    assert access_allowed(5, 1, False) is False


def test_access_after_twenty_two():
    assert access_allowed(23, 1, False) is False


def test_access_at_six():
    assert access_allowed(6, 2, False) is True


# PAYMENT STATUS - BRANCH COVERAGE

def test_autopay_current():
    assert payment_status(0, True, False) == "current"


def test_autopay_grace():
    assert payment_status(-1, True, False) == "grace"


def test_autopay_lien():
    assert payment_status(-16, True, False) == "lien"


def test_manual_payment_current():
    assert payment_status(5, False, False) == "current"


def test_manual_payment_grace():
    assert payment_status(4, False, False) == "grace"


def test_manual_payment_lien():
    assert payment_status(-11, False, False) == "lien"


def test_prior_late_current():
    assert payment_status(15, False, True) == "current"


def test_prior_late_grace():
    assert payment_status(14, False, True) == "grace"


def test_prior_late_lien():
    assert payment_status(-1, False, True) == "lien"
