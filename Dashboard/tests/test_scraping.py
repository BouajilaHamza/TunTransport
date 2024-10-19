import json
import os
from unittest.mock import patch

from Dashboard.utils.scraping import (
    get_available_destinations,
    get_departs,
    get_tarifs,
    wait_for_spider,
)

SCRAPING_URI = os.getenv("SCRAPING_URI")


@patch("Dashboard.utils.scraping.requests.post")
def test_get_departs(mock_post):
    # Arrange
    mock_post.return_value.status_code = 200  # Mocking successful response

    # Act
    get_departs()

    # Assert
    mock_post.assert_called_once_with(
        f"{SCRAPING_URI}/schedule.json", data={"project": "default", "spider": "dests"}
    )


@patch("Dashboard.utils.scraping.requests.post")
def test_get_available_destinations(mock_post):
    # Arrange
    depart_name = "Sample Depart"
    depart_id = "123"
    depart_company = "Sample Company"
    mock_post.return_value.status_code = 200  # Mocking successful response

    # Act
    get_available_destinations(depart_name, depart_id, depart_company)

    # Assert
    mock_post.assert_called_once_with(
        f"{SCRAPING_URI}/schedule.json",
        data={
            "project": "default",
            "spider": "deps",
            "depart": depart_name,
            "dep_id": depart_id,
            "Company": depart_company,
        },
    )


@patch("Dashboard.utils.scraping.requests.post")
def test_get_tarifs(mock_post):
    # Arrange
    _depart = {"key": "value"}
    _destination = {"key": "value"}
    company = "Sample Company"

    mock_post.return_value.json.return_value = {"tarif": 100}  # Mocking JSON response

    # Act
    result = get_tarifs(_depart, _destination, company)

    # Assert
    assert result == {"tarif": 100}
    mock_post.assert_called_once_with(
        f"{SCRAPING_URI}/schedule.json",
        data={
            "project": "default",
            "spider": "tarifs",
            "depart": json.dumps(_depart),
            "destination": json.dumps(_destination),
            "Company": company,
        },
    )


@patch("Dashboard.utils.scraping.requests.get")
def test_wait_for_spider(mock_get):
    # Arrange
    response = {"jobid": "12345"}

    mock_get.return_value.json.side_effect = [
        {"status": "not ok"},  # First call simulates job not done yet
        {"status": "ok"},  # Second call simulates job done
    ]

    # Act
    result = wait_for_spider(response)

    # Assert
    assert result is True
    assert mock_get.call_count == 2  # Ensure it called twice to check status
