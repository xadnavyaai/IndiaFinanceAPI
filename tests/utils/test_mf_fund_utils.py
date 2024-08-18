import pytest

@pytest.fixture
def mf_fund_utils():
    from pyfinmuni.utils import mf_fund_utils
    return mf_fund_utils

def test_find_top_fund_matches(mf_fund_utils):
    # Example queries
    query_fund_name = "SBI Bluechip Fund"
    top_matches = mf_fund_utils.find_top_fund_matches(query_fund_name)

    query_fund_name = "Principal Emerging Bluechip Fund - Growth Option"
    top_matches = mf_fund_utils.find_top_fund_matches(query_fund_name)
