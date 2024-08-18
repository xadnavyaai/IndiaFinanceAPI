import pytest

from pyfinmuni import NSEApi

@pytest.fixture
def nse_api():
    return NSEApi()

def test_get_stock_codes(nse_api):
    stock_codes = nse_api.get_stock_codes()
    assert isinstance(stock_codes, dict)
    assert len(stock_codes) > 0
    for code, name in stock_codes.items():
        assert isinstance(code, str)
        assert isinstance(name, str)

def test_get_top_gainers(nse_api):
    top_gainers = nse_api.get_top_gainers()
    assert isinstance(top_gainers, dict)
    assert len(top_gainers) > 0

def test_get_top_losers(nse_api):
    top_losers = nse_api.get_top_losers()
    assert isinstance(top_losers, dict)
    assert len(top_losers) > 0

def test_get_all_indices(nse_api):
    all_indices = nse_api.get_all_indices()
    assert isinstance(all_indices, dict)
    assert len(all_indices) > 0

def test_get_quote(nse_api):
    quote = nse_api.get_quote("RELIANCE")
    assert isinstance(quote, dict)
    assert "lastPrice" in quote  # Check that 'lastPrice' is in the quote data

def test_get_historical_data(nse_api):
    historical_data = nse_api.get_historical_data("RELIANCE", "07-06-2024", "07-07-2024")
    assert isinstance(historical_data, dict)
    assert "data" in historical_data  # Assuming 'data' is a key in the response
    assert len(historical_data['data']) > 0  # Check that there is data returned

def test_is_valid_code(nse_api):
    assert nse_api.is_valid_code("RELIANCE") is True
    assert nse_api.is_valid_code("INVALID_CODE") is False

def test_get_index_list(nse_api):
    index_list = nse_api.get_index_list()
    assert isinstance(index_list, list)
    assert len(index_list) > 0
    for index in index_list:
        assert isinstance(index, str)

def test_get_index_quote(nse_api):
    index_quote = nse_api.get_index_quote("NIFTY 50")
    assert isinstance(index_quote, dict)
    assert len(index_quote) > 0
    assert "indexSymbol" in index_quote
    assert index_quote["indexSymbol"] == "NIFTY 50"

