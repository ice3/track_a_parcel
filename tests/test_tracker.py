"""Tests for the tracker file."""

import pytest

from app.tracker import Tracker


@pytest.fixture
def my_tracker():
    """Init a new tracker before each tests."""
    return Tracker()


def test_simple_parcel_string(my_tracker):
    """Test url creation with one parcel without options."""
    expected = '[{"trackingNumber": 1, "dstCountry": "FR", "postalService": "upu"}]'
    parcel_string = my_tracker.parcel_string(
        [[1]]
    )
    assert parcel_string == expected


def test_parcel_with_options_string(my_tracker):
    """Test url creation with options."""
    expected = '[{"trackingNumber": 1, "dstCountry": "DE", "postalService": "..."}]'
    parcel_string = my_tracker.parcel_string(
        [[1, "DE", "..."]]
    )
    assert parcel_string == expected


def test_multiple_parcels_string(my_tracker):
    """Test url creation with multiple parcels."""
    expected = (
        '[{"trackingNumber": 1, "dstCountry": "FR", '
        '"postalService": "upu"}, '
        '{"trackingNumber": 2, "dstCountry": "FR", "postalService": "upu"}]')
    parcels_string = my_tracker.parcel_string(
        [
            [1], [2]
        ]
    )
    assert parcels_string == expected
