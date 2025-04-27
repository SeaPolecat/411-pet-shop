import pytest
import requests
from unittest.mock import patch, Mock
from pets.utils import api_utils

# Example breed to test with
TEST_BREED = "golden"

def test_get_image_success(mocker):
    """Test successful API call to get_image."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "https://images.dog.ceo/breeds/golden/n02099601_123.jpg"}
    
    mocker.patch('requests.get', return_value=mock_response)
    image_url = api_utils.get_image(TEST_BREED)
    
    assert image_url == "https://images.dog.ceo/breeds/golden/n02099601_123.jpg"

def test_get_image_api_failure(mocker, caplog):
    """Test API call failure with non-200 status code."""
    mock_response = Mock()
    mock_response.status_code = 500
    mocker.patch('requests.get', return_value=mock_response)

    with caplog.at_level('ERROR'):
        image_url = api_utils.get_image(TEST_BREED)
        assert image_url is None
        assert "API request failed with status code" in caplog.text

def test_get_image_exception(mocker, caplog):
    """Test exception during API call (e.g., network error)."""
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException("Network error"))

    with caplog.at_level('ERROR'):
        image_url = api_utils.get_image(TEST_BREED)
        assert image_url is None
        assert "Error fetching image for breed" in caplog.text
