import pytest
import requests_mock
from pyfinmuni import IndianMFApi  # Adjust this import according to your module structure

@pytest.fixture
def mf_api():
    return IndianMFApi()

def test_get_mf_list(mf_api, requests_mock):
    mock_data = [{"schemeName": "Test Fund", "schemeCode": 123456}]
    requests_mock.get("https://api.mfapi.in/mf", json=mock_data)
    
    mf_list = mf_api.get_mf_list()
    assert isinstance(mf_list, list)
    assert len(mf_list) > 0
    assert mf_list[0]['schemeName'] == "Test Fund"

def test_create_fund_code_map(mf_api):
    mock_fund_list = [{"schemeName": "Test Fund", "schemeCode": 123456}]
    fund_code_map = mf_api.create_fund_code_map(mock_fund_list)
    
    assert isinstance(fund_code_map, dict)
    assert fund_code_map["Test Fund"] == 123456

def test_is_valid_fund_code(mf_api):
    mock_fund_list = [{"schemeName": "Test Fund", "schemeCode": 123456}]
    mf_api.fund_code_map = mf_api.create_fund_code_map(mock_fund_list)
    
    assert mf_api.is_valid_fund_code(123456) is True
    assert mf_api.is_valid_fund_code(999999) is False

def test_get_mf_price_latest(mf_api, requests_mock):
    mock_data = {"meta": {"fund_house": "Test Fund House"}, "data": [{"date": "01-Jan-2024", "nav": "100.00"}]}
    requests_mock.get("https://api.mfapi.in/mf/123456/latest", json=mock_data)
    
    mf_api.fund_code_map = {"Test Fund": 123456}
    latest_price = mf_api.get_mf_price_latest(123456)
    
    assert isinstance(latest_price, dict)
    assert "meta" in latest_price
    assert latest_price["meta"]["fund_house"] == "Test Fund House"

def test_get_mf_price_latest_invalid_code(mf_api):
    mf_api.fund_code_map = {"Test Fund": 123456}
    latest_price = mf_api.get_mf_price_latest(999999)
    
    assert latest_price == {}

def test_get_mf_price_hist(mf_api, requests_mock):
    mock_data = {"meta": {"fund_house": "Test Fund House"}, "data": [{"date": "01-Jan-2024", "nav": "100.00"}]}
    requests_mock.get("https://api.mfapi.in/mf/123456", json=mock_data)
    
    mf_api.fund_code_map = {"Test Fund": 123456}
    price_hist = mf_api.get_mf_price_hist(123456)
    
    assert isinstance(price_hist, dict)
    assert "meta" in price_hist
    assert price_hist["meta"]["fund_house"] == "Test Fund House"

def test_get_mf_price_hist_invalid_code(mf_api):
    mf_api.fund_code_map = {"Test Fund": 123456}
    price_hist = mf_api.get_mf_price_hist(999999)
    
    assert price_hist == {}
